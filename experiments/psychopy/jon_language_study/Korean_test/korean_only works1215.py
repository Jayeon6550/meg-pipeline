import os, sys
import pandas as pd
from psychopy import core, visual, event, parallel, data, monitors, gui

from pypixxlib import _libdpx as dp

from experiments.psychopy.general.utilities import *


# Setup the connection with the Vpixx systems and disable Pixel Mode

TIME_TO_RESET_BUTTON_BOX =1.7
TIME_WAIT_BREAK = 0.5
# Define the RGB code for each channel on the KIT machine and their name
trigger = [[4, 0, 0], [16, 0, 0], [64, 0, 0], [0, 1, 0], [0, 4, 0], [0, 16, 0], [0, 64, 0], [0, 0, 1]]
channel_names  = ['224', '225', '226', '227', '228', '229', '230', '231']
black = [0, 0, 0]

RESPONSE_SELECTION = {
    "right box": ["red", "yellow"],
}


RESPONSE_PASS = {
    "right box": ["red"],
}

def RGB2Trigger(color):
    # helper function determines expected trigger from a given RGB 255 colour value
    # operates by converting individual colours into binary strings and stitching them together
    # and interpreting the result as an integer

    # return triggerVal
    return int((color[2] << 16) + (color[1] << 8) + color[0])  # dhk


dp.DPxOpen()
dp.DPxDisableDoutPixelMode()
dp.DPxWriteRegCache()
dp.DPxSetDoutValue(RGB2Trigger(black), 0xFFFFFF)
dp.DPxUpdateRegCache()

# Responsebox

# When you need to use it add thisline
responses = [] # Add this at the beginning of your script
#Copy/Paste these two lines everytime the participant should input a button
#response = getbutton() #listen to a button
#responses.append(response) #everytime we get a response we add it to the table

# Save the responses in a variable responses = [] then responses.append(response) then save it to your .csv

SCREEN_NUMBER = 2
#Try 1 or 2 as screen_number
#SCREEN_NUMBER = 1

trialList = data.importConditions('korean_test2.csv')

#mon = monitors.Monitor('BenQ24', width=53, distance=100)
#port = parallel.ParallelPort(address=0xD010)
clock = core.Clock()

backgroundColor = 'black'
instructionsFont = 'Malgun Gothic'
stimuliFont = 'Malgun Gothic'
stimuliColor = 'gold' #rgb(255, 215, 0)
stimuliUnits = 'deg'
stimuliSize = 2
wordOn = 38 #42 #350ms
wordOff = 20 #24 #200ms
lastWordOn = 38 #132  #1100

boxHeight = stimuliSize + 1.5
boxWidth = 15

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

#fixationPoint = '****'
fixationOn = 60
fixationOff = wordOff
fixationColor = 'red'
fixationSize = stimuliSize
fixationUnits = stimuliUnits
#fixationTrigger = 255

taskQuestionColor = 'red'
taskQuestionSize = 1.5
taskQuestionUnits = stimuliUnits
taskQuestionOff = wordOff

instructionColor = 'gold'
instructionSize = 1.5
INSTR_HEIGHT = 0.6      # 글자 크기 줄이기 (기존 0.9 → 0.6)
INSTR_WRAP   = 30        # 줄바꿈 폭 좁히기 (기존 30 → 22)
instructionUnits = stimuliUnits
instructionOff = wordOff

practiceCount = 5 #
breakKeyword = 'break'
breakColor = instructionColor
breakSize = instructionSize
breakUnits = instructionUnits
breakOff = wordOff

quitKey = 'escape'
#responseYes = 'j'
#responseNo = 'f'
#correctTrigger = 251
#incorrectTrigger = 250

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

win = visual.Window(screen =1, size=[1919.5, 1079.5], fullscr=False, color=backgroundColor, monitor='testMonitor')  # Set the border color to black)


instructions_text = (
        "실험 개요"
)

stim = visual.TextStim(win,
                        text = instructions_text,
                       font= instructionsFont, languageStyle='Arabic', units=breakUnits, color=instructionColor, height= 0.8, alignText= 'center',  wrapWidth= 30)
stim.setPos((0, 0))
stim.draw()
win.flip()


getbuttonColor(RESPONSE_PASS)



for frameN in range(instructionOff - 1):
    win.flip()
win.flip()

