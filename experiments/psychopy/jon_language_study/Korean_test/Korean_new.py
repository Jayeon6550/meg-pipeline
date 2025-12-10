import os, sys
import pandas as pd
from psychopy import core, visual, event, parallel, data, monitors, gui

from pypixxlib import _libdpx as dp
from experiments.psychopy.general.utilities import *


# ==============================================================
# 0) VPixx 기본 설정
# ==============================================================

TIME_TO_RESET_BUTTON_BOX = 1.7
TIME_WAIT_BREAK = 0.5

trigger = [[4, 0, 0], [16, 0, 0], [64, 0, 0],
           [0, 1, 0], [0, 4, 0], [0, 16, 0], [0, 64, 0], [0, 0, 1]]
channel_names = ['224', '225', '226', '227', '228', '229', '230', '231']
black = [0, 0, 0]

RESPONSE_SELECTION = {
    "right box": ["red", "yellow"],
}

def RGB2Trigger(color):
    return int((color[2] << 16) + (color[1] << 8) + color[0])

dp.DPxOpen()
dp.DPxDisableDoutPixelMode()
dp.DPxWriteRegCache()
dp.DPxSetDoutValue(RGB2Trigger(black), 0xFFFFFF)
dp.DPxUpdateRegCache()

responses = []


# ==============================================================
# 1) CSV 로드 + 실험 파라미터 기본 세팅
# ==============================================================

SCREEN_NUMBER = 2

trialList = data.importConditions('korean_test2.csv')
totalTrials = len(trialList)

clock = core.Clock()

backgroundColor = 'black'
instructionsFont = 'Malgun Gothic'
stimuliFont = 'Malgun Gothic'
stimuliColor = 'gold'
stimuliUnits = 'deg'
stimuliSize = 2

wordOn = 38
wordOff = 20
lastWordOn = 38

boxHeight = stimuliSize + 1.5
boxWidth = 15

FULL_SENTENCE_HEIGHT = 1.5    # context 폰트 크기
FULL_SENTENCE_OFF = wordOff   # context 후 간격
# ==============================================================
# 2) ✔ FIXATION / TASK / INSTRUCTION 세팅 (너가 말한 부분 그대로 유지)
# ==============================================================

fixationOn = 60
fixationOff = wordOff
fixationColor = 'red'
fixationSize = stimuliSize
fixationUnits = stimuliUnits

taskQuestionColor = 'red'
taskQuestionSize = 1.5
taskQuestionUnits = stimuliUnits
taskQuestionOff = wordOff

instructionColor = 'gold'
instructionSize = 1.5
INSTR_HEIGHT = 0.6
INSTR_WRAP = 30
instructionUnits = stimuliUnits
instructionOff = wordOff

breakKeyword = 'break'
breakColor = instructionColor
breakSize = instructionSize
breakUnits = instructionUnits
breakOff = wordOff


# ==============================================================
# 3) ✔ longestWordCount + longestSentence + practice/break/question 계산
# ==============================================================

longestWordCount = 0
longestWord = "none"
longestSentence = 0

totalBreakCount = 0
totalPracticeCount = 0
totalQuestionCount = 0

for idx in range(totalTrials):

    words = trialList[idx]['sentence'].split()

    # ---- 3-1) 가장 긴 단어 찾기 ----
    for w in words:
        if len(w) > longestWordCount:
            longestWordCount = len(w)
            longestWord = w

    # ---- 3-2) 가장 긴 문장(단어 개수) ----
    numWords = len(words)
    if numWords > longestSentence:
        longestSentence = numWords

    # ---- 3-3) practice trial 개수 ----
    if str(trialList[idx].get("subblock", "")).lower() == "practice":
        totalPracticeCount += 1

    # ---- 3-4) break trial 개수 ----
    if trialList[idx]['sentence'] == breakKeyword:
        totalBreakCount += 1

    # ---- 3-5) question 개수 ----
    tq = trialList[idx]['taskQuestion']
    if isinstance(tq, str) and len(tq) >= 4:
        totalQuestionCount += 1

# (디버그 출력 – 원래 네 코드처럼 유지)
print("Longest word:", longestWord)
print("Length:", longestWordCount)
print("Longest sentence (words):", longestSentence)


# ==============================================================
# 4) ✔ practiceCount 최종 결정 (CSV 기반)
# ==============================================================

practiceCount = totalPracticeCount


# ==============================================================
# 5) 결과 DataFrame 생성
# ==============================================================

