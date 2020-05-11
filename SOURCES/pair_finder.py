

def get_pairs(basket):
    pair_list = []

    for x in range(1,len(basket)):
        for y in range(x):
            pair_list.append((basket[x], basket[y]))

    return pair_list


def TriangularMatrixOfPairsCounters(movies_df, user_baskets):
    movies_df_size = len(movies_df)
    traingulare_matrix = init_triangular_matrix(movies_df_size)


def init_triangular_matrix(movies_df_size):
    triangular_matrix = []

    for x in range(1,movies_df_size):
        tmp = []

        for y in range(x):
            tmp.append((x,y))

        triangular_matrix.append(tmp)
