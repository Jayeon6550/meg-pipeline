---------
Processes
---------


MEG Project Proposal
^^^^^^^^^^^^^^^^^^^^


All new project proposals must fill the following `form <https://docs.google.com/forms/d/e/1FAIpQLSeZb8tCBbH5FVo9E0uZn7FMjXzXNtYjC6s5Ln1gh_sofFSEBQ/viewform?usp=sharing>`_.
Add as many known details as possible regarding:

- the topic of your project
- the research question you are addressing
- additional systems that you will need to run your experiment successfully

.. .. mermaid::

..     graph TD;
..         A[🎓 <b>User arrives<br/>at MEG lab</b>] -->|🚀 Start| B[🧪 <b>Design<br/>Experiment</b>];
..         B -->|📢 Present| C[📝 <b>Present<br/>Research</b>];

..         %% Contribution Guide
..         C --> X[📖 <b><a href='https://neurowaves.readthedocs.io/en/latest/1-lab-overview/6-neurowaves-contribution.html'>
..         Contribution Guide</a></b>];

..         X -->|📂 Submit| D[💻 <b>Submit Draft Code<br/>via Pull Request</b>];
..         D -->|🔍 Review| E[✅ <b>Code<br/>Reviewed</b>];
..         E -->|🤔 Decision| F{⚖️ <b>Does Code<br/>Work?</b>};

..         F --❌ No --> G[🔄 <b>Iterate & Revise<br/>Code</b>];
..         G -->|📂 Resubmit| D;

..         F --✅ Yes --> H[🔬 <b>Keep Testing<br/>Code</b>];
..         H -->|🏆 Success| I[🎉 <b>Experiment<br/>Finalized</b>];

..         %% Clickable Node for GitHub PR
..         click D "https://github.com/BioMedicalImaging-Core-NYUAD/neurowaves-lab-documentation/pulls" "Visit GitHub Repository"

..         %% Style Definitions
..         classDef success fill:#4CAF50,stroke:#2E7D32,color:#fff;
..         classDef decision fill:#FFEB3B,stroke:#FBC02D,color:#000;
..         classDef process fill:#2196F3,stroke:#1976D2,color:#fff;
..         classDef warning fill:#FF5722,stroke:#E64A19,color:#fff;

..         class A,B,C,D,E,H,X process;
..         class F decision;
..         class G warning;
..         class I success;





Identifying your usage
^^^^^^^^^^^^^^^^^^^^^^

(Add usage form)





Booking a session for testing/debugging your stimulus code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**If you do NOT need MEG Scientist assistance:**

- You can book the lab anytime (24/7)
- Go to the `MEG Booking Portal <https://corelabs.abudhabi.nyu.edu/dashboard.php>`_
- Select **MEG System - KIT**

**If you DO need MEG Scientist assistance:**

- Sessions are restricted to **9:00 AM – 5:00 PM**
- Check the MEG Scientist's availability on his `calendar <https://calendar.google.com/calendar/u/0/r?cid=aHozNzUyQG55dS5lZHU>`_ or `email him <mailto:hadi.zaatiti@nyu.edu>`_
- Once availability is confirmed, book your lab slot via the `MEG Booking Portal <https://corelabs.abudhabi.nyu.edu/dashboard.php>`_
- Select **MEG System - KIT**

Alternatively, you can book via `Corelabs Reservations <https://corelabs.abudhabi.nyu.edu/>`_.

    



Booking an MEG data acquisition session
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. warning::

   While scheduling your experiment, avoid rush hours 8:30am and 5:30pm, and friday prayer time, as more noise can be introduced into the data due to outside movement.
   All bookings should not happen on a monday morning, as Helium refill is scheduled for monday mornings (8:00 am till 10:30 am)
   and it is not possible to acquire data during this period.
   Provide your `netID` to the MEG scientists `nyuad.meg@nyu.edu` for you to have access to the lab booking calendar.


Subscribing to the Google MEG Lab Calendar mirroring CTPSS Calendar
-------------------------------------------------------------------

To see the lab's availability directly in your Google Calendar:

1. Open `Google Calendar <https://calendar.google.com/>`_.
2. On the left side, next to **Other calendars**, click the **+** (plus) icon and select **Subscribe to calendar**.
3. In the **Add calendar** box, enter the following Lab Calendar ID:

   .. code-block:: text

      [MEG LAB] Corelabs CTPSS Data Acquisition Bookings

4. The calendar will now appear in your list under "Other calendars".

.. note::

   This calendar is not for booking the lab but acts only as a mirror to the official CTPSS calendar.
   Do not use this calendar for booking your lab, but only to schedule your participants as detailed below.


Scheduling Participants with Appointment Schedules on Google Calendar
---------------------------------------------------------------------

When recruiting participants, you can provide them with a link to book their own slots based on your availability **and** the lab's availability.

**1. Create an Appointment Schedule:**
    - In Google Calendar, click the **Create** button and select **Appointment schedule**.
    - Set your preferred hours and duration for the MEG sessions.

**2. Check Multiple Calendars for Availability:**
    - In the appointment schedule configuration, look for the **Calendars checked for availability** section.
    - Ensure **your primary calendar** is selected so slots aren't offered when you are busy.
    - Click **Calendars** and select the **[MEG LAB] Corelabs CTPSS Data Acquisition Bookings** (subscribed to in the previous step). This ensures participants can only book when the lab is also free.

**3. Share the Booking Link:**
    - Once the schedule is created, click **Share** to get a booking link.
    - Send this link to your participants. They will see the available slots that work for both you and the lab.

.. important::

    **After a participant books a slot via the link:**
    You must still ensure the lab is officially reserved in the Corelabs system.

    Scan the QR code below to book your lab for your usage, login with `Gmail` using your `@nyu.edu` account:

    .. image:: ../graphic/meg-calendar-qr.png
        :alt: MEG Calendar QR code
        :align: center


    or simply go to  `https://corelabs.abudhabi.nyu.edu/ <https://corelabs.abudhabi.nyu.edu/>`_

    If you do not have access to the booking system, please email `nyuad.meg@nyu.edu` to be added to the system.
    
    Under Reservations, Schedule, from the upper drop down menu pick `Brain Imaging` and then book the `MagnetoEncephaloGraphy MEG-KIT`.

    If you need the MEG scientist (Hadi Zaatiti) to be present during the booking (e.g., for training):
    - Ensure the slot is available on his calendar `hz3752@nyu.edu`.
    - Send a meeting invite to `hz3752` with subject `MEG Training (or Debug or other) of [name and netID of trainee]`.
    - Confirm the lab booking via Corelabs.




