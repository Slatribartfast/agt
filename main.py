from itertools import combinations
import time

import staaten
import loosingKoalition
import calculateLoosingKoalition
from multiprocessing import Process

def without(a: list[int], b: list[int]) -> list[int]:
    # a without b
    c = []
    for elem in a:
        if elem not in b:
            c.append(elem)
            
    return(c)            
    


def get_winning_coalitions(input_coal: list[list], special_coalitions : list[list], lk = loosingKoalition.loosing_coalitions, debug = False) -> list[list]:
    # special case 15 (14)
    # retreiv the numbers for debug prupose
    set_1 = -1
    set_2 = -1
    for i in range(len(lk)):
        if lk[i] == input_coal[0]:
            set_1 = i
        if lk[i] == input_coal[1]:
            set_2 = i
            
    if input_coal[0] in special_coalitions and input_coal[1] in special_coalitions:
        if debug:
            print(f"CAREFULL, you cant get an winning coal of two special coalitions {set_1} and {set_2}")
            print("Therefore this cant be added to non sep non list \n")
        return[]
    
    if input_coal[0] in special_coalitions:
        # switch em'
        a = input_coal[0].copy()
        b = input_coal[1].copy()
        input_coal[0] = b
        input_coal[1] = a
        
    if input_coal[1] in special_coalitions:
        
        # print("the special thing is happening")
               
        dif_i_15 = [] # i ohne 15
        dif_15_i = [] # 15 ohne i
        
        dif_i_15 = without(input_coal[0], input_coal[1])
        dif_15_i = without(input_coal[1], input_coal[0])
        
        W_1 = []
        W_1.append(dif_15_i[0])
        W_1.append(dif_15_i[1])
        for elem in dif_i_15:
            if elem == dif_i_15[-1]:
                continue
            if elem == dif_i_15[-2]:
                continue
            W_1.append(elem)
            
        W_2 = []
        for elem in dif_15_i:
            if elem == dif_15_i[0]:
                continue
            if elem == dif_15_i[1]:
                continue
            W_1.append(elem)
        W_2.append(dif_i_15[-2])
        W_2.append(dif_i_15[-1])
        
        return [W_1,W_2]

        
    
    A_prev = []
    #consruct A maximal (has to be sorted out later, because its minimal)
    for i in range(len(staaten.state_share)):
        if i in input_coal[0] or i in input_coal[1]:
            if i in input_coal[0] and i in input_coal[1]:
                continue
            else:
                A_prev.append(i)
                
    # W1
    W_1 = []
    for i in range(len(staaten.state_share)):
        if i in input_coal[0] and i in input_coal[1]:
            W_1.append(i)
    
    if len(W_1) + len(A_prev) < 25:
        if debug:
            print("W1 too small")
            print(f"Cant contruct winning set for {set_1} and {set_2}")
            print("Therefore this cant be added to non sep non list \n")
        return []
    
    # minimal A
    A = A_prev[-(25-len(W_1)):]
    
    
    for elem in A:
        W_1.append(elem)
    
    
    # W2
    W_2  = []
    for i in range(len(staaten.state_share)):
        if i in input_coal[0] or i in input_coal[1]:
            if i in A:
                continue
            else:
                W_2.append(i)
        
    # test w2
    pop_c = 0.0
    for elem in W_2:
        pop_c += staaten.state_share[elem]
    
    if len(W_2) < 0.55 * len(staaten.state_names):
        if debug:
            print("w2 has too small number of staates")
            print(f"Cant contruct winning set for {set_1} and {set_2}")
            print("Therefore this cant be added to non sep non list \n")
        return []
    
    if pop_c < 0.65:
        if debug:
            print("w2 has to little population")
            print(f"Cant contruct winning set for {set_1} and {set_2}")
            print("Therefore this cant be added to non sep non list \n")
        return []
         
            
    return [W_1,W_2]
    
    
def get_winning_coalitions_larger_two(input_coal: list[list]) -> list[list]:
    l = []
    for coal in input_coal:
        for i in coal:
            l.append(i)
    if len(l) < ((0.55 * len(input_coal)) * len(staaten.state_names)):
        # print("too less states")
        return[]
    
    c = 0
    for i in l:
        c += staaten.state_share[i]
    l.sort()
    w_1 = []
    i = len(l) - 1
    while(not is_winning(w_1)):
        if i == 0:
            # print("no win")
            return[]
        if l[i] not in w_1:
            w_1.append(l.pop(i))
        i = i - 1
        
    w_2 = []
    i = len(l) - 1
    while(not is_winning(w_2)):
        if i == 0:
            # print("just one win")
            return[]
        if l[i] not in w_2:
            w_2.append(l.pop(i))
        i = i - 1
        
    if is_winning(l):
        return [w_1,w_2,l]
    else:
        # print("just two win")
        return[]

    

