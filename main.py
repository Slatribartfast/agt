from itertools import combinations

import staaten
import loosingKoalition
import winningKoalitions

def without(a: list[int], b: list[int]) -> list[int]:
    # a without b
    c = []
    for elem in a:
        if elem not in b:
            c.append(elem)
            
    return(c)            
    


def get_winning_coalitions(input_coal: list[list], special_coalitions : list[list]) -> list[list]:
    # special case 15 (14)
    
    if input_coal[0] in special_coalitions and input_coal[1] in special_coalitions:
        print("CAREFULL, you cant get an winning coal of two special coalitions")
        return[]
    
    if input_coal[0] in special_coalitions:
        # switch em'
        a = input_coal[0].copy()
        b = input_coal[1].copy()
        input_coal[0] = b
        input_coal[1] = a
        
    if input_coal[1] in special_coalitions:
        
        print("the special thing is happening")
               
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
        print("W1 too small")
        return []
    
    # minimal A
    A = A_prev[-(25-len(W_1)):]
    
    
    for elem in A:
        W_1.append(elem)
    
    print(len(W_1))
            
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
        print("w2 has too small number of staates")
        return []
    
    if pop_c < 0.65:
        print("w2 has to little population")
        return []
         
            
    return [W_1,W_2]
    
        

def is_winning(input_coal: list[int]) -> bool:
    if len(input_coal) >= 25:
        print("over 25")
        return True

    if len(input_coal) >= len(staaten.state_names) * 0.55:
        pop_c = 0
        for elem in input_coal:
            pop_c += staaten.state_share[elem]
        print(pop_c)
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




# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    non_sep_loosing_coal = []
    wk = winningKoalitions.winning_coalitions
    lk = loosingKoalition.loosing_coalitions

    # alle permutationen aus loosing in is non sep mit get winning packen
    for i in range(len(lk)-1):
        for j in range(i,len(lk)):
            if i == j:
                continue
            win = get_winning_coalitions(input_coal = [lk[i], lk[j]], special_coalitions=[lk[14]])
            if len(win) < 1:
                continue
            if is_non_separable([lk[i],lk[j]],win):
                non_sep_loosing_coal.append([i, j])
    
    print("die zweier")
    for elem in non_sep_loosing_coal:
        print(elem)
     
    # wenn einer zweier nicht klappt, den erweitern und gegen bekannte winning testen, sonst dicard
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
                    for w_1 in range(len(wk)):
                        for w_2 in range(w_1, len(wk)):
                            for w_3 in range(w_2,len(wk)):
                                if w_1 == w_2:
                                    continue
                                if w_2 == w_3:
                                    continue
                                if w_1 == w_3:
                                    continue
                                if is_non_separable(input_losing_coal=[lk[i],lk[j],lk[k]], winning_coal=[wk[w_1], wk[w_2], wk[w_3]]):
                                    non_sep_loosing_coal.append([i,j,k])
                        
    print("die zweier und dreier")
    for elem in non_sep_loosing_coal:
        print(elem)           
    
    # sammeln aller nicht sep mengen
    # die cover ich jetzt
    
    
    # mange aller mengen kardinalität kleiner gleich der größten von den seperablen, die nicht in den nicht seps stehen
    # pick 7 aus den sep mengen, sodass die vereinigung der sieben alle 15 bekannten grund lossers abdeckt 
    # UND die loosing nicht als Untermenge sind ()
    # UND dürfen sich selsbt nicht beinhalten
    
    # alt variante
    # collect all collections bis max kaardinalität 4
    cover = []
    # einer
    for i in range(len(lk)):
        cover.append([i])
    # zweier
    for i in range(len(lk)):
        for k in range(i+1, len(lk)):
            cover.append([i,k])
    # dreier
    for i in range(len(lk)):
        for j in range(i+1, len(lk)):
            for k in range(j+1, len(lk)):
                cover.append([i,j,k])
                pass
                
    # vierer
    for i in range(len(lk)):
        for j in range(i+1, len(lk)):
            for k in range(j+1, len(lk)):
                for l in range(k+1, len(lk)):
                    cover.append([i,j,k,l])
                    pass
                    

            
    # MINUS die in non sep stehen
    print(all(item in [4,5,6] for item in [4,5]))
    
    cover_2 = cover.copy()
    for c in cover:
        for s in non_sep_loosing_coal:
            if all(item in c for item in s):
                if c in cover_2:
                    cover_2.remove(c)
    
        
    # MINUS die in sich selbst vorkommen (den maximalen behalten, den minimalen kicken)
    cover_3 = cover_2.copy()
    for c in cover_2:
        for s in cover_2:
            if c == s:
                continue
            if all(item in c for item in s):
                if s in cover_3:
                    cover_3.remove(s)
                
    print("cover")
    for elem in cover_3:
        print(elem)          

    
    # falls die max 4 kardinaliät nicht reichte nochmal mit mehr
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
                print(f"There is a cover with {comb} at {exist_cover}")

        
    
    
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
