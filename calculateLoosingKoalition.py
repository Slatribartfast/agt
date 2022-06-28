import staaten
import main

from itertools import combinations
import random

def get_loosing_coals(max_out: int = 5, max_overall: int = 15)-> list[list]:
    loosing_coals_all = []
    for i in range(max_out + 1):
    
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
                loosing_coals_all.append(test_coal)
                

    loosing_coals = random.sample(loosing_coals_all, max_overall-1)
                
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
    for elem in get_loosing_coals(4):
        invert_to_readable = []
        for i in range(len(staaten.state_names)):
            if i in elem:
                pass
            else:
                invert_to_readable.append(i+1)
        print(invert_to_readable)
                
        