subjectColumns = ['name', 'age', 'sex', 'handedness',
                  'experiment', 'list', 'sentence',
                  'taskQuestion', 'trigger',
                  'expectedAnswer', 'participantAnswer', 'answer']

wordColumns = ["word" + str(i) for i in range(1, longestSentence + 1)]
myColumns = subjectColumns + wordColumns

results = pd.DataFrame(index=range(totalTrials), columns=myColumns)


# ==============================================================
# 6) 참가자 정보 GUI (너의 원래 코드 그대로 유지)
# ==============================================================

myDlg = gui.Dlg(title="RSVP MEG experiment", size=(600, 600))
myDlg.addText('Participant Info', color='Red')
myDlg.addField('Participant Name:', 'First Last', tip='or subject code')
myDlg.addField('Age:', 21)
myDlg.addField('Biological Sex:', choices=["Female", "Male"])
myDlg.addField('Handedness:', 100)
myDlg.addText('Experiment Info', color='Red')
myDlg.addField('Experiment Name:', 'Korean')
myDlg.addField('Experiment List:', 1)
myDlg.show()

if myDlg.OK:
    participantInfo = myDlg.data
else:
    print('user cancelled')



# 창 생성
win = visual.Window(
    screen=1,
    size=[1919.5, 1079.5],
    fullscr=False,
    color=backgroundColor,
    monitor='testMonitor'
)

# ============================================================
# 초기 안내 화면
# ============================================================

instructions_text = "실험 개요"

stim = visual.TextStim(
    win,
    text=instructions_text,
    font=instructionsFont, units='deg',
    color=instructionColor,
    height=0.8,
    alignText='center',
    wrapWidth=30
)
stim.draw()
win.flip()

# self-paced
listenbutton(9)

for frameN in range(instructionOff - 1):
    win.flip()
win.flip()


### >>> NEW: 반응 통계 초기화
recentCorrectResponses = 0
totalCorrectResponses = 0
trialsSinceLastBreak = 0
### <<< END NEW


# ============================================================
# ======================= PART 2 ==============================
# ============================================================

# Loop for each trial
prev_block = None
last_task_block = None

