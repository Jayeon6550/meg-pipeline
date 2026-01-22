import os
import hashlib
import datetime as dt
from typing import Dict, Any, List, Optional, Tuple

import requests
from dotenv import load_dotenv
from icalendar import Calendar
from dateutil import tz
from google.oauth2 import service_account
from googleapiclient.discovery import build


# ----------------------------
# Config / constants
# ----------------------------
SYNC_SOURCE = "booked-ics"
# Set to "true" in env if you want to delete events that disappeared from ICS
ENABLE_DELETES = False


def env_bool(name: str, default: bool = False) -> bool:
    v = os.environ.get(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "y", "on")


def require_env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return v


def to_rfc3339(dt_obj: dt.datetime) -> str:
    """Ensure RFC3339 with timezone offset."""
    if dt_obj.tzinfo is None:
        # assume local if naive
        dt_obj = dt_obj.replace(tzinfo=tz.tzlocal())
    return dt_obj.isoformat()


def normalize_uid(uid: str) -> str:
    uid = (uid or "").strip()
    # Some feeds include parameters; keep stable plain string
    return uid


def stable_hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def fetch_ics(url: str) -> bytes:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.content


def parse_ics(ics_bytes: bytes) -> List[Dict[str, Any]]:
    cal = Calendar.from_ical(ics_bytes)
    events: List[Dict[str, Any]] = []

    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        uid = normalize_uid(str(component.get("UID", "")))
        summary = str(component.get("SUMMARY", "") or "")
        description = str(component.get("DESCRIPTION", "") or "")
        location = str(component.get("LOCATION", "") or "")

        # ---- LOCATION FILTER (optional) ----
        loc_contains = os.environ.get("SYNC_LOCATION_CONTAINS", "").strip()
        if loc_contains:
            # normalize spaces to avoid double-space mismatches
            def norm(s: str) -> str:
                return " ".join(s.split()).lower()

            if norm(loc_contains) not in norm(location):
                continue

        dtstart = component.get("DTSTART").dt if component.get("DTSTART") else None
        dtend = component.get("DTEND").dt if component.get("DTEND") else None

        if not uid or not dtstart:
            continue

        # Handle all-day events (date not datetime)
        all_day = isinstance(dtstart, dt.date) and not isinstance(dtstart, dt.datetime)
        if all_day:
            # For all-day, DTEND is often next day; keep date objects
            start_payload = {"date": dtstart.isoformat()}
            if isinstance(dtend, dt.date) and not isinstance(dtend, dt.datetime):
                end_payload = {"date": dtend.isoformat()}
            else:
                # if missing/odd, set end = start + 1 day
                end_payload = {"date": (dtstart + dt.timedelta(days=1)).isoformat()}
        else:
            # Ensure timezone-aware
            if dtstart.tzinfo is None:
                dtstart = dtstart.replace(tzinfo=tz.tzlocal())
            if dtend is None:
                dtend = dtstart + dt.timedelta(hours=1)
            elif isinstance(dtend, dt.date) and not isinstance(dtend, dt.datetime):
                # rare: DTSTART datetime, DTEND date
                dtend = dt.datetime.combine(dtend, dt.time(0, 0)).replace(tzinfo=tz.tzlocal())
            elif dtend.tzinfo is None:
                dtend = dtend.replace(tzinfo=tz.tzlocal())

            start_payload = {"dateTime": to_rfc3339(dtstart)}
            end_payload = {"dateTime": to_rfc3339(dtend)}

        # Build a content hash so we can detect changes
        content_fingerprint = stable_hash(
            "|".join([uid, summary, description, location, str(dtstart), str(dtend)])
        )

        events.append(
            {
                "uid": uid,
                "summary": summary,
                "description": description,
                "location": location,
                "start": start_payload,
                "end": end_payload,
                "fingerprint": content_fingerprint,
            }
        )

    return events


def get_calendar_service(sa_file: str):
    scopes = ["https://www.googleapis.com/auth/calendar"]
    creds = service_account.Credentials.from_service_account_file(sa_file, scopes=scopes)
    return build("calendar", "v3", credentials=creds, cache_discovery=False)


def find_existing_event(service, calendar_id: str, uid: str) -> Optional[Dict[str, Any]]:
    """
    Find an event by privateExtendedProperty marker.
    This avoids having to store a local mapping database.
    """
    prop = f"booked_uid={uid}"
    resp = (
        service.events()
        .list(
            calendarId=calendar_id,
            privateExtendedProperty=prop,
            maxResults=2,
            singleEvents=True,
            showDeleted=False,
        )
        .execute()
    )
    items = resp.get("items", [])
    if not items:
        return None
    return items[0]


