import staaten

winning_coalitions_pre = [
    [3, 7, 8, 9, 10, 11, 12, 15],
    [1, 2, 3],
    [1, 2, 7, 14],
    [3, 4, 7, 8, 9],
    [1, 8, 9, 10, 11, 12, 14, 15],
    [1, 3, 8, 9],
    [2, 6, 7, 8, 13],
    [1, 7, 8, 9, 12, 13, 14],
    [1, 3, 10, 11],
    [1, 2, 4],
    [3, 4, 7, 9, 13, 14],
    [1, 7, 10, 11, 13, 14, 17, 18],
    # added by alex
    [1,2,5],
]


winning_coalitions = []
for i in range(len(winning_coalitions_pre)):
    array_to_add = []
    for j in range(len(staaten.state_names)):
        if j+1 not in winning_coalitions_pre[i]:
            array_to_add.append(j)
    winning_coalitions.append(array_to_add)