for trialIndex in range(totalTrials):

    pauseResponse = []
    responses = []
    event.clearEvents()

    # 현재 trial의 subblock 값 읽기 (practice 여부 파악)
    curr_subblock = str(trialList[trialIndex].get("subblock", "")).lower()

    # ------------------------------------------------------------
    # NEW: 현재 trial의 block 값 안전 변환
    # ------------------------------------------------------------
    raw_block = trialList[trialIndex].get("block")
    try:
        curr_block = int(float(raw_block)) if raw_block not in (None, "", "nan", "NaN", "NA") else 0
    except:
        curr_block = 0

    if curr_block not in (1, 2, 3):
        curr_block = 0
    # ------------------------------------------------------------

    sentence_text = trialList[trialIndex]['sentence']

    # ============================================================
    #  (A) BREAK 처리
    # ============================================================
    if sentence_text == breakKeyword:

        ### >>> NEW: practice 종료 break인지 확인
        is_practice_end_break = (prev_subblock == "practice")
        ### <<< END NEW

        if is_practice_end_break:
            # -----------------------------------------------------
            # practice 후에 등장하는 break → "연습문항이 끝났습니다!"
            # -----------------------------------------------------
            msg = (
                '연습문항이 끝났습니다!\n\n'
                '지금까지 %i개의 문항 중 %i문항을 맞추셨습니다.\n\n'
                '본 실험을 시작할 준비가 되면\n'
                '"예"(검지)를 눌러주세요.'
            ) % (trialsSinceLastBreak, recentCorrectResponses)

            stim = visual.TextStim(
                win, text=msg,
                font=instructionsFont, units='deg',
                color=instructionColor, height=0.9,
                alignText='center', wrapWidth=30
            )
            stim.setPos((0, 0))
            stim.draw()
            win.flip()

            core.wait(TIME_WAIT_BREAK)
            listenbutton(9)

            # practice 카운트 리셋
            recentCorrectResponses = 0
            trialsSinceLastBreak = 0

        else:
            # -----------------------------------------------------
            # 일반 break (subblock 끝날 때마다)
            # 기존 메시지 그대로 유지
            # -----------------------------------------------------
            msg = (
                '지금까지 %i개의 문장을 완료했고,\n'
                '앞으로 %i개의 문장이 남았습니다.\n\n'
                '다음 문장을 읽을 준비가 되면\n'
                '움직이지 말고 눈을 깜박이지 않은 채로\n\n'
                '"예"(검지)를 누르세요.'
            ) % (recentCorrectResponses, (totalTrials - trialIndex))

            stim = visual.TextStim(
                win, text=msg,
                font=instructionsFont, units='deg',
                color=instructionColor, height=0.8,
                alignText='center', wrapWidth=30
            )

            print("break window")

            stim.setPos((0, 0))
            stim.draw()
            win.flip()

            core.wait(TIME_WAIT_BREAK)
            listenbutton(9)

            recentCorrectResponses = 0
            trialsSinceLastBreak = 0

        # break trial 기록
        results.loc[trialIndex, 'name'] = participantInfo[0]
        results.loc[trialIndex, 'age'] = participantInfo[1]
        results.loc[trialIndex, 'sex'] = participantInfo[2]
        results.loc[trialIndex, 'handedness'] = participantInfo[3]
        results.loc[trialIndex, 'experiment'] = participantInfo[4]
        results.loc[trialIndex, 'list'] = participantInfo[5]
        results.loc[trialIndex, 'sentence'] = 'break'

        prev_subblock = curr_subblock
        continue

    # ============================================================
    #  (B) BLOCK 시작 시 인스트럭션 표시 (practice 이전에만)
    # ============================================================
    ### >>> NEW: block 전환 + practice 시작 전 인스트럭션
    if curr_block in (1, 2, 3) and curr_block != prev_block:
        # 새 블록에서 practice를 아직 안 했으면 인스트럭션 출력
        if curr_subblock == "practice":
            if curr_block == 1:
                instr_text = (
                    '이번 세션은 문장을 읽고 질문에 답하는 과제입니다.\n\n'
                    '잠시 후 연습문항이 먼저 제시됩니다.\n'
                    '"예"(검지)를 눌러 연습문항을 시작하세요.'
                )
            elif curr_block == 2:
                instr_text = (
                    '이번 세션에서는 단어 단위로 문장이 제시됩니다.\n\n'
                    '잠시 후 연습문항이 먼저 제시됩니다.\n'
                    '"예"(검지)를 눌러 연습문항을 시작하세요.'
                )
            else:  # block 3
                instr_text = (
                    '이번 세션은 wh-질문 이해 과제입니다.\n\n'
                    '잠시 후 연습문항이 먼저 제시됩니다.\n'
                    '"예"(검지)를 눌러 연습문항을 시작하세요.'
                )

            stim = visual.TextStim(
                win, text=instr_text,
                font=stimuliFont, units='deg',
                color=instructionColor, height=INSTR_HEIGHT,
                alignText='center', wrapWidth=INSTR_WRAP
            )
            stim.setPos((0, 0))
            stim.draw()
            win.flip()
            listenbutton(9)

        prev_block = curr_block
    ### <<< END NEW

    # 계속해서 PART 3에서 RSVP 시작…

    prev_subblock = curr_subblock