def upsert_event(service, calendar_id: str, e: Dict[str, Any]) -> Tuple[str, str]:
    uid = e["uid"]

    body = {
        "summary": e["summary"] or "Booked reservation",
        "description": e["description"] or "",
        "location": e["location"] or "",
        "start": e["start"],
        "end": e["end"],
        "extendedProperties": {
            "private": {
                "booked_source": SYNC_SOURCE,
                "booked_uid": uid,
                "booked_fingerprint": e["fingerprint"],
            }
        },
    }

    existing = find_existing_event(service, calendar_id, uid)

    if existing is None:
        created = service.events().insert(calendarId=calendar_id, body=body).execute()
        return "created", created["id"]

    # Only update if fingerprint changed
    existing_private = (existing.get("extendedProperties", {}) or {}).get("private", {}) or {}
    old_fp = existing_private.get("booked_fingerprint")

    if old_fp == e["fingerprint"]:
        return "unchanged", existing["id"]

    updated = service.events().patch(calendarId=calendar_id, eventId=existing["id"], body=body).execute()
    return "updated", updated["id"]


def list_tagged_events_in_window(service, calendar_id: str, time_min: str, time_max: str) -> Dict[str, Dict[str, Any]]:
    """
    List all events in a time window that were created by this sync (booked_source=booked-ics).
    Returns mapping uid -> event
    """
    tagged: Dict[str, Dict[str, Any]] = {}
    page_token = None
    prop = f"booked_source={SYNC_SOURCE}"

    while True:
        resp = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                showDeleted=False,
                maxResults=2500,
                pageToken=page_token,
                privateExtendedProperty=prop,
            )
            .execute()
        )

        for item in resp.get("items", []):
            priv = ((item.get("extendedProperties") or {}).get("private") or {})
            uid = priv.get("booked_uid")
            if uid:
                tagged[uid] = item

        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return tagged


def main():
    load_dotenv()

    ics_url = require_env("BOOKED_ICS_URL")
    calendar_id = require_env("GOOGLE_CALENDAR_ID")
    sa_file = require_env("GOOGLE_SA_FILE")

    # Optional tuning
    lookback_days = int(os.environ.get("SYNC_LOOKBACK_DAYS", "7"))
    lookahead_days = int(os.environ.get("SYNC_LOOKAHEAD_DAYS", "60"))
    global ENABLE_DELETES
    ENABLE_DELETES = env_bool("ENABLE_DELETES", False)

    print("=== Fetching ICS ===")
    print("ICS URL:", ics_url.split("icskey=")[0] + "icskey=REDACTED" if "icskey=" in ics_url else ics_url)
    ics_bytes = fetch_ics(ics_url)
    print("Downloaded bytes:", len(ics_bytes))

    print("=== Parsing ICS ===")
    ics_events = parse_ics(ics_bytes)
    print(f"Found {len(ics_events)} VEVENTs")

    print("=== Google Calendar Auth ===")
    service = get_calendar_service(sa_file)

    created = updated = unchanged = 0

    print("=== Upserting events ===")
    for e in ics_events:
        status, event_id = upsert_event(service, calendar_id, e)
        if status == "created":
            created += 1
        elif status == "updated":
            updated += 1
        else:
            unchanged += 1

    print(f"Done. created={created}, updated={updated}, unchanged={unchanged}")

    # Optional deletion pass (safe window)
    # Only deletes events previously created by this sync within the window.
    if ENABLE_DELETES:
        now = dt.datetime.now(tz=tz.UTC)
        time_min = (now - dt.timedelta(days=lookback_days)).isoformat()
        time_max = (now + dt.timedelta(days=lookahead_days)).isoformat()

        print("=== Deletion check (enabled) ===")
        tagged = list_tagged_events_in_window(service, calendar_id, time_min, time_max)
        uids_in_ics = {e["uid"] for e in ics_events}

        to_delete = [uid for uid in tagged.keys() if uid not in uids_in_ics]
        print(f"Tagged events in window: {len(tagged)} | missing from ICS: {len(to_delete)}")

        for uid in to_delete:
            ev = tagged[uid]
            service.events().delete(calendarId=calendar_id, eventId=ev["id"]).execute()
            print("Deleted event for UID:", uid)

    print("✅ Sync finished")


if __name__ == "__main__":
    main()
