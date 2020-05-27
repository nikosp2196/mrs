def get_pairs(basket):
    pair_list = []

    for x in range(1,len(basket)):
        for y in range(x):
            pair_list.append(str(basket[x]) + "," + str(basket[y]))

    return pair_list


def TriangularMatrixOfPairsCounters(movies_df, user_baskets):
    n = len(movies_df)
    tm_size = int(n * (n - 1) / 2)
    # Initialize lower triangular matrix counters
    triangular_matrix = [0] * tm_size 
    
    # This dictionary maps tm positions to pair values
    pos_to_index_map = {} 
    tm_pos = 0
    for j in range(0,n-1):
        for i in range(j+1,n):
            pos_to_index_map[tm_pos] = (i,j)
            tm_pos += 1


    for i,b in enumerate(user_baskets):
        b_combos = get_pairs(b)
        print("User: ", i + 1, "/ 100")
        for c in b_combos:
            tmp = c.split(",")
            tmp_x = int(tmp[0])
            tmp_y = int(tmp[1])
            # Turn movieId to index
            x = movies_df[movies_df['movieId'] == tmp_x].index[0]
            y = movies_df[movies_df['movieId'] == tmp_y].index[0]
            
            pos = get_tm_pos((x,y), n)
            triangular_matrix[pos] += 1
    
    return triangular_matrix, pos_to_index_map


def get_tm_pos(pair,n):
    if pair[0] < pair[1]:
        i = pair[0]
        j = pair[1]
    else:
        i = pair[1]
        j = pair[0]
    # This formula
    return int(i * (n - (i + 1) / 2) + j - i - 1)


def HashCountersOfPairs(movies_df, user_baskets):
    pair_dict = {}

    for i,b in enumerate(user_baskets):
        combos = get_pairs(b)
        print("User: ", i + 1, "/ 100")
        for c in combos:
            #combo_key = f"({c[0]},{c[1]})"

            if c not in pair_dict.keys():
                pair_dict[c] = 1
            else:
                pair_dict[c] += 1

    return pair_dict

###########
# APRIORI #
###########

def myApriori(itemBaskets, min_frequency, max_length):
    L = {}
    C1 = calculate_frequencies(itemBaskets ,len(itemBaskets))
    L[1] = frequency_filter(min_frequency,C1)
    pairs = []
    for i in itemBaskets:
        pairs.append(get_pairs(i))
    C2 = calculate_frequencies(pairs, len(itemBaskets))
    L[2] = frequency_filter(min_frequency, C2)
    
    for i in range(3,max_length + 1):
        tmp_combos = get_combos(itemBaskets, L, i)
        Ci = calculate_frequencies(tmp_combos, len(itemBaskets))
        L[i] = frequency_filter(min_frequency, Ci)
        if len(L[i].keys()) == 0:
            break

    return L


def calculate_frequencies(object_list, N):
    vector_dict = {}

    for b_i in range(len(object_list)):
        for c in object_list[b_i]: # c -> combo
            if c not in vector_dict.keys():
                vector_dict[c] = {"frequency": 1, "baskets" : [b_i]}
            else:
                vector_dict[c]['frequency'] += 1
                vector_dict[c]['baskets'].append(b_i)
    for i in vector_dict.keys():
        vector_dict[i]['frequency'] = vector_dict[i]['frequency'] / N
    
    return vector_dict


def frequency_filter(min_frequency, input_dict):
    
    for i in list(input_dict):
        if input_dict[i]['frequency'] < min_frequency:
            del input_dict[i]
    
    return input_dict


def get_combos(ub, L, k):
    combo_list = []

    for i_b, basket in enumerate(ub): # Iterate the baskets
        print("k:", k,"User: ", i_b + 1, "/ 100")
        combo_list.append([])
        if len(basket) >= k: # Baskets with size less than k can't have k-combo

            for i in basket: # Iterate the objects in the basket

                if i in list(L[1]): # If the object not in L1, it isn't frequent
                    
                    for j in list(L[k-1]): # Iterate the L_k-1 dict which holds the frequenct k-1 combos
                        previous_combo_elements = j.split(",")
                        str_i = str(i)
                        if i_b in L[k-1][j]['baskets'] and str_i not in previous_combo_elements:
                            combo_list[-1].append(create_new_combo(str_i,previous_combo_elements))
                        
            combo_list[-1] = list(dict.fromkeys(combo_list[-1]))
            
    return combo_list
                        

def create_new_combo(new_object, old_combo):
    #combo_objects = old_combo.split(",")
    old_combo.append(new_object)
    final_combo = ""
    combo_to_int = [int(i) for i in old_combo]
    sorted_combo = sorted(combo_to_int, reverse=True)
    for i in sorted_combo:
        final_combo += str(i) + ","

    return final_combo[:-1] 