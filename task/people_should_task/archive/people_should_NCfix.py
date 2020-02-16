##############################
# Self Localizer for Project One #
##############################

#############################
#   6 conditions
#   AGREE-pos, AGREE-neg, INFAVOR-pos, INFAVOR-neg, AGAINST-pos, AGAINST-neg
#


# Import PsychoPy
from psychopy import visual, core, event, data, gui, logging

# Import modules
import os
import sys
import random
import generate_stimuli

##############
# Parameters #
##############

conditions = (
                    u'AGREE-pos',
                    u'INFAVOR-pos',
                    u'AGAINST-pos',
                    u'AGREE-neg',
                    u'INFAVOR-neg',
                    u'AGAINST-neg'
                    )

statement_lists = generate_stimuli.create_lists()

prompt_map = {'AGREE': 'AGREE',
                         'INFAVOR': 'IN FAVOR',
                         'AGAINST': 'AGAINST' }


blocks_per_run = 30

condition_text = "Starting the %s condition..."

items_per_block=6

frame_rate = 1

frames = {

    'rest' : 12*frame_rate,
    'fixation': 2*frame_rate,
    'trial3': 4*frame_rate,
    'trial': 12*frame_rate,
    'prep': 3*frame_rate
}

fixations=[]
fixation_dur = frames['fixation']
rest_dur = frames['rest']
durs = [fixation_dur, fixation_dur, fixation_dur, rest_dur]

instructions = ['img/instruct1.png', 'img/instruct2.png']
instruct_dur = 5

for j in range(6):
    random.shuffle(durs)
    fixations.append(fixation_dur)
    for d in durs:
        fixations.append(d)
        

expdir = os.getcwd()
logdir = '%s/logs' % (expdir)


##### SET UP #######

######

# get subjID
subjDlg = gui.Dlg(title="People Should Task")
subjDlg.addField('Enter Subject ID:')
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
else:
    sys.exit()


#########
# log file
# Get logfile name
ct = 0
while 'logname' not in locals() or os.path.exists(logname):
    if ct > 0:
        lognum = '_%d' % (ct)
    else:
        lognum = ''
    logname = '%s/%s%s.tsv' % (logdir, subj_id, lognum)
    ct += 1



######
# set up trial handler

blocks = [ {'cond': cond[0], 'cnum': i+1, 'items': cond[1]} for i,cond in enumerate(statement_lists)]

trials = data.TrialHandler(blocks, 1, method='random')




# setup logging #
log_file = logging.LogFile("logs/%s.log" % (subj_id),  level=logging.DATA, filemode="w")
 
 
################
# Set up window #
################

useFullScreen=True  
win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False)


################
# Set up stimuli #
################ 
fixation = visual.TextStim(win, text="+", height=2, color="#FFFFFF")
ready_screen = visual.TextStim(win, text="Ready.....", height=1.5, color="#FFFFFF")

prep_screen = visual.TextStim(win,text="", wrapWidth=32)

condition = visual.TextStim(win, text=conditions[0], pos=(0,5), color="#FFFFFF", colorSpace=(0,0,0), height=1.2)
conditionBG = visual.Rect(win, width=16, height=2, pos=(0,5))

stem = visual.TextStim(win,text="People should", pos=(-5.5,2.5), height=1.3)
word = visual.TextStim(win, text="kind", pos=(0,-0.5), height=1.8, wrapWidth=30)

resp1 = visual.TextStim(win,text="yes", pos=(-4,-4))
resp2 = visual.TextStim(win,text="no", pos=(4,-4))
resp3 = visual.TextStim(win,text="Press for each reason", pos=(0,-4))

# instrcution screen
instruction_image = visual.SimpleImageStim(win,image="img/instruct1.png",pos=(-2,0))
instruction_text = visual.TextStim(win, height=1.3,color="#000000", 
        text="In the AGREE condition use buttons 1 and 2 to indicate whether you agree or disagree ", 
        pos=(0,+5))


# -------------

timer = core.Clock()
current_run =1 
########################
# SHOW READY SCREEN #
########################
ready_screen.draw()
win.flip()

