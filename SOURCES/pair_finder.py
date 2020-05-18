

def get_pairs(basket):
    pair_list = []

    for x in range(1,len(basket)):
        for y in range(x):
            pair_list.append((basket[x], basket[y]))

    return pair_list


def TriangularMatrixOfPairsCounters(movies_df, user_baskets):
    n = len(movies_df)
    tm_size = int(n * (n - 1) / 2)
    triangular_matrix = [0] * tm_size

    for i,b in enumerate(user_baskets):
        b_combos = get_pairs(b)
        print("User: ", i + 1, "/ 100")
        for c in b_combos:
            x = movies_df[movies_df['movieId'] == c[0]].index[0] - 1
            y = movies_df[movies_df['movieId'] == c[1]].index[0]
            
            pos = get_tm_pos((x,y), n)
            triangular_matrix[pos] += 1
    
    return triangular_matrix


def get_tm_pos(pair,n):
    if pair[0] < pair[1]:
        i = pair[0]
        j = pair[1]
    else:
        i = pair[1]
        j = pair[0]
    # This formula
    return int(i * (n - (i + 1) / 2) + j - i -1 )


def HashCountersOfPairs(user_baskets):
    pair_dict = {}

    for b in user_baskets:
        combos = get_pairs(b)
        
        for c in combos:
            combo_key = str(c[0]) + "," + str(c[1])

            if combo_key not in pair_dict.keys():
                pair_dict[combo_key] = 1
            else:
                pair_dict[combo_key] += 1

    return pair_dict
            
        
