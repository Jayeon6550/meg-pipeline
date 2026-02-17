#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This experiment was created using PsychoPy2 Experiment Builder (v1.85.6),
    on Wed Dec 27 11:31:39 2017
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Quit the Finder automatically before running the experiment
#applescript="\'tell application \"Finder\" to quit\'"
#shellCmd = 'osascript -e '+applescript
#os.system(shellCmd)

# Store info about the experiment session
expName = u'winter-priming_fwd33ms'  # from the Builder filename that created this script
expInfo = {'Name': '', 'Last name': '', 'Gender': ['M', 'F'],'Handedness': ['R', 'L'], 'Age': '', 'List': ['1a', '1b', '2a', '2b', '3a', '3b', '4a', '4b']}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName, order=['Name','Last name','Gender','Handedness','Age','List'])
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s_%s_%s' % (expInfo['Name'], expInfo['Last name'], expInfo['List'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=(1440, 900), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor=u'321A', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "start"
startClock = core.Clock()
consent_text = visual.TextStim(win=win, name='consent_text',
    text=u"Welcome and thank you for your interest in this experiment!\n\nOn average, this experiment takes about 12-15 minutes to complete, but the time may vary depending on how much time you will take during the breaks. You will be paid 30 AED for your time.\n\nThis experiment is being conducted by Dr. Roberto Petrosino and Prof. Diogo Almeida at the New York University Abu Dhabi (NYUAD), and has been approved by the NYUAD Institutional Review Board.\n\nTo take part in this experiment, you must be a native speaker of ENGLISH and have no known linguistic or learning disability (e.g., dyslexia). If you do not meet these requirements, please report to the experimenter.\n\nWe finally ask you to leave your phone out of the testing room, so to avoid any source of distraction during the experiment. We appreciate your cooperation.\n\nIf you are willing to participate in the experiment, press 'SPACE'.",
    font=u'Arial',
    pos=(0, 0), height=0.08, wrapWidth=2, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

start_text = visual.TextStim(win=win, name='start_text',
    text=u"In this experiment, you will see some letter strings at the center of the display. \nYou will be asked to decide whether they are a real English word as fast and accurately as possible.\n\nIf you think they are, press 'j'.\nIf you think they are not, press 'f'.\n\nWhen you are ready, press 'SPACE' to start some practice hits.",
    font=u'Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "fmask"
fmaskClock = core.Clock()
fmask_txt = visual.TextStim(win=win, name='fmask_txt',
    text='#######',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "prime"
primeClock = core.Clock()
prime_txt = visual.TextStim(win=win, name='prime_txt',
    text='default text',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "bmask"
bmaskClock = core.Clock()
bmask_txt = visual.TextStim(win=win, name='bmask_txt',
    text='#######',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "target"
targetClock = core.Clock()
target_txt = visual.TextStim(win=win, name='target_txt',
    text='default text',
    font=u'Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "Break_warmup"
Break_warmupClock = core.Clock()
break_wp_text = visual.TextStim(win=win, name='break_wp_text',
    text=u"How was it?\nYou will be given 4 short breaks throughout the experiment.\n\nRemember:\n - if you think the letter string on the screen is an English word, press 'j'.\n- if you think the letter string on the screen is NOT an English word, press 'f'.\n\nYou should do this as fast and accurately as possible.\n\nPress 'SPACE' to go through another practice batch.",

    font=u'Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);


# Initialize components for Routine "ready"
readyClock = core.Clock()
ready_text = visual.TextStim(win=win, name='ready_text',
    text=u"Any question? The experiment starts now.\n\nWhen you are ready, press 'SPACE' to begin.",
    font=u'Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "fmask"
fmaskClock = core.Clock()
fmask_txt = visual.TextStim(win=win, name='fmask_txt',
    text='#######',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "prime"
primeClock = core.Clock()
prime_txt = visual.TextStim(win=win, name='prime_txt',
    text='default text',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "bmask"
bmaskClock = core.Clock()
bmask_txt = visual.TextStim(win=win, name='bmask_txt',
    text='#######',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "target"
targetClock = core.Clock()
target_txt = visual.TextStim(win=win, name='target_txt',
    text='default text',
    font=u'Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "Break"
BreakClock = core.Clock()
break_text = visual.TextStim(win=win, name='break_text',
    text=u"placeholder", #the actual text of the break routine is defined below
    font=u'Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);


# Initialize components for Routine "exit"
exitClock = core.Clock()
exit_text = visual.TextStim(win=win, name='exit_text',
    text=u"The experiment is over.\n\n Many thanks for participating!",
    font=u'Arial',
    pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

####### ROUTINE INFO ############

fwdFrame = 30 # how long will the forward mask have to last?
primeFrame = 2 # how long will the prime word have to be presented for?
bwdFrame = 0 # how long will the backward mask have to last?
breakIdx = [39, 79, 119, 159] # define the trial index at which to present breaks (in this case every 40 trials)
experimentPrefix = 'winter-priming_' # just a prefix identifying the experiment and the relative lists

#################################

# ------Prepare to start Routine "consent"-------
t = 0
startClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
consent_resp = event.BuilderKeyResponse()
# keep track of which components have finished
consentComponents = [consent_text, consent_resp]
for thisComponent in consentComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "start"-------
while continueRoutine:
    # get current time
    t = startClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *start_text* updates
    if t >= 0.0 and consent_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        consent_text.tStart = t
        consent_text.frameNStart = frameN  # exact frame index
        consent_text.setAutoDraw(True)

    # *start_resp* updates
    if t >= 0.0 and consent_resp.status == NOT_STARTED:
        # keep track of start time/frame for later
        consent_resp.tStart = t
        consent_resp.frameNStart = frameN  # exact frame index
        consent_resp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(consent_resp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if consent_resp.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            consent_resp.keys = theseKeys[-1]  # just the last key pressed
            consent_resp.rt = consent_resp.clock.getTime()
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in consentComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "consent"-------
for thisComponent in consentComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if consent_resp.keys in ['', [], None]:  # No response was made
    consent_resp.keys=None
thisExp.addData('consent_resp.keys', consent_resp.keys)
if consent_resp.keys != None:  # we had a response
    thisExp.addData('consent_resp.rt', consent_resp.rt)
thisExp.nextEntry()
# the Routine "start" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()


# ------Prepare to start Routine "start"-------
t = 0
startClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
start_resp = event.BuilderKeyResponse()
# keep track of which components have finished
startComponents = [start_text, start_resp]
for thisComponent in startComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "start"-------
while continueRoutine:
    # get current time
    t = startClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *start_text* updates
    if t >= 0.0 and start_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        start_text.tStart = t
        start_text.frameNStart = frameN  # exact frame index
        start_text.setAutoDraw(True)

    # *start_resp* updates
    if t >= 0.0 and start_resp.status == NOT_STARTED:
        # keep track of start time/frame for later
        start_resp.tStart = t
        start_resp.frameNStart = frameN  # exact frame index
        start_resp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(start_resp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if start_resp.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            start_resp.keys = theseKeys[-1]  # just the last key pressed
            start_resp.rt = start_resp.clock.getTime()
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in startComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "start"-------
for thisComponent in startComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if start_resp.keys in ['', [], None]:  # No response was made
    start_resp.keys=None
thisExp.addData('start_resp.keys',start_resp.keys)
if start_resp.keys != None:  # we had a response
    thisExp.addData('start_resp.rt', start_resp.rt)
thisExp.nextEntry()
# the Routine "start" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
loop_warmup = data.TrialHandler(nReps=1, method='random',
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(experimentPrefix+'warm-up.csv'),
    seed=None, name='loop_warmup')
thisExp.addLoop(loop_warmup)  # add the loop to the experiment
thisLoop_warmup = loop_warmup.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisLoop_warmup.rgb)
if thisLoop_warmup != None:
    for paramName in thisLoop_warmup:
        exec('{} = thisLoop_warmup[paramName]'.format(paramName))

for thisLoop_warmup in loop_warmup:
    currentLoop = loop_warmup
    # abbreviate parameter names if possible (e.g. rgb = thisLoop_warmup.rgb)
    if thisLoop_warmup != None:
        for paramName in thisLoop_warmup:
            exec('{} = thisLoop_warmup[paramName]'.format(paramName))

    # ------Prepare to start Routine "fmask"-------
    fmaskClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    fmaskComponents = [fmask_txt]
    for thisComponent in fmaskComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "fmask"-------
    while continueRoutine:
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *fmask_txt* updates
        if frameN >= 0.0 and fmask_txt.status == NOT_STARTED:
            # keep track of start time/frame for later
            fmask_txt.frameNStart = frameN  # exact frame index
            fmask_txt.setAutoDraw(True)
            win.callOnFlip(fmaskClock.reset) # t=0 at the first frame of the routine
        if fmask_txt.status == STARTED and frameN >= (fmask_txt.frameNStart + fwdFrame):
            fmask_txt.setAutoDraw(False)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fmaskComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "fmask"-------
    for thisComponent in fmaskComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store time of presentation to make sure
    loop_warmup.addData('fr_fmask', frameN)

    # ------Prepare to start Routine "prime"-------
    primeClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    prime_txt.setText(prime)
    # keep track of which components have finished
    primeComponents = [prime_txt]
    for thisComponent in primeComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "prime"-------
    while continueRoutine:
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # *prime_txt* updates
        if frameN >= 0.0 and prime_txt.status == NOT_STARTED:
            # keep track of start time/frame for later
            prime_txt.frameNStart = frameN  # exact frame index
            prime_txt.setAutoDraw(True)
            win.callOnFlip(primeClock.reset) # t=0 at the first frame of the routine
        if prime_txt.status == STARTED and frameN >= (prime_txt.frameNStart + primeFrame):
            prime_txt.setAutoDraw(False)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in primeComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
            if frameN == 0: # the very first frame of the prime stimulus
                fmaskDuration = fmaskClock.getTime() # marks the offset of the fmask

    # -------Ending Routine "prime"-------
    for thisComponent in primeComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    loop_warmup.addData('t_fmask', fmaskDuration) # stamps the duration of the fmask in seconds
    loop_warmup.addData('fr_prime', frameN) #stamps the duration of the prime in frames

    # ------Prepare to start Routine "bmask"-------
    bmaskClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    bmaskComponents = [bmask_txt]
    for thisComponent in bmaskComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "bmask"-------
    while continueRoutine:
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # *bmask_txt* updates
        if frameN >= 0.0 and bmask_txt.status == NOT_STARTED:
            # keep track of start time/frame for later
            bmask_txt.frameNStart = frameN  # exact frame index
            bmask_txt.setAutoDraw(True)
            win.callOnFlip(bmaskClock.reset) # t=0 at the very first frame of the routine
        if bmask_txt.status == STARTED and frameN >= (bmask_txt.frameNStart + bwdFrame):
            bmask_txt.setAutoDraw(False)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in bmaskComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        #if frameN == 0: # at the first frame of the routine
            #primeDuration = primeClock.getTime() # marks the offset of the prime clock

    # -------Ending Routine "bmask"-------
    for thisComponent in bmaskComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    #store timing to be sure we are all set
    #loop_warmup.addData('t_prime', primeDuration) # stamps the duration of the prime in seconds
    loop_warmup.addData('fr_bmask', frameN) # stamps the duration of the bmask in frames

    # ------Prepare to start Routine "target"-------
    t = 0
    targetClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    target_txt.setText(target)
    target_resp = event.BuilderKeyResponse()
    # keep track of which components have finished
    targetComponents = [target_txt, target_resp]
    for thisComponent in targetComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "target"-------
    while continueRoutine:
        # get current time
        t = targetClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *target_txt* updates
        if t >= 0.0 and target_txt.status == NOT_STARTED:
            # keep track of start time/frame for later
            target_txt.tStart = t
            target_txt.frameNStart = frameN  # exact frame index
            target_txt.setAutoDraw(True)

        # *target_resp* updates
        if t >= 0.0 and target_resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            target_resp.tStart = t
            target_resp.frameNStart = frameN  # exact frame index
            target_resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(target_resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if target_resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['f', 'j'])

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                target_resp.keys = theseKeys[-1]  # just the last key pressed
                target_resp.rt = target_resp.clock.getTime()
                # was this 'correct'?
                if (target_resp.keys == str(corrAns)) or (target_resp.keys == corrAns):
                    target_resp.corr = 1
                else:
                    target_resp.corr = 0
                # a response ends the routine
                continueRoutine = False

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in targetComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
            if frameN == 0: # at the very first frame of the routine
                primeDuration = primeClock.getTime() # marks the offset of the prime clock
                bmaskDuration = bmaskClock.getTime() # marks the offset of the bmask clock

    # -------Ending Routine "target"-------
    for thisComponent in targetComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if target_resp.keys in ['', [], None]:  # No response was made
        target_resp.keys=None
        # was no response the correct answer?!
        if str(corrAns).lower() == 'none':
           target_resp.corr = 1  # correct non-response
        else:
           target_resp.corr = 0  # failed to respond (incorrectly)
    # store data for loop_warmup (TrialHandler)
    loop_warmup.addData('t_prime', primeDuration) # stamps the duration of the prime in seconds
    loop_warmup.addData('t_bmask', bmaskDuration) # stamps the duration of the bmask in seconds
    loop_warmup.addData('target_resp.keys',target_resp.keys)
    loop_warmup.addData('target_resp.corr', target_resp.corr)
    if target_resp.keys != None:  # we had a response
        loop_warmup.addData('target_resp.rt', target_resp.rt)
    # the Routine "target" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # ------Prepare to start Routine "Break_warmup"-------
    t = 0
    Break_warmupClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    key_break_wp = event.BuilderKeyResponse()
    if loop_warmup.thisN not in [ int( loop_warmup.nTotal / 2 ) - 1 ]:
        continueRoutine = False #take a break after the first half of stimuli has been presented
    # keep track of which components have finished
    Break_warmupComponents = [break_wp_text, key_break_wp]
    for thisComponent in Break_warmupComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "Break_warmup"-------
    while continueRoutine:
        # get current time
        t = Break_warmupClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *break_wp_text* updates
        if t >= 0.0 and break_wp_text.status == NOT_STARTED:
            # keep track of start time/frame for later
            break_wp_text.tStart = t
            break_wp_text.frameNStart = frameN  # exact frame index
            break_wp_text.setAutoDraw(True)

        # *key_break_wp* updates
        if t >= 0 and key_break_wp.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_break_wp.tStart = t
            key_break_wp.frameNStart = frameN  # exact frame index
            key_break_wp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_break_wp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if key_break_wp.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                key_break_wp.keys = theseKeys[-1]  # just the last key pressed
                key_break_wp.rt = key_break_wp.clock.getTime()
                # a response ends the routine
                continueRoutine = False


        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Break_warmupComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "Break_warmup"-------
    for thisComponent in Break_warmupComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_break_wp.keys in ['', [], None]:  # No response was made
        key_break_wp.keys=None
    loop_warmup.addData('key_break_wp.keys',key_break_wp.keys)
    if key_break_wp.keys != None:  # we had a response
        loop_warmup.addData('key_break_wp.rt', key_break_wp.rt)

    # the Routine "Break_warmup" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()

# completed 1 repeats of 'loop_warmup'


# ------Prepare to start Routine "ready"-------
t = 0
readyClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
ready_key = event.BuilderKeyResponse()
# keep track of which components have finished
readyComponents = [ready_text, ready_key]
for thisComponent in readyComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "ready"-------
while continueRoutine:
    # get current time
    t = readyClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *ready_text* updates
    if t >= 0.0 and ready_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        ready_text.tStart = t
        ready_text.frameNStart = frameN  # exact frame index
        ready_text.setAutoDraw(True)

    # *ready_key* updates
    if t >= 0.0 and ready_key.status == NOT_STARTED:
        # keep track of start time/frame for later
        ready_key.tStart = t
        ready_key.frameNStart = frameN  # exact frame index
        ready_key.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(ready_key.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if ready_key.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            ready_key.keys = theseKeys[-1]  # just the last key pressed
            ready_key.rt = ready_key.clock.getTime()
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in readyComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "ready"-------
for thisComponent in readyComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if ready_key.keys in ['', [], None]:  # No response was made
    ready_key.keys=None
thisExp.addData('ready_key.keys',ready_key.keys)
if ready_key.keys != None:  # we had a response
    thisExp.addData('ready_key.rt', ready_key.rt)
thisExp.nextEntry()
# the Routine "ready" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
loop = data.TrialHandler(nReps=1, method='random',
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(experimentPrefix+"list"+expInfo['List']+".csv"),
    seed=None, name='loop')
thisExp.addLoop(loop)  # add the loop to the experiment
thisLoop = loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisLoop.rgb)
if thisLoop != None:
    for paramName in thisLoop.keys():
        exec('{} = thisLoop[paramName]'.format(paramName))

for thisLoop in loop:
    currentLoop = loop
    # abbreviate parameter names if possible (e.g. rgb = thisLoop.rgb)
    if thisLoop != None:
        for paramName in thisLoop.keys():
            exec('{} = thisLoop[paramName]'.format(paramName))

    # ------Prepare to start Routine "fmask"-------
    #t = 0
    fmaskClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    fmaskComponents = [fmask_txt]
    for thisComponent in fmaskComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "fmask"-------
    while continueRoutine:
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *fmask_txt* updates
        if frameN >= 0.0 and fmask_txt.status == NOT_STARTED:
            # keep track of start time/frame for later
            fmask_txt.frameNStart = frameN  # exact frame index
            fmask_txt.setAutoDraw(True)
            win.callOnFlip(fmaskClock.reset) # t=0 at the first frame of the routine
        if fmask_txt.status == STARTED and frameN >= (fmask_txt.frameNStart + fwdFrame):
            fmask_txt.setAutoDraw(False)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fmaskComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "fmask"-------
    for thisComponent in fmaskComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    loop.addData('fr_fmask', frameN) # stamps the duration of the fmask in frames

    # ------Prepare to start Routine "prime"-------
    #t = 0
    primeClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    prime_txt.setText(prime)
    # keep track of which components have finished
    primeComponents = [prime_txt]
    for thisComponent in primeComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "prime"-------
    while continueRoutine:
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *prime_txt* updates
        if frameN >= 0.0 and prime_txt.status == NOT_STARTED:
            # keep track of start time/frame for later
            prime_txt.frameNStart = frameN  # exact frame index
            prime_txt.setAutoDraw(True)
            win.callOnFlip(primeClock.reset) # t=0 at the very first frame of the routine
        if prime_txt.status == STARTED and frameN >= (prime_txt.frameNStart + primeFrame):
            prime_txt.setAutoDraw(False)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in primeComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
            if frameN == 0: #the very first frame of the prime stimulus
                fmaskDuration = fmaskClock.getTime() #marks the offset of the fmask clock

    # -------Ending Routine "prime"-------
    for thisComponent in primeComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    loop.addData('t_fmask', fmaskDuration) # stamps the duration of the fmask in seconds
    loop.addData('fr_prime', frameN) # stamps the duration of the prime in frames

    # ------Prepare to start Routine "bmask"-------
    bmaskClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    bmaskComponents = [bmask_txt]
    for thisComponent in bmaskComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "bmask"-------
    while continueRoutine:
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *bmask_txt* updates
        if frameN >= 0.0 and bmask_txt.status == NOT_STARTED:
            # keep track of start time/frame for later
            bmask_txt.frameNStart = frameN  # exact frame index
            bmask_txt.setAutoDraw(True)
            win.callOnFlip(bmaskClock.reset) # t=0 at the very first frame of the routine
        if bmask_txt.status == STARTED and frameN >= (bmask_txt.frameNStart + bwdFrame):
            bmask_txt.setAutoDraw(False)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in bmaskComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
            #if frameN == 0: # at the first frame of the routine
                #primeDuration = primeClock.getTime() # marks the offset of the prime clock

    # -------Ending Routine "bmask"-------
    for thisComponent in bmaskComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    #loop.addData('t_prime', primeDuration) # stamps the duration of the prime in seconds
    loop.addData('fr_bmask', frameN) # stamps the duration of the bmask in frames

    # ------Prepare to start Routine "target"-------
    t = 0
    targetClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    target_txt.setText(target)
    target_resp = event.BuilderKeyResponse()
    # keep track of which components have finished
    targetComponents = [target_txt, target_resp]
    for thisComponent in targetComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "target"-------
    while continueRoutine:
        # get current time
        t = targetClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *target_txt* updates
        if t >= 0.0 and target_txt.status == NOT_STARTED:
            # keep track of start time/frame for later
            target_txt.tStart = t
            target_txt.frameNStart = frameN  # exact frame index
            target_txt.setAutoDraw(True)

        # *target_resp* updates
        if t >= 0.0 and target_resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            target_resp.tStart = t
            target_resp.frameNStart = frameN  # exact frame index
            target_resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(target_resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if target_resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['f', 'j'])

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                target_resp.keys = theseKeys[-1]  # just the last key pressed
                target_resp.rt = target_resp.clock.getTime()
                # was this 'correct'?
                if (target_resp.keys == str(corrAns)) or (target_resp.keys == corrAns):
                    target_resp.corr = 1
                else:
                    target_resp.corr = 0
                # a response ends the routine
                continueRoutine = False

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in targetComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
            if frameN == 0: #at the very first frame of the routine
                primeDuration = primeClock.getTime() # marks duratin of the prime in seconds
                bmaskDuration = bmaskClock.getTime() # marks duration of the bmask in seconds

    # -------Ending Routine "target"-------
    for thisComponent in targetComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if target_resp.keys in ['', [], None]:  # No response was made
        target_resp.keys=None
        # was no response the correct answer?!
        if str(corrAns).lower() == 'none':
           target_resp.corr = 1  # correct non-response
        else:
           target_resp.corr = 0  # failed to respond (incorrectly)
    # store data for loop (TrialHandler)
    loop.addData('t_prime', primeDuration) #stamps the duration of the prime in seconds
    loop.addData('t_bmask', bmaskDuration) # stamps the duration of the bmask in seconds
    loop.addData('target_resp.keys',target_resp.keys)
    loop.addData('target_resp.corr', target_resp.corr)
    if target_resp.keys != None:  # we had a response
        loop.addData('target_resp.rt', target_resp.rt)
    # the Routine "target" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # ------Prepare to start Routine "Break"-------
    t = 0
    BreakClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    break_resp = event.BuilderKeyResponse()
   #if (loop.thisN != 0) and (loop.thisN % 40 != 0) :
    if loop.thisN not in breakIdx:
        continueRoutine = False # pause the loop and take a break every 40 trials
    # keep track of which components have finished
    BreakComponents = [break_text, break_resp]
    break_text.text = "You can now take a short break.\n\nThere are " + str(loop.nRemaining) + " words left.\n\nWhen you are ready, press 'SPACE' to resume the experiment."
    for thisComponent in BreakComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "Break"-------
    while continueRoutine:
        # get current time
        t = BreakClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *break_text* updates
        if t >= 0.0 and break_text.status == NOT_STARTED:
            # keep track of start time/frame for later
            break_text.tStart = t
            break_text.frameNStart = frameN  # exact frame index
            break_text.setAutoDraw(True)

        # *break_resp* updates
        if t >= 0.0 and break_resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            break_resp.tStart = t
            break_resp.frameNStart = frameN  # exact frame index
            break_resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(break_resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if break_resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                break_resp.keys = theseKeys[-1]  # just the last key pressed
                break_resp.rt = break_resp.clock.getTime()
                # a response ends the routine
                continueRoutine = False

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in BreakComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "Break"-------
    for thisComponent in BreakComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if break_resp.keys in ['', [], None]:  # No response was made
        break_resp.keys=None
    loop.addData('break_resp.keys',break_resp.keys)
    if break_resp.keys != None:  # we had a response
        loop.addData('break_resp.rt', break_resp.rt)

    # the Routine "Break" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()

# completed 1 repeats of 'loop'


# ------Prepare to start Routine "exit"-------
t = 0
exitClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_2 = event.BuilderKeyResponse()
# keep track of which components have finished
exitComponents = [exit_text, key_resp_2]
for thisComponent in exitComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "exit"-------
while continueRoutine:
    # get current time
    t = exitClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *exit_text* updates
    if t >= 0.0 and exit_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        exit_text.tStart = t
        exit_text.frameNStart = frameN  # exact frame index
        exit_text.setAutoDraw(True)

    # *key_resp_2* updates
    if t >= 0.0 and key_resp_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_2.tStart = t
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_2.status == STARTED:
        theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_2.keys = theseKeys[-1]  # just the last key pressed
            key_resp_2.rt = key_resp_2.clock.getTime()
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in exitComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "exit"-------
for thisComponent in exitComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_2.keys in ['', [], None]:  # No response was made
    key_resp_2.keys=None
thisExp.addData('key_resp_2.keys',key_resp_2.keys)
if key_resp_2.keys != None:  # we had a response
    thisExp.addData('key_resp_2.rt', key_resp_2.rt)
thisExp.nextEntry()
# the Routine "exit" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()


# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
