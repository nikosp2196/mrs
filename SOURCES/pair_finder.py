

def get_pairs(basket):
    pair_list = []

    for x in range(1,len(basket)):
        for y in range(x):
            pair_list.append((basket[x], basket[y]))

    return pair_list


def TriangularMatrixOfPairsCounters(movies_df, user_baskets):
    movies_df_size = len(movies_df)
    triangular_matrix = init_triangular_matrix(movies_df_size)

    for i,b in enumerate(user_baskets):
        combos = get_pairs(b)
        print("User: ", i + 1, "/ 100")
        for c in combos:
            x = movies_df[movies_df['movieId'] == c[0]].index[0] - 1
            y = movies_df[movies_df['movieId'] == c[1]].index[0]
            #print("Pair: ", c, "Index: ", x, y)
            #print(triangular_matrix[x][y])
            triangular_matrix[x][y] += 1
    
    return triangular_matrix



def init_triangular_matrix(movies_df_size):
    triangular_matrix = []

    for x in range(1,movies_df_size):
        tmp = []

        for y in range(x):
            tmp.append(0)
        #print(tmp)
        triangular_matrix.append(tmp)
    return triangular_matrix


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
            
        