# ============================================================
# ======================= PART 3 ==============================
# ============================================================

    # ------------------------------------------------------------
    # 실제 trial (practice 포함) 시작
    # ------------------------------------------------------------

    print(trialList[trialIndex]['sentence'])

    # 현재 trial이 실제 trial이므로 last_task_block 업데이트
    last_task_block = curr_block

    words = trialList[trialIndex]['sentence'].split()
    numWords = len(words)

    # 트리거 준비 (기존 코드 그대로 유지)
    triggerList = range(
        int(trialList[trialIndex]['trigger']),
        int(trialList[trialIndex]['trigger']) + numWords
    )

    # fixation 박스 생성 (기존 그대로)
    box = visual.Rect(
        win, width=boxWidth, height=boxHeight, units='deg'
    )
    box.setPos((0, 0))
    box.setLineColor('red')
    box.setAutoDraw(True)

    # fixation ON
    for frameN in range(fixationOn):
        win.flip()
        if frameN == 0:
            clock.reset()
    win.flip()

    # fixation OFF
    for frameN in range(fixationOff - 2):
        win.flip()
    win.flip()

    # ------------------------------------------------------------
    # context (통문장) 표시 — block 1과 3에서만 (기존 코드 유지)
    # ------------------------------------------------------------
    if curr_block in (1, 3):
        option1 = str(trialList[trialIndex].get('option1', '')).strip()
        option2 = str(trialList[trialIndex].get('option2', '')).strip()

        if option1 or option2:
            try:
                box.setAutoDraw(False)
            except:
                pass

            full_text = str(trialList[trialIndex].get('context', '')).strip()

            full_stim = visual.TextStim(
                win, text=full_text,
                font=stimuliFont, units='deg',
                height=FULL_SENTENCE_HEIGHT,
                color=taskQuestionColor,
                alignText='center',
                wrapWidth=30
            )
            full_stim.setPos((0, 0))
            full_stim.draw()
            win.flip()

            # self-paced 진행
            listenbutton(9)

            # context → word transition
            for frameN in range(FULL_SENTENCE_OFF - 1):
                win.flip()
            win.flip()

            try:
                box.setAutoDraw(True)
            except:
                pass

    # ============================================================
    # RSVP — 단어 단위 제시 (기존 코드 그대로 유지)
    # ============================================================

    for wordIndex in range(numWords):
        print(repr(words[wordIndex]))

        stim = visual.TextStim(
            win, text=words[wordIndex],
            font=stimuliFont, units='deg',
            height=stimuliSize, color=stimuliColor,
            alignText='center'
        )
        stim.setPos((0, 0))

        # --------------------------------------------------------
        # 마지막 단어일 때 (lastWordOn 사용)
        # --------------------------------------------------------
        if wordIndex == (numWords - 1):
            for frameN in range(lastWordOn):
                stim.draw()
                win.flip()

                if frameN == 0:
                    clock.reset()

                # 트리거 (기존 로직 그대로)
                if frameN < 10:
                    combined_trigger_value = (
                        trialList[trialIndex]['trigger224w'] * trigger_channels_dictionary[224] +
                        trialList[trialIndex]['trigger225w'] * trigger_channels_dictionary[225] +
                        trialList[trialIndex]['trigger226w'] * trigger_channels_dictionary[226] +
                        trialList[trialIndex]['trigger227w'] * trigger_channels_dictionary[227] +
                        trialList[trialIndex]['trigger228w'] * trigger_channels_dictionary[228] +
                        trialList[trialIndex]['trigger229w'] * trigger_channels_dictionary[229] +
                        trialList[trialIndex]['trigger230w'] * trigger_channels_dictionary[230] +
                        trialList[trialIndex]['trigger231w'] * trigger_channels_dictionary[231]
                    )

                    dp.DPxSetDoutValue(int(combined_trigger_value), 0xFFFFFF)
                    dp.DPxUpdateRegCache()

                if frameN == 10:
                    dp.DPxSetDoutValue(RGB2Trigger(black), 0xFFFFFF)
                    dp.DPxUpdateRegCache()

            win.flip()
            results.loc[trialIndex, wordIndex + len(subjectColumns)] = clock.getTime()

        else:
            # --------------------------------------------------------
            # 첫 단어 OR 중간 단어 (기존 wordOn 사용)
            # --------------------------------------------------------
            for frameN in range(wordOn):
                stim.draw()
                win.flip()

                if frameN == 0:
                    clock.reset()

                if frameN < 10:
                    if wordIndex == 0:
                        combined_trigger_value = (
                            trialList[trialIndex]['trigger224'] * trigger_channels_dictionary[224] +
                            trialList[trialIndex]['trigger225'] * trigger_channels_dictionary[225] +
                            trialList[trialIndex]['trigger226'] * trigger_channels_dictionary[226] +
                            trialList[trialIndex]['trigger227'] * trigger_channels_dictionary[227] +
                            trialList[trialIndex]['trigger228'] * trigger_channels_dictionary[228] +
                            trialList[trialIndex]['trigger229'] * trigger_channels_dictionary[229] +
                            trialList[trialIndex]['trigger230'] * trigger_channels_dictionary[230] +
                            trialList[trialIndex]['trigger231'] * trigger_channels_dictionary[231]
                        )
                    else:
                        combined_trigger_value = (
                            trialList[trialIndex]['trigger224w'] * trigger_channels_dictionary[224] +
                            trialList[trialIndex]['trigger225w'] * trigger_channels_dictionary[225] +
                            trialList[trialIndex]['trigger226w'] * trigger_channels_dictionary[226] +
                            trialList[trialIndex]['trigger227w'] * trigger_channels_dictionary[227] +
                            trialList[trialIndex]['trigger228w'] * trigger_channels_dictionary[228] +
                            trialList[trialIndex]['trigger229w'] * trigger_channels_dictionary[229] +
                            trialList[trialIndex]['trigger230w'] * trigger_channels_dictionary[230] +
                            trialList[trialIndex]['trigger231w'] * trigger_channels_dictionary[231]
                        )

                    dp.DPxSetDoutValue(int(combined_trigger_value), 0xFFFFFF)
                    dp.DPxUpdateRegCache()

                if frameN == 10:
                    dp.DPxSetDoutValue(RGB2Trigger(black), 0xFFFFFF)
                    dp.DPxUpdateRegCache()

            win.flip()
            results.loc[trialIndex, wordIndex + len(subjectColumns)] = clock.getTime()

        # 단어 간 간격
        for frameN in range(wordOff - 2):
            win.flip()
        win.flip()

    # box 숨김
    box.setAutoDraw(False)

    # ------------------------------------------------------------
    # PART 4(질문 처리)로 계속됨
    # ------------------------------------------------------------