def is_winning(input_coal: list[int]) -> bool:
    if len(input_coal) >= 25:
        # print("over 25")
        return True

    if len(input_coal) >= len(staaten.state_names) * 0.55:
        pop_c = 0
        for elem in input_coal:
            pop_c += staaten.state_share[elem]
        # print(pop_c)
        if pop_c >= 0.65:
            return True
    return False


def is_non_separable(input_losing_coal: list[list], winning_coal: list[list]) -> bool:
    if len(winning_coal) < len(input_losing_coal):
        print("Requirement lemma 2 not satisfied")
        return False
    for i in range(len(staaten.state_names)):
        los = 0
        win = 0
        for i_los in input_losing_coal:
            if i in i_los:
                los += 1
        for i_win in winning_coal:
            if i in i_win:
                win += 1
        if win > los:
            return False
    return True


def get_cover(lk = loosingKoalition.loosing_coalitions, debug = True) -> int:
    
    res = -1
    time_before = time.time()
    non_sep_loosing_coal = []

    # alle permutationen aus loosing in is non sep mit get winning packen
    for i in range(len(lk)-1):
        for j in range(i,len(lk)):
            if i == j:
                continue
            win = get_winning_coalitions(input_coal = [lk[i], lk[j]], special_coalitions=[lk[-1]], lk=lk)
            if len(win) < 1:
                continue
            if is_non_separable([lk[i],lk[j]],win):
                non_sep_loosing_coal.append([i, j])
    
    # print("die zweier")
    # for elem in non_sep_loosing_coal:
    #     print(elem)
     
    # wenn einer zweier nicht klappt, den erweitern und gegen bekannte winning testen, sonst dicard
    # vierer machen hier macht keinen sinn, da es später eh schon keine vierer gibt, dann können mithilfe von non sep vierer auch später keine gekickt werden
    for i in range(len(lk)-1):
        for j in range(i,len(lk)):
            if [i,j] not in non_sep_loosing_coal:
                for k in range(j,len(lk)):
                    if i == j:
                        continue
                    if j == k:
                        continue
                    if i == k:
                        continue
                    
                    wins = get_winning_coalitions_larger_two([lk[i],lk[j],lk[k]])
                    if len(wins) > 0:
                        if is_non_separable(input_losing_coal=[lk[i],lk[j],lk[k]], winning_coal=wins):
                            non_sep_loosing_coal.append([i,j,k])        
                        
    # print("die zweier und dreier")
    # for elem in non_sep_loosing_coal:
    #     print(elem)           
    
    # sammeln aller nicht sep mengen

    # collect all collections bis max kaardinalität 4 (man kann sehen, dass alle vierer gekickt werden, deshalb müssen auch keine fünfer gesucht werden)
    cover = []
    # einer reinwerfen
    for i in range(len(lk)):
        cover.append([i])
    # zweier reinwerfen
    for i in range(len(lk)):
        for k in range(i+1, len(lk)):
            cover.append([i,k])
    # dreier reinwerfen
    for i in range(len(lk)):
        for j in range(i+1, len(lk)):
            for k in range(j+1, len(lk)):
                cover.append([i,j,k])
                pass
                
    # vierer reinwerfen
    for i in range(len(lk)):
        for j in range(i+1, len(lk)):
            for k in range(j+1, len(lk)):
                for l in range(k+1, len(lk)):
                    cover.append([i,j,k,l])
                    pass
                
    # fünfer reinwerfen
    for i in range(len(lk)):
        for j in range(i+1, len(lk)):
            for k in range(j+1, len(lk)):
                for l in range(k+1, len(lk)):
                    for m in range(l+1, len(lk)):
                        cover.append([i,j,k,l,m])
                        pass
                    

            
    # MINUS die in non sep stehen (wird dann cover 2 genennt)
    # print(all(item in [4,5,6] for item in [4,5]))
    
    cover_2 = cover.copy()
    for c in cover:
        for s in non_sep_loosing_coal:
            if all(item in c for item in s):
                if c in cover_2:
                    cover_2.remove(c)
    
        
    # MINUS die in sich selbst vorkommen (den maximalen behalten, den minimalen kicken) (wird dann cover 3 genannt) 
    cover_3 = cover_2.copy()
    for c in cover_2:
        for s in cover_2:
            if c == s:
                continue
            if all(item in c for item in s):
                if s in cover_3:
                    cover_3.remove(s)
                
    # print("cover")
    # for elem in cover_3:
    #     print(elem)          

    
    # falls die max 4 kardinaliät nicht reichte nochmal mit mehr (wird bisher nicht gemacht, nur problem gecalled)
    saveing = []
    for elem in cover_3:   
        if len(elem) > 4:
            if debug:
                print("Es gibt 5er cover, das nicht gekickt werden -> es müssen dann auch fünfer betrachtet werden, sonst gilt der Beweis nicht")
                print(f"unkickbar {elem} aus \n")
                for ding in non_sep_loosing_coal:
                    print(ding)
            saveing.append(elem)   
    if len(saveing) > 0:
        if len(lk) < 8:
            return -1
        else:
            pr = []
            for elem in saveing:
                for i in elem:
                    pr.append(i)
            most_common = max(pr, key = pr.count)
            if most_common == (len(lk)-1):
                return []
            # print("stay")
            lk.pop(most_common)
            return get_cover(lk=lk,debug=debug)
