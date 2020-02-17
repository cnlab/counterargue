##################################
#       People should task       #
#                                #
# A counterarguing localizer     #
# for use in fMRI studies        # 
#                                #
# Copyright (c) 2011-2019        #
# Communication Neuroscience Lab #
##################################

'''
Task uses PsychoPy Python library
and has been updated and tested with 
PsychoPy v3.2.3 on 9/22/19

Coding and testing by Matt O'Donnell (mbod@asc.upenn.edu)

For more details and questions
check github repository for task
https://github.com/cnlab/counterargue
or contact Matt O'Donnell (mbod@asc.upenn.edu)

'''




import random

num_of_conditions = 6
blocks_per_condition = 5


trials = {
                    u'AGREE-pos': 3,
                    u'INFAVOR-pos': 1,
                    u'AGAINST-pos': 1,
                    u'AGREE-neg': 3,
                    u'INFAVOR-neg': 1,
                    u'AGAINST-neg': 1
                    }

conditions = list(trials.keys())

def create_lists():
    # load word lists

    pos = [w.strip() for w in open('positive.txt')]
    neg = [w.strip() for w in open('negative.txt')]
    neu = [w.strip() for w in open('neutral.txt')]

    random.shuffle(neu)
    # add half of neutral stim to positive list and half to negative
    nlen = len(neu)
    pos.extend(neu[0:nlen])
    neg.extend(neu[nlen:])
    
    random.shuffle(pos)
    random.shuffle(neg)

    stim = { 'pos': pos, 'neg': neg }
    stimuli = []
    
    for round in range(blocks_per_condition):
        random.shuffle(conditions)
        for block in range(num_of_conditions):
            current_cond = conditions[block]
            val = current_cond[-3:]
            stimuli.append((current_cond,[(stim[val].pop()) for c in range(trials[current_cond])]))


    return stimuli

