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
# ======================= PART 2 ==============================
# ==============================================================

prev_block = None
last_task_block = None

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

    if curr_block not in (1, 2, 3):
        curr_block = 0

    sentence_text = trialList[trialIndex]['sentence']

    # ============================================================
    #  (A) BREAK LOGIC
    # ============================================================
    if sentence_text == breakKeyword:

        is_practice_end_break = (prev_subblock == "practice")

        if is_practice_end_break:
            msg = (
                '연습문항이 끝났습니다!\n\n'
                '지금까지 %i개의 문항 중 %i문항을 맞추셨습니다.\n\n'
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

            recentCorrectResponses = 0
            trialsSinceLastBreak = 0

        else:
            msg = (
                '지금까지 %i개의 문장을 완료했고,\n'
                '앞으로 %i개의 문장이 남았습니다.\n\n'
                '"예"(검지)를 누르세요.'
            ) % (recentCorrectResponses, (totalTrials - trialIndex))

            stim = visual.TextStim(
                win, text=msg,
                font=instructionsFont, units='deg',
                color=instructionColor, height=0.8,
                alignText='center', wrapWidth=30
            )

            print("break window")

            stim.draw()
            win.flip()

            core.wait(TIME_WAIT_BREAK)
            listenbutton(9)

            recentCorrectResponses = 0
            trialsSinceLastBreak = 0

        results.loc[trialIndex, 'sentence'] = 'break'
        prev_subblock = curr_subblock
        continue


    # ============================================================
    # BLOCK Instruction
    # ============================================================
    if curr_block in (1, 2, 3) and curr_block != prev_block:
        if curr_subblock == "practice":
            if curr_block == 1:
                instr_text = (
                    '블록 1: 문장 이해 실험입니다.\n'
                    '"예"를 누르면 연습문항이 시작됩니다.'
                )
            elif curr_block == 2:
                instr_text = (
                    '블록 2: RSVP 실험입니다.\n'
                    '"예"를 누르면 연습문항이 시작됩니다.'
                )
            else:
                instr_text = (
                    '블록 3: wh-질문 이해 실험입니다.\n'
                    '"예"를 누르면 연습문항이 시작됩니다.'
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

    prev_subblock = curr_subblock


# ============================================================
# ======================= PART 3 — RSVP (FIXED) ===============
# ============================================================

    print(trialList[trialIndex]['sentence'])

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
    # *** FIXED RSVP — single correct loop ***
    # ============================================================

    for wordIndex in range(numWords):

        stim = visual.TextStim(
            win, text=words[wordIndex],
            font=stimuliFont, units='deg',
            height=stimuliSize, color=stimuliColor,
            alignText='center'
        )
        stim.setPos((0, 0))

        # --------------------------------------------------------
        # LAST WORD
        # --------------------------------------------------------
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


        # --------------------------------------------------------
        # FIRST or MIDDLE WORD
        # --------------------------------------------------------
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

    # ------------------------------------------------------------
    # PART 4 continues…
    # ------------------------------------------------------------