prev_block = None
last_task_block = None  # <<< 마지막으로 수행한 블록(1/2/3)을 기록하여 break 화면에서 점수 표시 여부 결정

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
            # 블록 2: 점수 라인 없이 깔끔한 안내만
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
        getbuttonColor(RESPONSE_PASS)

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


    # >>> PATCH 2) 블록 전환 감지 & 블록별 인스트럭션  (REPLACEMENT)
    # block 값 안전 변환 (빈칸/None/"NaN" 등은 2로 처리)
    _raw_block = trialList[trialIndex].get('block')
    if _raw_block in (None, '', 'NA', 'NaN', 'nan'):
        curr_block = 2
    else:
        try:
            curr_block = int(float(_raw_block))
        except Exception:
            curr_block = 2

    # 허용 범위 이외 값 방지
    if curr_block not in (1, 2, 3):
        curr_block = 2


    print('current block', curr_block)

    # 블록 전환 시에만 인스트럭션 표시
    if curr_block != prev_block:
        currentBreakCount = 0  # ★ PATCH: 새로운 block에서는 practice break 카운트를 초기화
        print('Curr block different than previous')
        if curr_block == 1:
            instr_text = (
                '이번 세션에서는 주어진 문장을 읽고, 그 내용에 대한 질문에 답하시면 됩니다.'
            '\n\n\n'  
            '1. 우선 하나의 간단한 문장을 읽습니다.\n\n'
            '2. 문장을 읽은 후, 질문을 볼 준비가 되면 "예"(검지)버튼을 누릅니다.\n\n'
            '3. 이어서 해당 문장의 내용을 이해했는지 확인하는 질문이 제시됩니다.\n'
            '   질문은 단어 단위로 한 단어씩 제시됩니다. 이때는 눈을 깜빡이거나 몸을 움직이지 마세요.\n\n'
            '4. 질문 제시가 끝나면 두 가지 "보기"가 나오며, [1번=검지],[2번=중지]로 응답합니다.'
            '\n\n\n'
            '질문이 제시되는 동안에는 눈을 깜빡이지 않도록 해주세요.\n'
            '그 외의 구간에서는 자유롭게 깜빡이셔도 괜찮습니다.'
            '\n\n'
            '실험을 시작할 준비가 되셨다면, "예"(검지)를 눌러주세요.'
        )
        elif curr_block == 3:
            instr_text = (
                '이번 세션에서는 주어진 문장을 읽고, 그 내용에 대한 질문에 답하시면 됩니다.'
            '\n\n\n'  
            '1. 우선 하나의 간단한 문장을 읽습니다.\n\n'
            '2. 문장을 읽은 후, 질문을 볼 준비가 되면 "예"(검지)버튼을 누릅니다.\n\n'
            '3. 이어서 해당 문장의 내용을 이해했는지 확인하는 질문이 제시됩니다.\n'
            '   질문은 단어 단위로 한 단어씩 제시됩니다. 이때는 눈을 깜빡이거나 몸을 움직이지 마세요.\n\n'
            '4. 질문 제시가 끝나면 두 가지 "보기"가 나오며, [1번=검지],[2번=중지]로 응답합니다.'
            '\n\n\n'
            '질문이 제시되는 동안에는 눈을 깜빡이지 않도록 해주세요.\n'
            '그 외의 구간에서는 자유롭게 깜빡이셔도 괜찮습니다.'
            '\n\n'
            '실험을 시작할 준비가 되셨다면, "예"(검지)를 눌러주세요.'
            )
        else:
            # curr_block == 2
            instr_text = (
                '이번 세션에서는 주어진 문장을 읽고, 그에 대한 질문에 답하시면 됩니다. \n\n'
                '문장은 단어 단위로, 한 단어씩 제시됩니다. 이때는 눈을 깜박이거나 몸을 움직이지 마세요.\n\n'
                '그 외의 구간에서는 자유롭게 깜빡이셔도 괜찮습니다.'
                '\n\n'
                '실험을 시작할 준비가 되셨다면, "예"(검지)를 누르세요.'
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
        getbuttonColor(RESPONSE_PASS)  # self-paced 진입
        prev_block = curr_block

    print(trialList[trialIndex]['sentence'])

    # 이 trial은 실제 문장 수행 trial이므로 마지막 블록 기록 (break가 아닌 경우에만 도달)
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
        option1 = str(trialList[trialIndex].get('option1', '')).strip()
        option2 = str(trialList[trialIndex].get('option2', '')).strip()
        # option이 있어야 2지선다 블록으로 간주
        if option1 or option2:
            try:
                box.setAutoDraw(False)  # 통문장 구간은 박스 숨김
            except:
                pass

            full_text = str(trialList[trialIndex].get('context', '')).strip()
            full_stim = visual.TextStim(win, text=full_text, font=stimuliFont,
                                        units=stimuliUnits, height=FULL_SENTENCE_HEIGHT,
                                        color=taskQuestionColor, alignText='center', wrapWidth=30)
            full_stim.setPos((0, 0))
            full_stim.draw(); win.flip()

            # 참가자가 충분히 읽고 스스로 넘김
            getbuttonColor(RESPONSE_PASS)

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
                    # Debugging log: Print the calculated combined value
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

                        # Debugging log: Print the calculated combined value
                        dp.DPxSetDoutValue(RGB2Trigger(black), 0xFFFFFF)
                        dp.DPxUpdateRegCache()
                else:
                    # Trigger logic for the rest of the words
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

                        # Debugging log: Print the calculated combined value
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

    # >>> PATCH 4) 질문 표시: Block 1/3(2지선다) vs 기존(taskQuestion)
    option1 = str(trialList[trialIndex].get('option1', '')).strip()
    option2 = str(trialList[trialIndex].get('option2', '')).strip()

    if curr_block in (1, 3) and (option1 or option2):
        event.clearEvents()

        question_text = f"① {option1}\n\n② {option2}\n\n"
        stim = visual.TextStim(win, text=question_text, font=stimuliFont, units=stimuliUnits,
                               height=1.5, color=taskQuestionColor, alignText='center', wrapWidth=30)
        stim.setPos((0, -2.5))
        stim.draw()
        win.flip()

        response = getbuttonColor(RESPONSE_SELECTION)  # 9=red(①), 7=yellow(②)
        responses.append(response)

        stim = visual.TextStim(win, text='모든 버튼에서 손가락을 떼주세요.\n\n',
                               font= stimuliFont, units= stimuliUnits, height=1.5, color=taskQuestionColor, alignText='center' ,wrapWidth= 30)
        stim.setPos((0,-1.5))
        stim.draw()
        win.flip()
        core.wait(TIME_TO_RESET_BUTTON_BOX)

        if responses[-1] == quitKey:
            participantName = participantInfo[0].replace(" ", "")
            filename = 'results.' + participantName + '.csv'
            results.to_csv(filename, encoding='utf-8-sig')
            win.close()
            core.quit()

        if trialList[trialIndex]['correctAnswer'] == "red" and responses[-1]==('right box', 'red'):
            recentCorrectResponses += 1
            totalCorrectResponses += 1
            answer = 1
        elif trialList[trialIndex]['correctAnswer'] == "yellow" and responses[-1]==('right box', 'yellow'):
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
        # ----- 기존 taskQuestion 경로(블록2 또는 옵션 없음) 그대로 유지 -----
        if isinstance(trialList[trialIndex]['taskQuestion'], str) and len(trialList[trialIndex]['taskQuestion']) >= 4:
            event.clearEvents()

            stim = visual.TextStim(win, text=trialList[trialIndex]['taskQuestion'], font= stimuliFont, units= stimuliUnits, height=1.5, color=taskQuestionColor, alignText = 'center',wrapWidth= 30)
            stim.setPos((0, 0))
            stim.draw()
            win.flip()

            response = getbuttonColor(RESPONSE_SELECTION)  # listen to a button

            responses.append(response)


            stim = visual.TextStim(win, text='모든 버튼에서 손가락을 떼주세요.\n\n',
                                   font= stimuliFont, units= stimuliUnits, height=1, color=taskQuestionColor, alignText='center',wrapWidth= 30)
            stim.setPos((0,-2.5))
            stim.draw()
            win.flip()
            core.wait(TIME_TO_RESET_BUTTON_BOX)

            if responses[-1] == quitKey:
                participantName = participantInfo[0].replace(" ", "")
                filename = 'results.' + participantName + '.csv'
                results.to_csv(filename, encoding='utf-8-sig')
                win.close()
                core.quit()

            if trialList[trialIndex]['correctAnswer'] == "red" and responses[-1]==('right box', 'red'):

                recentCorrectResponses += 1
                totalCorrectResponses += 1
                answer = 1
            elif trialList[trialIndex]['correctAnswer'] == "yellow" and responses[-1]==('right box', 'yellow'):

                recentCorrectResponses += 1
                totalCorrectResponses += 1
                answer = 1
            else:

                answer = 0
            # Wait a little longer before moving on
            #core.wait(0.5)  # This ensures that the yellow text stays for an additional moment; here it awaits indefinitely

            for frameN in range(taskQuestionOff - 1):
                win.flip()
            win.flip()

            trialsSinceLastBreak += 1

    results.loc[trialIndex, 'name'] = participantInfo[0]
    results.loc[trialIndex, 'age'] = participantInfo[1]
    results.loc[trialIndex, 'sex'] = participantInfo[2]
    results.loc[trialIndex, 'handedness'] = participantInfo[3]
    results.loc[trialIndex, 'experiment'] = participantInfo[4]
    results.loc[trialIndex, 'list'] = participantInfo[5]
    results.loc[trialIndex, 'sentence'] = trialList[trialIndex]['sentence']
    results.loc[trialIndex, 'taskQuestion'] = trialList[trialIndex]['taskQuestion']
    results.loc[trialIndex, 'trigger'] = trialList[trialIndex]['trigger']

    # (선택) 옵션 로그도 저장하고 싶다면 아래 2줄 유지
    results.loc[trialIndex, 'option1'] = option1 if 'option1' in locals() else ''
    results.loc[trialIndex, 'option2'] = option2 if 'option2' in locals() else ''

    if ('option1' in locals() and (option1 or option2) and curr_block in (1,3)):
        # Block 1/3의 2지선다
        results.loc[trialIndex, 'expectedAnswer'] = trialList[trialIndex]['correctAnswer']
        results.loc[trialIndex, 'participantAnswer'] = responses[-1][1] if responses else ''
        results.loc[trialIndex, 'answer'] = answer
    elif isinstance(trialList[trialIndex]['taskQuestion'], str) and len(trialList[trialIndex]['taskQuestion']) >= 4:
        # 기존 taskQuestion 경로
        results.loc[trialIndex, 'expectedAnswer'] = trialList[trialIndex]['correctAnswer']
        results.loc[trialIndex, 'participantAnswer'] = responses[-1][1] if responses else ''
        results.loc[trialIndex, 'answer'] = answer
    else:
        results.loc[trialIndex, 'expectedAnswer'] = ''
        results.loc[trialIndex, 'participantAnswer'] = ''
        results.loc[trialIndex, 'answer'] = ''

    # TODO: check that this works correctly, this should save one by one
    participantName = participantInfo[0].replace(" ", "")
    filename = 'results.' + participantName + '.csv'
    results.to_csv(filename, encoding='utf-8-sig')

    event.clearEvents()
    #responses = []
    stim = visual.TextStim(win,
                           text='지금은 눈을 깜빡이셔도 괜찮습니다.\n\n' 
                                '다음 문장을 읽을 준비가 되면 \n\n'
                                '움직이지 말고,눈을 깜빡이지 않은 채로 \n\n'
                                '"예"(검지)를 누르세요.\n\n',
                           font= stimuliFont, units= stimuliUnits, height= 1, color=stimuliColor, wrapWidth= 30, alignText='center')
    stim.setPos((0, -1.5))
    stim.draw()
    win.flip()

    # pauseResponse = event.waitKeys(keyList=[responseYes, quitKey])
    # response = getbutton()  # listen to a button
    # responses.append(response) # everytime we get a response we add it to the table
    getbuttonColor(RESPONSE_PASS)

    #core.wait(0.5)  # This ensures that the yellow text stays for an additional moment; here it waits for exactly 500 ms



    # if responses[-1] == quitKey:
    #     participantName = participantInfo[0].replace(" ", "")
    #     filename = 'results.' + participantName + '.csv'
    #     results.to_csv(filename)
    #     win.close()
    #     core.quit()

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
                       font= stimuliFont, units= stimuliUnits, color= stimuliColor, height=INSTR_HEIGHT, alignText='center', wrapWidth=INSTR_WRAP)

stim.setPos((0, 0))
stim.draw()
win.flip()

#listenbutton(3) we want to add this to let them press at the end?

event.waitKeys()

participantName = participantInfo[0].replace(" ", "")
filename = 'results.' + participantName + '.csv'
results.to_csv(filename, encoding='utf-8-sig')

win.close()
core.quit()

dp.DPxClose()