# ============================================================
# ======================= PART 4 ==============================
# ============================================================

    # ------------------------------------------------------------
    # 질문 표시: Block 1/3 → 2지선다 / Block 2 → taskQuestion
    # ------------------------------------------------------------

    option1 = str(trialList[trialIndex].get('option1', '')).strip()
    option2 = str(trialList[trialIndex].get('option2', '')).strip()

    # ============================================================
    # 2지선다 (block 1 & 3)
    # ============================================================
    if curr_block in (1, 3) and (option1 or option2):

        event.clearEvents()

        question_text = f"① {option1}\n\n② {option2}\n\n"

        stim = visual.TextStim(
            win, text=question_text,
            font=stimuliFont, units='deg',
            height=1.5, color=taskQuestionColor,
            alignText='center', wrapWidth=30
        )
        stim.setPos((0, -2.5))
        stim.draw()
        win.flip()

        response = getbuttonColor(RESPONSE_SELECTION)
        responses.append(response)

        stim = visual.TextStim(
            win, text='모든 버튼에서 손가락을 떼주세요.\n\n',
            font=stimuliFont, units='deg',
            height=1.5, color=taskQuestionColor,
            alignText='center', wrapWidth=30
        )
        stim.setPos((0, -1.5))
        stim.draw()
        win.flip()

        core.wait(TIME_TO_RESET_BUTTON_BOX)

        # 정답 처리
        if trialList[trialIndex]['correctAnswer'] == 9 and responses[-1] == ('right box', 'red'):
            recentCorrectResponses += 1
            totalCorrectResponses += 1
            answer = 1
        elif trialList[trialIndex]['correctAnswer'] == 7 and responses[-1] == ('right box', 'yellow'):
            recentCorrectResponses += 1
            totalCorrectResponses += 1
            answer = 1
        else:
            answer = 0

        for frameN in range(taskQuestionOff - 1):
            win.flip()
        win.flip()

        trialsSinceLastBreak += 1

    # ============================================================
    # block2 OR 2지선다 옵션 없을 때 → 기존 taskQuestion 방식
    # ============================================================
    else:
        if isinstance(trialList[trialIndex]['taskQuestion'], str) and len(trialList[trialIndex]['taskQuestion']) >= 4:

            event.clearEvents()

            stim = visual.TextStim(
                win, text=trialList[trialIndex]['taskQuestion'],
                font=stimuliFont, units='deg',
                height=1.5, color=taskQuestionColor,
                alignText='center', wrapWidth=30
            )
            stim.setPos((0, 0))
            stim.draw()
            win.flip()

            response = getbuttonColor(RESPONSE_SELECTION)
            responses.append(response)

            stim = visual.TextStim(
                win, text='모든 버튼에서 손가락을 떼주세요.\n\n',
                font=stimuliFont, units='deg',
                height=1, color=taskQuestionColor,
                alignText='center', wrapWidth=30
            )
            stim.setPos((0, -2.5))
            stim.draw()
            win.flip()

            core.wait(TIME_TO_RESET_BUTTON_BOX)

            if trialList[trialIndex]['correctAnswer'] == 9 and responses[-1] == ('right box', 'red'):
                recentCorrectResponses += 1
                totalCorrectResponses += 1
                answer = 1
            elif trialList[trialIndex]['correctAnswer'] == 7 and responses[-1] == ('right box', 'yellow'):
                recentCorrectResponses += 1
                totalCorrectResponses += 1
                answer = 1
            else:
                answer = 0

            for frameN in range(taskQuestionOff - 1):
                win.flip()
            win.flip()

            trialsSinceLastBreak += 1

    # ============================================================
    # 결과 저장 (기존 코드 구조 유지)
    # ============================================================

    results.loc[trialIndex, 'name'] = participantInfo[0]
    results.loc[trialIndex, 'age'] = participantInfo[1]
    results.loc[trialIndex, 'sex'] = participantInfo[2]
    results.loc[trialIndex, 'handedness'] = participantInfo[3]
    results.loc[trialIndex, 'experiment'] = participantInfo[4]
    results.loc[trialIndex, 'list'] = participantInfo[5]
    results.loc[trialIndex, 'sentence'] = trialList[trialIndex]['sentence']
    results.loc[trialIndex, 'taskQuestion'] = trialList[trialIndex]['taskQuestion']
    results.loc[trialIndex, 'trigger'] = trialList[trialIndex]['trigger']

    # 옵션 저장
    results.loc[trialIndex, 'option1'] = option1
    results.loc[trialIndex, 'option2'] = option2

    if curr_block in (1, 3) and (option1 or option2):
        results.loc[trialIndex, 'expectedAnswer'] = trialList[trialIndex]['correctAnswer']
        results.loc[trialIndex, 'participantAnswer'] = responses[-1][1] if responses else ''
        results.loc[trialIndex, 'answer'] = answer
    elif isinstance(trialList[trialIndex]['taskQuestion'], str):
        results.loc[trialIndex, 'expectedAnswer'] = trialList[trialIndex]['correctAnswer']
        results.loc[trialIndex, 'participantAnswer'] = responses[-1][1] if responses else ''
        results.loc[trialIndex, 'answer'] = answer
    else:
        results.loc[trialIndex, 'expectedAnswer'] = ''
        results.loc[trialIndex, 'participantAnswer'] = ''
        results.loc[trialIndex, 'answer'] = ''

    # 실시간 저장
    participantName = participantInfo[0].replace(" ", "")
    filename = 'results.' + participantName + '.csv'
    results.to_csv(filename, encoding='utf-8-sig')

