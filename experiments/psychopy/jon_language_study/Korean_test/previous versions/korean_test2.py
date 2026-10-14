import os, sys
import pandas as pd
from psychopy import core, visual, event, parallel, data, monitors, gui

from pypixxlib import _libdpx as dp

from experiments.psychopy.general.utilities import *

import random

# --- 질문 표시 정책(전역 설정) ---
ASK_CHOICE_DEFAULT = None   # None이면 CSV/기존 규칙 따름. True/False로 전역 강제 가능
ASK_CHOICE_PROB = None      # 예: 0.3 → CSV 플래그 없을 때 30%만 질문
SEED_PER_PARTICIPANT = True # 참가자+trial 기반 재현 가능한 난수

# ---------- 유틸 함수들 ----------
def _to_bool_or_none(v):
    # "1", 1, "true", "True" -> True / "0", 0, "false", "False" -> False / 그 외 -> None
    if isinstance(v, str):
        s = v.strip().lower()
        if s in ("1", "true", "t", "y", "yes"):
            return True
        if s in ("0", "false", "f", "n", "no"):
            return False
    elif isinstance(v, (int, float)):
        if v == 1:
            return True
        if v == 0:
            return False
    return None

def _stable_rand01(participant_name, trial_index):
    # 참가자+trial 기반의 재현 가능한 난수 (MEG 재실행 시 동일 동작 보장)
    base = (participant_name or "anon") + f"::{trial_index}"
    return (hash(base) % 10_000_000) / 10_000_000.0

def _clean_text(v):
    """
    CSV에서 온 값이 None/'none'/'NaN'/'na'/빈칸인 경우 빈문자열로 정리.
    화면에 'None'/'nan'이 찍히는 걸 방지.
    """
    if v is None:
        return ''
    s = str(v).strip()
    return '' if s.lower() in ('none', 'nan', 'na', '') else s
# -----------------------------------

def should_ask_choice(trial, curr_block, participant_name, trial_index):
    """
    블록1/3의 2지선다 질문 표시 여부 결정:
      1) 전역 강제(ASK_CHOICE_DEFAULT)
      2) CSV ask_choice
      3) 확률 정책(ASK_CHOICE_PROB)
      4) 기존 규칙: (블록 1/3) and (option1 and option2)  ← 안전하게 둘 다 텍스트 있을 때만
    """
    # 1) 전역 강제
    if isinstance(ASK_CHOICE_DEFAULT, bool):
        return ASK_CHOICE_DEFAULT

    # 2) CSV 플래그
    ask_flag = _to_bool_or_none(trial.get('ask_choice')) if 'ask_choice' in trial else None
    if ask_flag is not None:
        return ask_flag

    # 3) 확률 정책
    if isinstance(ASK_CHOICE_PROB, (int, float)) and 0.0 <= ASK_CHOICE_PROB <= 1.0:
        r = _stable_rand01(participant_name, trial_index) if SEED_PER_PARTICIPANT else random.random()
        return (r < ASK_CHOICE_PROB)

    # 4) 기존 규칙(후방호환) - 옵션 둘 다 실제 텍스트가 있어야 질문 표시
    option1 = _clean_text(trial.get('option1', ''))
    option2 = _clean_text(trial.get('option2', ''))
    return (curr_block in (1, 3)) and (option1 and option2)

def should_ask_comp(trial, curr_block):
    """
    블록2의 컴프리헨션 질문 표시 여부:
      1) CSV ask_comp
      2) 기존 규칙: block==2 and taskQuestion 길이 >= 4
    """
    ask_flag = _to_bool_or_none(trial.get('ask_comp')) if 'ask_comp' in trial else None
    if ask_flag is not None:
        return ask_flag
    tq = trial.get('taskQuestion')
    return (curr_block == 2) and (isinstance(tq, str) and len(tq) >= 4)

# Setup the connection with the Vpixx systems and disable Pixel Mode

TIME_TO_RESET_BUTTON_BOX = 1.7
TIME_WAIT_BREAK = 0.5
# Define the RGB code for each channel on the KIT machine and their name
trigger = [[4, 0, 0], [16, 0, 0], [64, 0, 0], [0, 1, 0], [0, 4, 0], [0, 16, 0], [0, 64, 0], [0, 0, 1]]
channel_names  = ['224', '225', '226', '227', '228', '229', '230', '231']
black = [0, 0, 0]

