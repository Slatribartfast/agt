from scipy import rand
import staaten
import main

from itertools import combinations
import random
import math

def calc_gain(l_1:list[int], l_2:list[int]):
    # distance l_1 to l_2
    # no real distance because order matters
    
    res = 0
    for i in range(len(staaten.state_names)):
        if i in l_1 and i not in l_2:
            res += 1
        elif i not in l_1 and i in l_2:
            res += 1
            
    return res

def get_loosing_coals(max_out: int = 5, max_overall: int = 15, min_gain: int = 6, kick_rate: int = 1000, give_up_rate: int = 10000, min_pop_size = 0.625, min_avg_pop_size = 0.645)-> list[list]:
    loosing_coals_all = []
    for i in range(max_out + 1):
        loosing_coals_pre = []
        bool_array = []
        for positions in combinations(range(len(staaten.state_names)), len(staaten.state_names) - i):
                p = [0] * len(staaten.state_names)

                for i in positions:
                    p[i] = 1
                bool_array.append(p)   
                   
        for elem in bool_array: 
            test_coal = []
            for j in range(len(elem)):               
                if elem[j]:
                    test_coal.append(j)
            if not main.is_winning(test_coal):
                # and pop enough
                c = 0
                for elem in test_coal:
                    c = c + staaten.state_share[elem]
                if c > min_pop_size:
                    loosing_coals_pre.append(test_coal)
        if len(loosing_coals_pre)  > 0:
           loosing_coals_all.append(loosing_coals_pre) 
                

    loosing_coals = [] 
    c_bad_luck = 0  
    current_max_length = 0
    
    c = 0
    for s in loosing_coals_all:
        c = c + len(s)
    print(f"There are {c} coalitions left")
    
    while len(loosing_coals) <  max_overall- 1:
        # print(f"h {c_bad_luck}")
        c_bad_luck = c_bad_luck + 1
        if c_bad_luck % kick_rate == 0:
            if len(loosing_coals) < 2:
                continue
           # c_bad_luck = 0
           # kick one randomly
            loosing_coals.pop(random.randrange(len(loosing_coals)))
            # and the least populated one
            #c_pop_l = []
            #for elem in loosing_coals:  
            #   count_pop = 0        
            #    for s in elem:
            #        count_pop += staaten.state_share[s]
            #    c_pop_l.append(count_pop)
            #min_value = min(c_pop_l)
            #return the index of minimum value 
            #min_index=c_pop_l.index(min_value)   
            #loosing_coals.pop(min_index)
        if c_bad_luck % give_up_rate == 0:
            min_gain = min_gain - 1
            c_bad_luck = 0
            # print("minimizing dis")
        wanted_length_ix = random.randint(0, len(loosing_coals_all)-1)
        # print(f"{wanted_length_ix} {len(loosing_coals_all)}")
        cand = random.choice(loosing_coals_all[wanted_length_ix])
        
        if cand in loosing_coals:
            continue
        min_dist = min_gain
        for elem in loosing_coals:
            d = calc_gain(elem, cand)
            if d < min_dist:
                min_dist = d
        
        #
        c_pop_1 = 0
        avg_pop = 1
        if len(loosing_coals)  > 0:
            for elem in loosing_coals:          
                for s in elem:
                    c_pop_1 = c_pop_1 + staaten.state_share[s]                   
        
        for elem in cand:
           c_pop_1 = c_pop_1 + staaten.state_share[elem] 
        
        avg_pop = (c_pop_1) / (len(loosing_coals) + 1)
          
        # penelty for long words
        min_dist = min_dist + (max_out - (len(staaten.state_names) - len(cand)))
        # penelaty for long wait
            
        if min_dist >= min_gain and avg_pop > min_avg_pop_size:
            loosing_coals.append(cand)
            if current_max_length < len(loosing_coals):
                current_max_length = len(loosing_coals)
                c_bad_luck = 0
 
        
                
    # the last sepcial one
    is_loosing = True
    c = 0
    while(is_loosing):
        c = c + 1
        test_coal = []
        for j in range(len(staaten.state_names)):
            if j <= c:
                test_coal.append(j)
        if main.is_winning(test_coal):
                loosing_coals.append(test_coal[:-1])
                is_loosing = False
        
    return loosing_coals

                
if __name__ == '__main__':
    for elem in get_loosing_coals():
        invert_to_readable = []
        for i in range(len(staaten.state_names)):
            if i in elem:
                pass
            else:
                invert_to_readable.append(i+1)
        print(invert_to_readable)
                
        