# ============================================================
# ======================= PART 5 ==============================
# ============================================================

    # ------------------------------------------------------------
    # inter-trial 안내 메시지 (기존 코드 유지)
    # ------------------------------------------------------------

    event.clearEvents()

    stim = visual.TextStim(
        win,
        text=(
            '지금은 눈을 깜빡이셔도 괜찮습니다.\n\n'
            '다음 문장을 읽을 준비가 되면\n\n'
            '움직이지 말고, 눈을 깜빡이지 않은 채로\n\n'
            '"예"(검지)를 누르세요.\n\n'
        ),
        font=stimuliFont, units='deg',
        height=1, color=stimuliColor,
        wrapWidth=30, alignText='center'
    )
    stim.setPos((0, -1.5))
    stim.draw()
    win.flip()

    # self-paced
    listenbutton(9)

    for frameN in range(taskQuestionOff - 1):
        win.flip()
    win.flip()

    # ------------------------------------------------------------
    # 루프 끝 — 다음 trial로 이동
    # ------------------------------------------------------------
# ============================================================
# ======================= PART 6 ==============================
# ============================================================

# 루프 끝 — 실험 전체 종료 메시지
event.clearEvents()

stim = visual.TextStim(
    win,
    text=(
        '실험을 모두 마치셨습니다.\n\n'
        '잠시만 움직이지 말아주세요.\n'
        '약 30초 동안 마지막 기록을 진행합니다.\n\n'
        '총 %i개의 문장을 읽었고,\n'
        '%i개의 질문 중 %i개를 맞추셨습니다.'
        % (
            (totalTrials - totalBreakCount - practiceCount),
            totalQuestionCount,
            totalCorrectResponses
        )
    ),
    font=stimuliFont, units='deg',
    color=stimuliColor, height=INSTR_HEIGHT,
    alignText='center', wrapWidth=INSTR_WRAP
)

stim.setPos((0, 0))
stim.draw()
win.flip()

# 종료 전에 키 입력 대기
event.waitKeys()

# 최종 저장
participantName = participantInfo[0].replace(" ", "")
filename = 'results.' + participantName + '.csv'
results.to_csv(filename, encoding='utf-8-sig')

# 창 닫기
win.close()
core.quit()

# VPixx 장비 종료
dp.DPxClose()
