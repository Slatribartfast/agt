from scipy import rand
import staaten
import main

from itertools import combinations
import random
import math
import numpy as np

def calc_gain(l_1:np.array, l_2:np.array):
    # distance l_1 to l_2
    # no real distance because order matters
    
    res = 0
    for i in range(len(staaten.state_names)):
        if i in l_1 and i not in l_2:
            res += 1
        elif i not in l_1 and i in l_2:
            res += 1
            
    return res

def get_loosing_coals(max_out: int = 5, max_overall: int = 15, min_gain: int = 6, kick_rate: int = 1000, give_up_rate: int = 10000)-> list[list]:
    rng = np.random.default_rng()
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
                loosing_coals_pre.append(test_coal)
        if len(loosing_coals_pre)  > 0:
            loosing_coals_all.append(loosing_coals_pre)
               
    loosing_coals_all_arr = np.array([np.array(xi) for xi in loosing_coals_all], dtype=object)
    loosing_coals = [] 
    c_bad_luck = 0  
    current_max_length = 0
    
  
    while len(loosing_coals) <  max_overall- 1:
        # print(f"h {c_bad_luck}")
        c_bad_luck = c_bad_luck + 1
        if c_bad_luck % kick_rate == 0:
           # c_bad_luck = 0 
            loosing_coals.pop(rng.integers(0, len(loosing_coals)))
        if c_bad_luck % give_up_rate == 0:
            min_gain = min_gain - 1
            c_bad_luck = 0
            # print("minimizing dis")
        wanted_length_ix = rng.integers(0, len(loosing_coals_all_arr)-1)
        # print(f"{wanted_length_ix} {len(loosing_coals_all)}")
        cand = random.choice(loosing_coals_all_arr[wanted_length_ix])
        for prev in loosing_coals:
            if np.array_equal(prev, cand):
                continue
        min_dist = min_gain
        for elem in loosing_coals:
            d = calc_gain(elem, cand)
            if d < min_dist:
                min_dist = d
                
        # penelty for long words
        min_dist = min_dist + (max_out - (len(staaten.state_names) - len(cand)))
        # penelaty for long wait
            
        if min_dist >= min_gain:
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
                
        