import staaten

loosing_coalitions_pre = [
    [1, 4, 7, 13, 14],
    [2, 3, 6, 13],
    [1, 4, 5, 28],
    [1, 2, 10, 11, 14],
    [1, 3, 8, 11, 15],
    [1, 4, 8, 9, 12],
    [1, 2, 7, 17, 18],
    [1, 5, 6, 16, 18],
    [2, 4, 6, 15, 21],
    [1, 3, 9, 10, 12],
    [3, 4, 5, 20, 22],
    [2, 3, 7, 8, 9],
    [1, 3, 6, 26],
    [2, 3, 5, 19],
    [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
]


loosing_coalitions = []
for i in range(len(loosing_coalitions_pre)):
    array_to_add = []
    for j in range(len(staaten.state_names)):
        if j+1 not in loosing_coalitions_pre[i]:
            array_to_add.append(j)
    loosing_coalitions.append(array_to_add)
