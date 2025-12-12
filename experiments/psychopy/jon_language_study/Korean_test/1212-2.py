import os, sys
import pandas as pd
from psychopy import core, visual, event, parallel, data, monitors, gui
from pypixxlib import _libdpx as dp
from experiments.psychopy.general.utilities import *

# ==============================================================
# 0) Basic VPixx setting
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
# 1) Road csv file + basic setting for parameter
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

FULL_SENTENCE_HEIGHT = 1.5
FULL_SENTENCE_OFF = wordOff


# ==============================================================
# 2) Fixation / Task / Instruction setting
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
# 3) Compute longestWordCount, longestSentence, and counts
# ==============================================================

totalQuestionCount = 0
totalBreakCount = 0
totalPracticeCount = 0
longestWordCount = 0
longestWord = "none"
longestSentence = 0

for idx in range(totalTrials):

    words = trialList[idx]['sentence'].split()

    for w in words:
        if len(w) > longestWordCount:
            longestWordCount = len(w)
            longestWord = w

    numWords = len(words)
    if numWords > longestSentence:
        longestSentence = numWords

    if str(trialList[idx].get("subblock", "")).lower() == "practice":
        totalPracticeCount += 1

    if trialList[idx]['sentence'] == breakKeyword:
        totalBreakCount += 1

    tq = trialList[idx]['taskQuestion']
    if isinstance(tq, str) and len(tq) >= 4:
        totalQuestionCount += 1

print("Longest word:", longestWord)
print("Length:", longestWordCount)
print("Longest sentence (words):", longestSentence)
print("Practice trials:", totalPracticeCount)
print("Break trials:", totalBreakCount)
print("Questions:", totalQuestionCount)

practiceCount = totalPracticeCount


# ==============================================================
# ### NEW: block별 REAL trial 총 개수 사전 계산 (practice/break 제외)
# ==============================================================

block_real_total = {1: 0, 2: 0, 3: 0}
for i in range(totalTrials):
    row = trialList[i]
    sentence_text = row['sentence']
    sub = str(row.get("subblock", "")).lower()

    raw_block = row.get("block")
    try:
        blk = int(float(raw_block)) if raw_block not in (None, "", "nan", "NaN", "NA") else 0
    except:
        blk = 0

    if blk in (1, 2, 3) and sub != "practice" and sentence_text != breakKeyword:
        block_real_total[blk] += 1

# ==============================================================
# ### NEW: 전체 REAL trial 총 개수 (모든 블록 통합)  ✅(남은 개수 표시용)
# ==============================================================

total_real_trial_total = block_real_total[1] + block_real_total[2] + block_real_total[3]


# ==============================================================
# ### NEW: helper - practice 시작 시 "다음 real block" 찾기 (CSV에서 practice block=0 대응)
# ==============================================================

def find_upcoming_real_block(start_index):
    """
    현재 인덱스(start_index) 이후에서, 첫 번째 real trial의 block(1/2/3)을 찾아 반환.
    못 찾으면 0 반환.
    """
    for j in range(start_index, totalTrials):
        r = trialList[j]
        s = r['sentence']
        sub = str(r.get("subblock", "")).lower()
        rb = r.get("block")
        try:
            b = int(float(rb)) if rb not in (None, "", "nan", "NaN", "NA") else 0
        except:
            b = 0
        if s != breakKeyword and sub != "practice" and b in (1, 2, 3):
            return b
    return 0


# ==============================================================
# 5) DataFrame generation
# ==============================================================

subjectColumns = ['name', 'age', 'sex', 'handedness',
                  'experiment', 'list', 'sentence',
                  'taskQuestion', 'trigger',
                  'expectedAnswer', 'participantAnswer', 'answer']

wordColumns = ["word" + str(i) for i in range(1, longestSentence + 1)]
myColumns = subjectColumns + wordColumns

results = pd.DataFrame(index=range(totalTrials), columns=myColumns)


# ==============================================================
# 6) GUI
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


# ==============================================================
# Window creation
# ==============================================================

win = visual.Window(
    screen=1,
    size=[1919.5, 1079.5],
    fullscr=False,
    color=backgroundColor,
    monitor='testMonitor'
)


# ==============================================================
# Initial instruction
# ==============================================================

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

listenbutton(9)

for frameN in range(instructionOff - 1):
    win.flip()
win.flip()

recentCorrectResponses = 0
totalCorrectResponses = 0
trialsSinceLastBreak = 0


# ==============================================================
# ### NEW: 카운터 (practice / real 분리)
# ==============================================================

practice_counter = 0
practice_correct_counter = 0
block_real_done = {1: 0, 2: 0, 3: 0}

# ==============================================================
# ### NEW: subblock 성과(방금 끝난 subblock에서만) 카운터  ✅
# - "맞췄다"는 '질문이 실제로 나온 trial'에서 answer==1인 경우만 카운트
# ==============================================================

subblock_question_total = 0
subblock_question_correct = 0
active_real_subblock = None  # real subblock 추적용


# ==============================================================
# ======================= PART 2 ==============================
# ==============================================================

