

# setup ordering of people should stimuli
#
# 5 conditions x 6 blocks of 6 words across 2 runs
# all words repeated in each condition
# 36 words per condition per run
# select 6 to occur first in each condition
# 18 pos 18 neg


import random

num_of_conditions = 6
blocks_per_condition = 1


trials = {
                    u'AGREE-pos': 3,
                    u'AGREE-neg': 3,
                    u'INFAVOR-pos': 1,
                    u'INFAVOR-neg': 1,
                    u'AGAINST-pos': 1,
                    u'AGAINST-neg': 1
                    }

conditions = ['AGREE-pos', 'AGREE-neg', 'INFAVOR-neg', 'INFAVOR-pos', 'AGAINST-pos', 'AGAINST-neg']

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
        #random.shuffle(conditions)
        for block in range(num_of_conditions):
            current_cond = conditions[block]
            val = current_cond[-3:]
            stimuli.append((current_cond,[(stim[val].pop()) for c in range(trials[current_cond])]))


    return stimuli