#
    # step 2 keine 7 verschiedene daraus als vereinigugn ergibt das gesamte L1 bis L15
    exist_cover = 0
    is_covering = False
    while(not is_covering):
        exist_cover += 1
        bool_list = []
        cover_ideas_bool = []
        for positions in combinations(range(len(cover_3)), exist_cover):
            p = [0] * len(cover_3)

            for i in positions:
                p[i] = 1
            cover_ideas_bool.append(p)
            
        for comb in cover_ideas_bool:
            combined = []
            for i in range(len(comb)):
                if comb[i]:
                    for to_add in cover_3[i]:
                        if to_add not in combined:
                            combined.append(to_add)
            if len(combined) >= len(lk):
                is_covering = True
                if debug:
                    print(f"There is a cover with {comb}, especially the sets \n")
                    for set_of_seps in range(len(cover_3)):
                        if comb[set_of_seps]:
                            print(cover_3[set_of_seps]) 
                
                    print(f"\nSo there is no {exist_cover-1} cover, somit ist die Dimension mindestens {exist_cover-1}")
                res = exist_cover-1
                break
    if debug:
        print(f"The process time was {time.time() - time_before:.2f}s")
    return res


def a_process_for_parallel_execution(name ="file.txt", max_out=5, max_overall=12, min_gain=6, kick_rate=500, give_up_rate=100000,id = -1):  
    print("go")
    best = 0
    tries = 0            
    while(True):  
        tries += 1
        if True:
            if tries % 10 == 0:
                print(f"max_overall: {max_overall}, tries: {tries}")
        lk = calculateLoosingKoalition.get_loosing_coals(max_out, max_overall, min_gain, kick_rate, give_up_rate)
        res = get_cover(lk = lk, debug = False)
        if res > 4:
            best = res
            print(best)
            with open(name, 'a') as f: 
                f.write(str(best)+ "\n")
                f.write(f"process id {id}\n")
                f.write("stats\n")
                f.write(f"{max_out}, {max_overall}, {min_gain}, {kick_rate}, {give_up_rate}\n")
                f.write(str(time.strftime("%Y%m%d-%H%M%S")))
                f.write("\nloosing coalitions taken\n")
                for elem in lk:
                    f.write(str(staaten.make_readable_alla_paper(elem)) + "\n")
                f.write("\n")
                f.write("\n")
                f.flush()
    


if __name__ == '__main__':
    
    # res = get_cover(lk = calculateLoosingKoalition.get_loosing_coals())
    
    if True:   
        proc = []
        num_loosing = [25,25,24,24,23,23,23,23,22,22,22,22,21,21,20,20]
        num_min_gain = [6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7]
        timestr = time.strftime("%Y%m%d-%H%M%S")
        name = "results"+timestr+".txt"
        with open(name, 'w') as f: 
                    f.write("Results\n\n")
                    f.flush()

        for i in range(len(num_loosing)):         
            proc.append(Process(target=a_process_for_parallel_execution, args=(name,5, num_loosing[i], num_min_gain[i], 1000, 100000,i))) 
            proc[-1].start()
            time.sleep(0.1)
        for i in range(len(proc)):       
            proc[i].join() 
            

        

    
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