# wait for trigger from scanner ('t' key press)
event.waitKeys(keyList=('t'))

# set clock
globalClock = core.Clock()
logging.setDefaultClock(globalClock)

logging.log(level=logging.DATA, msg="** START RUN %i **" % current_run)


trials.extraInfo={'START': globalClock.getTime()}

# disdaq fixation
logging.log(level=logging.DATA, msg="INSTRUCTIONS")

################ 
# SHOW INSTRUCTIONS
################

for instruction in instructions:
    timer.reset()
    instruction_image.setImage(instruction)
    while timer.getTime() < instruct_dur:
        instruction_image.draw()
        win.flip()
        

current_block=0
while current_block < blocks_per_run:
    current_block+=1
    trial = trials.next()

    cur_cond = trial['cond']

    prep_screen.setText(condition_text % prompt_map[cur_cond[:-4]])
    logging.log(level=logging.DATA, msg=condition_text % cur_cond)
    logging.log(level=logging.DATA, msg="Run %i - Block %i" % (current_run, current_run))


    timer.reset()
    while timer.getTime() < frames['prep']:
    #for f in range(frames['prep']):         
        prep_screen.draw()
        win.flip()

    # get next set of words
    block_items = trial['items']
    random.shuffle(block_items)

    condition.setText(prompt_map[cur_cond[:-4]])
    for idx,cur_item in enumerate(block_items):
        event.clearEvents()
        resp = []
        
        #words.trialList.append({'cond': trial['cond'], 'word': cur_item, 'tIdx': idx+1})
        
        
        word.setText(cur_item)
        
        logging.log(level=logging.DATA, msg="Trial %i - Stimuli %s - Condition %s" % (idx+1,cur_item, cur_cond))

        
        key = None
        rt = None
        r1_clear=[]
        r2_clear=[]
        r3_clear=[]
        
        trial_time = frames['trial3'] if cur_cond[:-4]=='AGREE' else frames['trial']
        
        frame=0
        timer.reset()
        while timer.getTime() < trial_time:
        #for frame in range(trial_time):
            condition.draw()
            conditionBG.draw()
            stem.draw()
            word.draw()
            if cur_cond[:-4]=='AGREE':
                resp1.draw()
                resp2.draw()
            else:
                resp3.draw()
            if not key:
                key = event.getKeys(timeStamped=globalClock)
            else:
                if key[0][0]=='b':
                    if cur_cond[:-4]=='AGREE':
                        resp1.setColor('#FF0000')
                        r1_clear.append(frame+30)
                    else:
                        resp3.setColor('#FF0000')
                        r3_clear.append(frame+30)
                    resp.append((key[0][0],key[0][1],cur_item))
                    key=None
                elif key[0][0]=='y':
                    if cur_cond[:-4]=='AGREE':
                        resp2.setColor('#FF0000')
                        r2_clear.append(frame+30)
                    else:
                        resp3.setColor('#FF0000')
                        r3_clear.append(frame+30)
                    resp.append((key[0][0],key[0][1],cur_item))
                    key=None
            win.flip()
            if frame in r1_clear:
                resp1.setColor('#FFFFFF')
            if frame in r2_clear:
                resp2.setColor('#FFFFFF')       
            if frame in r3_clear:
                resp3.setColor('#FFFFFF')
            
            frame+=1
        
        
        resp1.setColor('#FFFFFF')
        resp2.setColor('#FFFFFF')
        resp3.setColor('#FFFFFF')
     
        #trials.saveAsText(fileName=logname, appendFile=False)
      
     # post block fixation 
    logging.log(level=logging.DATA, msg="FIXATION")


    fixation_dur = fixations[current_block-1]
    timer.reset()
    while timer.getTime() < fixation_dur:
    #for frame in range(frames['fixation']):
        fixation.draw()
        win.flip()

logging.log(level=logging.DATA, msg="*** END Run %i ****" % current_run)

trials.extraInfo['END']=globalClock.getTime()
trials.saveAsText(fileName=logname, appendFile=False)

event.waitKeys(keyList=('space'))
