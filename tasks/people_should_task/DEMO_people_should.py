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
import generate_stimuli2

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

statement_lists = generate_stimuli2.create_lists()

prompt_map = {'AGREE': 'AGREE',
                         'INFAVOR': 'IN FAVOR',
                         'AGAINST': 'AGAINST' }


blocks_per_run = 6

condition_text = "Starting the %s condition..."

items_per_block=1

frame_rate = 60

frames = {

    'fixation': 2*frame_rate,
    'trial3': 4*frame_rate,
    'trial': 12*frame_rate,
    'prep': 3*frame_rate
}

expdir = os.getcwd()
logdir = '%s/logs' % (expdir)

print logdir

##### SET UP #######

######





######
# set up trial handler

blocks = [ {'cond': cond[0], 'cnum': i+1, 'items': cond[1]} for i,cond in enumerate(statement_lists)]

trials = data.TrialHandler(blocks, 1, method='sequential')

print blocks



# setup logging #
log_file = logging.LogFile("logs/%s.log" % ('demo'),  level=logging.DATA, filemode="w")
 
 
################
# Set up window #
################

useFullScreen=True
win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False)


################
# Set up stimuli #
################ 
fixation = visual.TextStim(win, text="+", height=2, color="#FFFFFF")
ready_screen = visual.TextStim(win, text="Press space to continue....", height=1.5, color="#FFFFFF", wrapWidth=25)

prep_screen = visual.TextStim(win,text="", wrapWidth=32)

condition = visual.TextStim(win, text=conditions[0], pos=(0,5), color="#FFFFFF", colorSpace=(0,0,0), height=1.2)
conditionBG = visual.Rect(win, width=16, height=2, pos=(0,5))

stem = visual.TextStim(win,text="People should", pos=(-5.5,2.5), height=1.3)
word = visual.TextStim(win, text="kind", pos=(0,-0.5), height=1.8, wrapWidth=30)

resp1 = visual.TextStim(win,text="yes", pos=(-4,-4))
resp2 = visual.TextStim(win,text="no", pos=(4,-4))
resp3 = visual.TextStim(win,text="Press for each reason", pos=(0,-4))


instruct_text = visual.TextStim(win, text='', pos=(0,4), height=1, color="#FFFFFF", wrapWidth=24)
instruct_text2 = visual.TextStim(win, text='', pos=(0,-1), color='#FFFFFF', wrapWidth=24)
instruct_image = visual.ImageStim(win, pos=(0,7.5))
instruct_next = visual.TextStim(win, text='Please space to continue', pos=(0,-6) )

# instructions

page1 = [None,'''
In this task you will respond to PEOPLE SHOULD statements e.g. 'People should eat broccoli.'

There will be 3 conditions:
    
1. AGREE - Do you agree or disagree with the people should statement?

2. IN FAVOR - Can you think of reasons in support of the statement?

3. AGAINST - Can you think of reasons against the statement?
''']

page2 = ['img/demo1.png','''
In the AGREE condition you will see three different statements and be asked to quickly respond either YES or NO depending on whether you agree or disagree with the statement.

Press 1 for YES (you do agree with the statement)
Press 2 for NO (you do not agree with the statement)
'''] 


page3 = ['img/demo2.png', '''
In the IN FAVOR condition you will see a single statement for 12 seconds. Please try and think of as many different reasons in support of the statement as you can.

Press 1 for each different reason you can think of in support of the statement shown.
''']

page4 = ['img/demo3.png', '''
In the AGAINST condition you will see a single statement for 12 seconds. Please try and think of as many different reasons against the statement as you can.

Press 2 for each different reason you can think of against the statement shown.
''']

instructions = [page1, page2, page3, page4]
print instructions
for ipage in instructions:

    if ipage[0]==None:
        instruct_text.setText(ipage[1].strip())
        instruct_text.draw()
    else:
        instruct_image.setImage(ipage[0])
        instruct_text2.setText(ipage[1])
        instruct_image.draw()
        instruct_text2.draw()


    
    instruct_next.draw()
    win.flip()
    event.waitKeys(keyList=('space'))

# one run
for current_run in [1]:
    current_block = 0

    ########################
    # SHOW READY SCREEN #
    ########################


    ready_screen.draw()
    win.flip()

    # wait for trigger from scanner (5 key press)
    event.waitKeys(keyList=('space'))

    # set clock
    globalClock = core.Clock()
    logging.setDefaultClock(globalClock)

    logging.log(level=logging.DATA, msg="** START RUN %i **" % current_run)


    trials.extraInfo={'START': globalClock.getTime()}

    timer = core.Clock()
    
    while current_block < blocks_per_run:
        current_block+=1
        trial = trials.next()
    #for trial in trials:
        #print trial['cond'].encode('utf-8')

        cur_cond = trial['cond']

        prep_screen.setText(condition_text % prompt_map[cur_cond[:-4]])
        logging.log(level=logging.DATA, msg=condition_text % cur_cond)
        logging.log(level=logging.DATA, msg="Run %i - Block %i" % (current_run, current_run))

        for f in range(frames['prep']):         
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
            
            timer.reset()
            
            for frame in range(trial_time):
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
                    if key[0][0]=='1':
                        if cur_cond[:-4]=='AGREE':
                            resp1.setColor('#FF0000')
                            r1_clear.append(frame+30)
                        elif cur_cond[:-4]=='INFAVOR':
                            resp3.setColor('#FF0000')
                            r3_clear.append(frame+30)
                        resp.append((key[0][0],key[0][1],cur_item))
                        key=None
                    elif key[0][0]=='2':
                        if cur_cond[:-4]=='AGREE':
                            resp2.setColor('#FF0000')
                            r2_clear.append(frame+30)
                        elif cur_cond[:-4]=='AGAINST':
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
            print resp
            
            resp1.setColor('#FFFFFF')
            resp2.setColor('#FFFFFF')
            resp3.setColor('#FFFFFF')
         
            #trials.saveAsText(fileName=logname, appendFile=False)
            
        ready_screen.draw()
        win.flip()
        
        event.waitKeys(keyList=['space'])
          
         # post block fixation 
        logging.log(level=logging.DATA, msg="FIXATION")

        for frame in range(frames['fixation']):
            fixation.draw()
            win.flip()

    
