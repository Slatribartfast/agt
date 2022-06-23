# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import staaten
import loosingKoalition
import winningKoalitions


def get_winning_coalitions(input_coal: list[list]) -> list[list]:
    # special case 15 (14)
    if input_coal[0] == loosingKoalition[14]:
        print("should never happen")
        
    if input_coal[1] == loosingKoalition[14]:  
        dif_i_15 = [] # i ohne 15
        dif_15_i = [] # 15 ohne i
        
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

        
    
    A = []
    #consruct A
    for i in range(len(staaten.state_share)):
        if i in input_coal[0] or i in input_coal[1]:
            if i in input_coal[0] or i in input_coal[1]:
                continue
            else:
                A.append(i)
                
    
    # W1
    W_1 = []
    for elem in A:
        W_1.append(elem)
    
    for i in range(len(staaten.state_share)):
        if i in input_coal[0] and i in input_coal[1]:
            W_1.append(i)
            
         
    if len(W_1) < 25:
        print("W1 too small")
        return []
            
    # W2
    W_2  = []
    for i in range(len(staaten.state_share)):
        if i in input_coal[0] and i in input_coal[1]:
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


c = 0.0
for elem in staaten.state_share:
    c += elem
print(c)

c_pop = 0
for i in range(len(staaten.state_share)):
    if i < 3:
        continue
    c_pop = c_pop + staaten.state_share[i]
print(c_pop)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    wk = winningKoalitions.winning_coalitions
    lk = loosingKoalition.loosing_coalitions
    test_bool = is_non_separable([lk[0], lk[1], lk[11]], [wk[1], wk[6], wk[10]])
    print(test_bool)
    # alle permutationen aus loosing in is non sep mit get winning packen
    # res müsste im paper sein
    
    # wenn einer zweier nicht klappt, den erweitern und gegen bekannte winning testen, sonst dicard
    
    # sammeln aller nicht sep mengen
    # die cover ich jetzt
    
    
    # mange aller mengen kardinalität kleiner gleich der größten von den seperablen, die nicht in den nicht seps stehen
    # pick 7 aus den sep mengen, sodass die vereinigung der sieben alle 15 bekannten grund lossers abdeckt 
    # UND die loosing nicht als Untermenge sind ()
    # UND dürfen sich selsbt nicht beinhalten
    
    # alt variante
    # collect all collections bis max kaardinalität 4
    # MINUS die in non sep stehen
    # MINUS die in sich selbst vorkommen (den maximalen behalten, den minimalen kicken)
    # falls die max 4 kardinaliät nicht reichte nochmal mit mehr
    #
    # step 2 keine 7 verschiedene daraus als vereinigugn ergibt das gesamte L1 bis L15
    
    
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