RESPONSE_SELECTION = {
    "right box": ["red", "yellow"],
}

def RGB2Trigger(color):
    # helper function determines expected trigger from a given RGB 255 colour value
    return int((color[2] << 16) + (color[1] << 8) + color[0])  # dhk

dp.DPxOpen()
dp.DPxDisableDoutPixelMode()
dp.DPxWriteRegCache()
dp.DPxSetDoutValue(RGB2Trigger(black), 0xFFFFFF)
dp.DPxUpdateRegCache()

# Responsebox
responses = []

SCREEN_NUMBER = 2
trialList = data.importConditions('korean_test2.csv')

clock = core.Clock()

backgroundColor = 'black'
instructionsFont = 'Malgun Gothic'
stimuliFont = 'Malgun Gothic'
stimuliColor = 'gold' #rgb(255, 215, 0)
stimuliUnits = 'deg'
stimuliSize = 2

wordOn = 38  # 350ms
wordOff = 20 # 200ms
lastWordOn = 38

boxHeight = stimuliSize + 1.5
boxWidth = 17

# >>> PATCH 1) Block 1/3용 context(통문장) 표시 파라미터 & 블록 상태
FULL_SENTENCE_HEIGHT = 1.5    # context 폰트 크기
FULL_SENTENCE_OFF = wordOff   # context 후 간격
prev_block = None             # 블록 전환 감지용

longestWordCount = 0
longestWord = 'none'

totalTrials = len(trialList)
for trialIndex in range(totalTrials):
    words = trialList[trialIndex]['sentence'].split()
    for word in words:
        if len(word) > longestWordCount:
            longestWordCount = len(word)
            longestWord = word

print(longestWord)
print(longestWordCount)

fixationPoint = '****'
fixationOn = 60
fixationOff = wordOff
fixationColor = 'red'
fixationSize = stimuliSize
fixationUnits = stimuliUnits
fixationTrigger = 255

taskQuestionColor = 'red'
taskQuestionSize = 1.5
taskQuestionUnits = stimuliUnits
taskQuestionOff = wordOff

instructionColor = 'gold'
instructionSize = 1.5
INSTR_HEIGHT = 0.6
INSTR_WRAP   = 30
instructionUnits = stimuliUnits
instructionOff = wordOff

practiceCount = 0
breakKeyword = 'break'
breakColor = instructionColor
breakSize = instructionSize
breakUnits = instructionUnits
breakOff = wordOff

quitKey = 'escape'
responseYes = 'j'
startItem = 1

totalTrials = len(trialList)
totalQuestionCount = 0
totalBreakCount = 0

for trialIndex in range(totalTrials):
    if isinstance(trialList[trialIndex]['taskQuestion'], str) and len(trialList[trialIndex]['taskQuestion']) >= 4:
        totalQuestionCount += 1
    if trialList[trialIndex]['sentence'] == breakKeyword:
        totalBreakCount += 1

currentBreakCount = 0
totalCorrectResponses = 0
recentCorrectResponses = 0
trialsSinceLastBreak = 0

longestSentence = 0
for trialIndex in range(totalTrials):
    numWords = len(trialList[trialIndex]['sentence'].split())
    if numWords > longestSentence:
        longestSentence = numWords

subjectColumns = ['name', 'age', 'sex', 'handedness', 'experiment', 'list', 'sentence', 'taskQuestion', 'trigger', 'expectedAnswer', 'participantAnswer', 'answer']
wordColumns = ["word" + str(i) for i in range(1, longestSentence + 1)]
myColumns = subjectColumns + wordColumns
results = pd.DataFrame(index=range(totalTrials), columns=myColumns)

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

win = visual.Window(screen =1, size=[1919.5, 1079.5], fullscr=False, color=backgroundColor, monitor='testMonitor')

prev_block = None
last_task_block = None  # 마지막으로 수행한 블록(1/2/3)