prev_block = None
last_task_block = 0   # ### FIX: break row(block=0)에서도 마지막 real block 추적용
prev_subblock = None

# ### NEW: block instruction이 한 번씩만 뜨게 관리
shown_block_instruction = {1: False, 2: False, 3: False}

for trialIndex in range(totalTrials):

    pauseResponse = []
    responses = []
    event.clearEvents()

    curr_subblock = str(trialList[trialIndex].get("subblock", "")).lower()

    raw_block = trialList[trialIndex].get("block")
    try:
        curr_block = int(float(raw_block)) if raw_block not in (None, "", "nan", "NaN", "NA") else 0
    except:
        curr_block = 0

    if curr_block not in (0, 1, 2, 3):
        curr_block = 0

    sentence_text = trialList[trialIndex]['sentence']

    # ============================================================
    # ### NEW: practice / real 판별
    # ============================================================
    is_practice = (curr_subblock == "practice")
    is_break = (sentence_text == breakKeyword)
    is_real = (curr_block in (1, 2, 3) and (not is_practice) and (not is_break))

    # ============================================================
    # ### NEW: real subblock 바뀌면(혹시 break 없이 바뀌어도) subblock 성과 카운터 리셋
    # ============================================================
    if is_real:
        if active_real_subblock is None:
            active_real_subblock = curr_subblock
        elif curr_subblock != active_real_subblock:
            active_real_subblock = curr_subblock
            subblock_question_total = 0
            subblock_question_correct = 0

    # ============================================================
    # ### FIX: BLOCK instruction (CSV practice block=0 대응)
    # - practice 구간이 시작될 때, 다음 real block을 look-ahead로 찾아서 instruction 표시
    # ============================================================
    if is_practice and prev_subblock != "practice":
        upcoming_block = find_upcoming_real_block(trialIndex)
        if upcoming_block in (1, 2, 3) and (not shown_block_instruction[upcoming_block]):
            if upcoming_block == 1:
                instr_text = (
                    '블록 1: 문장 이해 실험입니다.\n\n'
                    '잠시 후 연습문항이 먼저 제시됩니다.\n'
                    '"예"(검지)를 눌러 연습문항을 시작하세요.'
                )
            elif upcoming_block == 2:
                instr_text = (
                    '블록 2: RSVP 실험입니다.\n\n'
                    '잠시 후 연습문항이 먼저 제시됩니다.\n'
                    '"예"(검지)를 눌러 연습문항을 시작하세요.'
                )
            else:
                instr_text = (
                    '블록 3: wh-질문 이해 실험입니다.\n\n'
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

            shown_block_instruction[upcoming_block] = True

    # ============================================================
    #  (A) ### FIX: BREAK LOGIC (practice/real 분리 + 남은 개수)
    #  - ✅ practice: 그대로
    #  - ✅ real: (1) 방금 끝난 subblock 성과 (2) 전체 real trial 남은 개수
    # ============================================================
    if sentence_text == breakKeyword:

        is_practice_end_break = (prev_subblock == "practice")

        if is_practice_end_break:
            msg = (
                '연습문항이 끝났습니다!\n\n'
                '지금까지 %i개의 문항 중 %i문항을 맞추셨습니다.\n\n'
                '본 실험을 시작할 준비가 되면\n'
                '"예"(검지)를 눌러주세요.'
            ) % (practice_counter, practice_correct_counter)

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

            # practice 카운터 reset
            practice_counter = 0
            practice_correct_counter = 0

        else:
            # ✅ 전체 real trial 진행률(모든 블록 통합)
            total_real_done = block_real_done[1] + block_real_done[2] + block_real_done[3]
            total_real_remaining = total_real_trial_total - total_real_done
            if total_real_remaining < 0:
                total_real_remaining = 0

            # ✅ real break 화면: subblock 성과 + 전체 남은 개수
            msg = (
                '방금 막 마친 subblock에서\n'
                '%i개 중 %i개를 맞추셨습니다.\n\n'
                '총 %i개 중에 %i개가 남았습니다.\n\n'
                '다음 문장을 읽을 준비가 되면\n'
                '움직이지 말고 눈을 깜박이지 않은 채로\n\n'
                '"예"(검지)를 누르세요.'
            ) % (
                subblock_question_total,
                subblock_question_correct,
                total_real_trial_total,
                total_real_remaining
            )

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

            # ✅ subblock 성과 카운터 reset (다음 subblock을 위해)
            subblock_question_total = 0
            subblock_question_correct = 0

        results.loc[trialIndex, 'sentence'] = 'break'
        prev_subblock = curr_subblock
        continue

    # 업데이트
    prev_subblock = curr_subblock


# ============================================================
# ======================= PART 3 — RSVP (원본 그대로) ==========
# ============================================================

    print(trialList[trialIndex]['sentence'])

    # ### FIX: last_task_block는 real trial에서만 업데이트
    if is_real:
        last_task_block = curr_block

    words = trialList[trialIndex]['sentence'].split()
    numWords = len(words)

    triggerList = range(
        int(trialList[trialIndex]['trigger']),
        int(trialList[trialIndex]['trigger']) + numWords
    )

    box = visual.Rect(win, width=boxWidth, height=boxHeight, units='deg')
    box.setPos((0, 0))
    box.setLineColor('red')
    box.setAutoDraw(True)

    # Fixation ON
    for frameN in range(fixationOn):
        win.flip()
        if frameN == 0:
            clock.reset()
    win.flip()

    # Fixation OFF
    for frameN in range(fixationOff - 2):
        win.flip()
    win.flip()

    # Context sentence (block 1 & 3)
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

            listenbutton(9)

            for frameN in range(FULL_SENTENCE_OFF - 1):
                win.flip()
            win.flip()

            try:
                box.setAutoDraw(True)
            except:
                pass


    # ============================================================
    # RSVP — 단어 단위 제시 (원본 트리거 로직 그대로)
    # ============================================================

    for wordIndex in range(numWords):

        stim = visual.TextStim(
            win, text=words[wordIndex],
            font=stimuliFont, units='deg',
            height=stimuliSize, color=stimuliColor,
            alignText='center'
        )
        stim.setPos((0, 0))

        # LAST WORD
        if wordIndex == (numWords - 1):

            for frameN in range(lastWordOn):
                stim.draw()
                win.flip()

                if frameN == 0:
                    clock.reset()

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

                    print(f"Trial {trialIndex}, Trigger: Combined Value = {combined_trigger_value}")
                    print("wordIndex", wordIndex)
                    print("frameN", frameN)

                    dp.DPxSetDoutValue(int(combined_trigger_value), 0xFFFFFF)
                    dp.DPxUpdateRegCache()

                if frameN == 10:
                    dp.DPxSetDoutValue(RGB2Trigger(black), 0xFFFFFF)
                    dp.DPxUpdateRegCache()

            win.flip()
            results.loc[trialIndex, wordIndex + len(subjectColumns)] = clock.getTime()

        # FIRST or MIDDLE WORD
        else:

            for frameN in range(wordOn):
                stim.draw()
                win.flip()

                if frameN == 0:
                    clock.reset()

                if frameN < 10:

                    if wordIndex == 0:  # first word
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

                    else:  # middle words
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

                    print(f"Trial {trialIndex}, Trigger: Combined Value = {combined_trigger_value}")
                    print("wordIndex", wordIndex)
                    print("frameN", frameN)

                    dp.DPxSetDoutValue(int(combined_trigger_value), 0xFFFFFF)
                    dp.DPxUpdateRegCache()

                if frameN == 10:
                    dp.DPxSetDoutValue(RGB2Trigger(black), 0xFFFFFF)
                    dp.DPxUpdateRegCache()

            win.flip()
            results.loc[trialIndex, wordIndex + len(subjectColumns)] = clock.getTime()

        # inter-word blank
        for frameN in range(wordOff - 2):
            win.flip()
        win.flip()

    box.setAutoDraw(False)

    # ============================================================
    # ======================= PART 4 ==============================
    # ============================================================

    option1 = str(trialList[trialIndex].get('option1', '')).strip()
    option2 = str(trialList[trialIndex].get('option2', '')).strip()

    # ### NEW: answer 기본값 (질문 없는 trial에서도 카운트 업데이트 안전)
    answer = 0

    # ### NEW: 이 trial에서 "질문이 실제로 나왔는지" 여부 (subblock 성과용) ✅
    had_question = False

    # Two-choice questions (block 1 & 3)
    if curr_block in (1, 3) and (option1 or option2):

        had_question = True

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

    # block2 taskQuestion
    else:
        if isinstance(trialList[trialIndex]['taskQuestion'], str) and len(trialList[trialIndex]['taskQuestion']) >= 4:

            had_question = True

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
    # ### NEW: practice / real 카운트 업데이트 (질문 여부와 무관하게 문장 단위로)
    # - practice는 practice끼리
    # - real은 block별 진행률로
    # ============================================================
    if is_practice:
        practice_counter += 1
        if answer == 1:
            practice_correct_counter += 1

    elif is_real:
        # ✅ 전체 진행률(남은 개수) = real 문장 trial 기준
        block_real_done[curr_block] += 1

        # ✅ subblock 성과 = "질문이 실제로 나온 trial"만 카운트
        if had_question:
            subblock_question_total += 1
            if answer == 1:
                subblock_question_correct += 1

    # ============================================================
    # Save results
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

    # Save results of option (원본 유지)
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

    participantName = participantInfo[0].replace(" ", "")
    filename = 'results.' + participantName + '.csv'
    results.to_csv(filename, encoding='utf-8-sig')

    # ============================================================
    # ======================= PART 5 ==============================
    # ============================================================

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

    listenbutton(9)

    for frameN in range(taskQuestionOff - 1):
        win.flip()
    win.flip()

# ============================================================
# ======================= PART 6 ==============================
# ============================================================

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

event.waitKeys()

participantName = participantInfo[0].replace(" ", "")
filename = 'results.' + participantName + '.csv'
results.to_csv(filename, encoding='utf-8-sig')

win.close()
core.quit()
dp.DPxClose()
