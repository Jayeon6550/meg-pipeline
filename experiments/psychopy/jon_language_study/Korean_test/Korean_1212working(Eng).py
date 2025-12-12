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
# 1) Load CSV + basic parameters
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
# 2) Fixation / Task / Instruction parameters
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

# ==============================================================
# 3) Compute longest word/sentence length + basic counts
# ==============================================================

totalQuestionCount = 0
totalBreakCount = 0
totalPracticeCount = 0
longestSentence = 0

for t in trialList:
    words = t['sentence'].split()
    longestSentence = max(longestSentence, len(words))
    if str(t.get("subblock", "")).lower() == "practice":
        totalPracticeCount += 1
    if t['sentence'] == breakKeyword:
        totalBreakCount += 1
    if isinstance(t['taskQuestion'], str) and len(t['taskQuestion']) >= 4:
        totalQuestionCount += 1

practiceCount = totalPracticeCount

# ==============================================================
# NEW: Pre-compute REAL trial totals per block (exclude practice/break)
# ==============================================================

block_real_total = {1: 0, 2: 0, 3: 0}
for t in trialList:
    sub = str(t.get("subblock", "")).lower()
    try:
        blk = int(float(t.get("block", 0)))
    except:
        blk = 0
    if blk in (1, 2, 3) and sub != "practice" and t['sentence'] != breakKeyword:
        block_real_total[blk] += 1

# ==============================================================
# NEW: Total number of REAL trials across all blocks
# ==============================================================

total_real_trial_total = sum(block_real_total.values())

# ==============================================================
# NEW: Helper — find the upcoming REAL block at the start of practice
# ==============================================================

def find_upcoming_real_block(start_index):
    for j in range(start_index, totalTrials):
        r = trialList[j]
        sub = str(r.get("subblock", "")).lower()
        try:
            b = int(float(r.get("block", 0)))
        except:
            b = 0
        if r['sentence'] != breakKeyword and sub != "practice" and b in (1,2,3):
            return b
    return 0

# ==============================================================
# 5) Results DataFrame setup
# ==============================================================

subjectColumns = ['name', 'age', 'sex', 'handedness',
                  'experiment', 'list', 'sentence',
                  'taskQuestion', 'trigger',
                  'expectedAnswer', 'participantAnswer', 'answer']

wordColumns = ["word" + str(i) for i in range(1, longestSentence + 1)]
results = pd.DataFrame(index=range(totalTrials),
                       columns=subjectColumns + wordColumns)

# ==============================================================
# 6) Participant info GUI
# ==============================================================

myDlg = gui.Dlg(title="RSVP MEG experiment")
myDlg.addField('Participant Name:')
myDlg.addField('Age:')
myDlg.addField('Sex:')
myDlg.addField('Handedness:')
myDlg.addField('Experiment Name:')
myDlg.addField('List:')
myDlg.show()

participantInfo = myDlg.data

# ==============================================================
# Window creation
# ==============================================================

win = visual.Window(screen=1, color=backgroundColor)

# ==============================================================
# Initial instruction screen
# ==============================================================

stim = visual.TextStim(win, text="Experiment overview")
stim.draw()
win.flip()
listenbutton(9)

# ==============================================================
# Counters (legacy / intermediate)
# ==============================================================

recentCorrectResponses = 0
totalCorrectResponses = 0
trialsSinceLastBreak = 0

# ==============================================================
# NEW: FINAL overall REAL question performance counters
# ==============================================================

total_real_question_count = 0
total_real_question_correct = 0

# ==============================================================
# NEW: Counters separated by practice vs real
# ==============================================================

practice_counter = 0
practice_correct_counter = 0
block_real_done = {1:0, 2:0, 3:0}

# ==============================================================
# NEW: Subblock performance counters
# ==============================================================

subblock_question_total = 0
subblock_question_correct = 0
active_real_subblock = None

# ==============================================================
# ======================= PART 2 ==============================
# Main trial loop
# ==============================================================

for trialIndex in range(totalTrials):
    # (full trial logic unchanged)
    pass