# Loop for each trial
for trialIndex in range(startItem - 1, totalTrials):

    pauseResponse = []
    responses = []
    event.clearEvents()

    if trialList[trialIndex]['sentence'] == breakKeyword:
        # Handling breaks
        event.clearEvents()
        currentBreakCount += 1
        completedTrials = trialIndex + 1 - practiceCount - currentBreakCount
        remainingTrials = (totalTrials - totalBreakCount - practiceCount) - completedTrials

        # ---- 점수 표시는 블록 1/3일 때만 ----
        if last_task_block in (1, 3):
            msg = (
                '%i개의 문항 중에서 %i문항을 맞혔습니다.\n\n'
                '지금까지 %i개의 문장을 완료했고, 앞으로 %i개의 문장이 남았습니다. \n\n'
                '다음 문장을 읽을 준비가 되면 움직이지 말고 눈을 깜박이지 않은 채로 \n\n'
                '"예"(검지)를 누르세요.'
            ) % (trialsSinceLastBreak, recentCorrectResponses, completedTrials, remainingTrials)
        else:
            msg = (
                '지금까지 %i개의 문장을 완료했고, 앞으로 %i개의 문장이 남았습니다. \n\n'
                '다음 문장을 읽을 준비가 되면 움직이지 말고 눈을 깜박이지 않은 채로 \n\n'
                '"예"(검지)를 누르세요.'
            ) % (completedTrials, remainingTrials)

        stim = visual.TextStim(
            win, text=msg, font=stimuliFont, units=instructionUnits,
            height=INSTR_HEIGHT*1.2, alignText='center', color=instructionColor,
            wrapWidth=INSTR_WRAP
        )
        print('break window')

        stim.setPos((0, 0))
        stim.draw()
        win.flip()
        print('listening to button')
        core.wait(TIME_WAIT_BREAK)
        # Pause until response
        listenbutton(9)

        core.wait(0.5)

        trialsSinceLastBreak = 0
        recentCorrectResponses = 0

        results.loc[trialIndex, 'name'] = participantInfo[0]
        results.loc[trialIndex, 'age'] = participantInfo[1]
        results.loc[trialIndex, 'sex'] = participantInfo[2]
        results.loc[trialIndex, 'handedness'] = participantInfo[3]
        results.loc[trialIndex, 'experiment'] = participantInfo[4]
        results.loc[trialIndex, 'list'] = participantInfo[5]
        results.loc[trialIndex, 'sentence'] = 'break'

        for frameN in range(breakOff - 1):
            win.flip()
        win.flip()

        continue

    # >>> PATCH 2) 블록 전환 감지 & 블록별 인스트럭션
    _raw_block = trialList[trialIndex].get('block')
    if _raw_block in (None, '', 'NA', 'NaN', 'nan'):
        curr_block = 2
    else:
        try:
            curr_block = int(float(_raw_block))
        except Exception:
            curr_block = 2

    if curr_block not in (1, 2, 3):
        curr_block = 2

    print('current block', curr_block)

    # 블록 전환 시에만 인스트럭션 표시
    if curr_block != prev_block:
        print('Curr block different than previous')
        if curr_block == 1:
            instr_text = (
                '이번 세션에서는 주어진 문장을 읽고, 그에 대한 질문에 답하시면 됩니다.'
            '\n\n\n'  
            '1. 우선 하나의 간단한 문장을 읽습니다.\n\n'
            '2. 문장을 읽은 후에는, 해당 문장의 내용과 관련된 간단한 질문이 제시됩니다.\n\n'
            '3. 질문에 대한 답으로 두 가지 "보기"가 주어집니다. 그 중 가장 알맞는 답을 선택하면 됩니다.'
            '\n\n\n'
            '질문은 단어 단위로, 한 단어씩 제시됩니다.\n'
            '단어가 나오는 동안에는 눈을 깜박이거나 몸을 움직이지 마세요.\n'
            '문장이 끝난 뒤나 질문에 답할 때는 눈을 깜박이셔도 괜찮습니다.'
            '\n\n'
            '본 실험을 시작할 준비가 됐다면 움직이지 말고, 눈을 깜박이지 않은 채로 "예"(검지)를 누르세요.'
        )
        elif curr_block == 3:
            instr_text = (
                '이번 세션에서는 주어진 문장을 읽고, 그에 대한 질문에 답하시면 됩니다.'
            '\n\n\n'  
            '1. 우선 하나의 간단한 문장을 읽습니다.\n\n'
            '2. 문장을 읽은 후에는, 해당 문장의 내용과 관련된 간단한 질문이 제시됩니다.\n\n'
            '3. 질문에 대한 답으로 두 가지 "보기"가 주어집니다. 그 중 가장 알맞는 답을 선택하면 됩니다.'
            '\n\n\n'
            '질문은 단어 단위로, 한 단어씩 제시됩니다.\n'
            '단어가 나오는 동안에는 눈을 깜박이거나 몸을 움직이지 마세요.\n'
            '문장이 끝난 뒤나 질문에 답할 때는 눈을 깜박이셔도 괜찮습니다.'
            '\n\n'
            '본 실험을 시작할 준비가 됐다면 움직이지 말고, 눈을 깜박이지 않은 채로 "예"(검지)를 누르세요.'
            )
        else:
            instr_text = (
                '이번 세션에서는 주어진 문장을 읽고, 그에 대한 질문에 답하시면 됩니다. \n\n'
                '문장은 단어 단위로, 한 단어씩 제시됩니다. 단어가 나오는 동안에는 눈을 깜박이거나 몸을 움직이지 마세요.\n\n'
                '문장이 제시된 후에 때떄로 \n\n'
                '문장이 끝난 뒤나 질문에 답할 때는 눈을 깜박이셔도 괜찮습니다.\n\n'
                '본 실험을 시작할 준비가 됐다면 움직이지 말고, 눈을 깜빡이지 않은 채로 "예"(검지)를 누르세요.'
            )

        stim = visual.TextStim(
            win, text=instr_text, font=stimuliFont,
            units=instructionUnits, color=instructionColor,
            height=INSTR_HEIGHT, alignText='center',
            wrapWidth=INSTR_WRAP
        )
        stim.setPos((0, 0))
        stim.draw()
        win.flip()
        listenbutton(9)  # self-paced 진입
        prev_block = curr_block

    print(trialList[trialIndex]['sentence'])

    # 실제 문장 수행 trial이므로 마지막 블록 기록
    last_task_block = curr_block

    words = trialList[trialIndex]['sentence'].split()
    numWords = len(words)
    triggerList = range(int(trialList[trialIndex]['trigger']), int(trialList[trialIndex]['trigger']) + numWords)

    box = visual.Rect(win, width=boxWidth, height=boxHeight, units=fixationUnits)
    box.setPos((0, 0))
    box.setLineColor(fixationColor)
    box.setAutoDraw(True)

    for frameN in range(fixationOn):
        win.flip()
        if frameN == 0:
            clock.reset()
    win.flip()

    for frameN in range(fixationOff - 2):
        win.flip()
    win.flip()

    # >>> PATCH 3) Block 1/3: context(통문장) 먼저 self-paced 표시 (트리거 없음)
    if curr_block in (1, 3):
        option1 = _clean_text(trialList[trialIndex].get('option1', ''))
        option2 = _clean_text(trialList[trialIndex].get('option2', ''))
        # option이 있어야 2지선다 블록으로 간주
        if option1 and option2:
            try:
                box.setAutoDraw(False)  # 통문장 구간은 박스 숨김
            except:
                pass

            full_text = _clean_text(trialList[trialIndex].get('context', ''))
            full_stim = visual.TextStim(win, text=full_text, font=stimuliFont,
                                        units=stimuliUnits, height=FULL_SENTENCE_HEIGHT,
                                        color=taskQuestionColor, alignText='center', wrapWidth=30)
            full_stim.setPos((0, 0))
            full_stim.draw(); win.flip()

            # 참가자가 충분히 읽고 스스로 넘김
            listenbutton(9)

            # 짧은 간격
            for frameN in range(FULL_SENTENCE_OFF - 1):
                win.flip()
            win.flip()

            try:
                box.setAutoDraw(True)  # RSVP 시작 전 박스 복구
            except:
                pass

    # ----- 단어 RSVP (기존 트리거 로직 유지) -----
    for wordIndex in range(numWords):
        print(repr(words[wordIndex]))
        if event.getKeys(quitKey):
            participantName = participantInfo[0].replace(" ", "")
            filename = 'results.' + participantName + '.csv'
            results.to_csv(filename, encoding='utf-8-sig')
            win.close()
            core.quit()

        stim = visual.TextStim(win, text=words[wordIndex],  font=stimuliFont, units=stimuliUnits, height=stimuliSize, color=stimuliColor, alignText='center', anchorHoriz = 'center')
        stim.setPos((0, 0))

        if wordIndex == max(range(numWords)):
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

                    dp.DPxSetDoutValue(combined_trigger_value, 0xFFFFFF)
                    dp.DPxUpdateRegCache()
                    print('wordIndex', wordIndex)
                    print('frameN', frameN)

                if frameN == 10:
                    dp.DPxSetDoutValue(RGB2Trigger(black), 0xFFFFFF)
                    dp.DPxUpdateRegCache()

            win.flip()

            results.loc[trialIndex, wordIndex + len(subjectColumns)] = clock.getTime()
        else:
            for frameN in range(wordOn):
                stim.draw()
                win.flip()

                if wordIndex == 0:
                    if frameN < 10:
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
                        print(f"Trial {trialIndex}, Trigger: Combined Value = {combined_trigger_value}")

                        dp.DPxSetDoutValue(combined_trigger_value, 0xFFFFFF)
                        dp.DPxUpdateRegCache()
                        print('wordIndex', wordIndex)
                        print('frameN', frameN)
                    if frameN == 10:
                        dp.DPxSetDoutValue(RGB2Trigger(black), 0xFFFFFF)
                        dp.DPxUpdateRegCache()
                else:
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

                        dp.DPxSetDoutValue(combined_trigger_value, 0xFFFFFF)
                        dp.DPxUpdateRegCache()
                        print('wordIndex', wordIndex)
                        print('frameN', frameN)
                    if frameN == 10:
                        dp.DPxSetDoutValue(RGB2Trigger(black), 0xFFFFFF)
                        dp.DPxUpdateRegCache()

                if frameN == 0:
                    clock.reset()
            win.flip()
            results.loc[trialIndex, wordIndex + len(subjectColumns)] = clock.getTime()

        for frameN in range(wordOff - 2):
            win.flip()
        win.flip()

    box.setAutoDraw(False)

    # >>> PATCH 4) 질문 표시: CSV 플래그 기반 분기 (블록1/3 2지선다 vs 블록2 컴프 vs 생략)
    option1 = _clean_text(trialList[trialIndex].get('option1', ''))
    option2 = _clean_text(trialList[trialIndex].get('option2', ''))

    # show_choice/comp 계산 (ask_* 플래그 최우선)
    show_choice = should_ask_choice(trialList[trialIndex], curr_block, participantInfo[0], trialIndex)
    show_comp = should_ask_comp(trialList[trialIndex], curr_block)

    if show_choice:
        # === 블록1/3: 2지선다 화면 + getbuttonColor ===
        event.clearEvents()

        question_text = f"① {option1}\n\n② {option2}\n\n"
        stim = visual.TextStim(
            win, text=question_text, font=stimuliFont, units=stimuliUnits,
            height=1.5, color=taskQuestionColor, alignText='center', wrapWidth=30
        )
        stim.setPos((0, -2.5))
        stim.draw()
        win.flip()

        response = getbuttonColor(RESPONSE_SELECTION)  # 9=red(①), 7=yellow(②)
        responses.append(response)

        stim = visual.TextStim(
            win, text='모든 버튼에서 손가락을 떼주세요.\n\n',
            font=stimuliFont, units=stimuliUnits, height=1.5,
            color=taskQuestionColor, alignText='center', wrapWidth=30
        )
        stim.setPos((0, -1.5))
        stim.draw()
        win.flip()
        core.wait(TIME_TO_RESET_BUTTON_BOX)

        if responses[-1] == quitKey:
            participantName = participantInfo[0].replace(" ", "")
            filename = 'results.' + participantName + '.csv'
            results.to_csv(filename, encoding='utf-8-sig')
            win.close()
            core.quit()

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

    elif show_comp:
        # === 블록2: taskQuestion + red/yellow ===
        event.clearEvents()

        stim = visual.TextStim(
            win, text=trialList[trialIndex]['taskQuestion'], font=stimuliFont,
            units=stimuliUnits, height=1.5, color=taskQuestionColor,
            alignText='center', wrapWidth=30
        )
        stim.setPos((0, 0))
        stim.draw()
        win.flip()

        response = getbuttonColor(RESPONSE_SELECTION)  # listen to a button
        responses.append(response)

        stim = visual.TextStim(
            win, text='모든 버튼에서 손가락을 떼주세요.\n\n',
            font=stimuliFont, units=stimuliUnits, height=1,
            color=taskQuestionColor, alignText='center', wrapWidth=30
        )
        stim.setPos((0, -2.5))
        stim.draw()
        win.flip()
        core.wait(TIME_TO_RESET_BUTTON_BOX)

        if responses[-1] == quitKey:
            participantName = participantInfo[0].replace(" ", "")
            filename = 'results.' + participantName + '.csv'
            results.to_csv(filename, encoding='utf-8-sig')
            win.close()
            core.quit()

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

    else:
        # === 질문 생략(바로 안내/대기 화면으로) ===
        trialsSinceLastBreak += 1
        answer = ''
        responses = []
        for frameN in range(taskQuestionOff - 1):
            win.flip()
        win.flip()

    results.loc[trialIndex, 'name'] = participantInfo[0]
    results.loc[trialIndex, 'age'] = participantInfo[1]
    results.loc[trialIndex, 'sex'] = participantInfo[2]
    results.loc[trialIndex, 'handedness'] = participantInfo[3]
    results.loc[trialIndex, 'experiment'] = participantInfo[4]
    results.loc[trialIndex, 'list'] = participantInfo[5]
    results.loc[trialIndex, 'sentence'] = trialList[trialIndex]['sentence']
    results.loc[trialIndex, 'taskQuestion'] = trialList[trialIndex]['taskQuestion']
    results.loc[trialIndex, 'trigger'] = trialList[trialIndex]['trigger']

    # (선택) 옵션 로그도 저장
    results.loc[trialIndex, 'option1'] = option1
    results.loc[trialIndex, 'option2'] = option2

    if show_choice:
        results.loc[trialIndex, 'expectedAnswer'] = trialList[trialIndex]['correctAnswer']
        results.loc[trialIndex, 'participantAnswer'] = responses[-1][1] if responses else ''
        results.loc[trialIndex, 'answer'] = answer
    elif show_comp:
        results.loc[trialIndex, 'expectedAnswer'] = trialList[trialIndex]['correctAnswer']
        results.loc[trialIndex, 'participantAnswer'] = responses[-1][1] if responses else ''
        results.loc[trialIndex, 'answer'] = answer
    else:
        results.loc[trialIndex, 'expectedAnswer'] = ''
        results.loc[trialIndex, 'participantAnswer'] = ''
        results.loc[trialIndex, 'answer'] = ''

    # 저장
    participantName = participantInfo[0].replace(" ", "")
    filename = 'results.' + participantName + '.csv'
    results.to_csv(filename, encoding='utf-8-sig')

    event.clearEvents()
    stim = visual.TextStim(win,
                           text='지금은 편하게 눈을 깜빡이셔도 괜찮습니다.\n\n' 
                                '다음 문장을 눈 깜빡임없이 읽을 준비가 되면 \n\n'
                                '"예"(검지)를 누르세요.\n\n',
                           font=stimuliFont, units=stimuliUnits, height=1, color=stimuliColor, wrapWidth=30, alignText='center')
    stim.setPos((0, -1.5))
    stim.draw()
    win.flip()

    listenbutton(9)

    for frameN in range(taskQuestionOff - 1):
        win.flip()
    win.flip()

event.clearEvents()
stim = visual.TextStim(win,
                       text='실험을 모두 마치셨습니다.\n\n' 
                            '잠시만 움직이지 말아주세요.\n'
                            '약 30초 동안 마지막 기록을 진행합니다.\n\n'
                            '총 %i개의 문장을 읽었고, \n'
                            '%i개의 질문 중에 %i개를 맞추셨습니다.'  % (
                       (totalTrials - totalBreakCount - practiceCount), totalCorrectResponses, totalQuestionCount),
                       font=stimuliFont, units=stimuliUnits, color=stimuliColor, height=INSTR_HEIGHT, alignText='center', wrapWidth=INSTR_WRAP)

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
