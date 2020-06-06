
import time
import keyboard
from random import seed
from random import randint
import pandas as pd

def get_pairs(basket):
    pair_list = []

    for x in range(1,len(basket)):
        for y in range(x):
            pair_list.append(frozenset([basket[x], basket[y]]))

    return pair_list


def TriangularMatrixOfPairsCounters(movies_df, user_baskets):
    n = len(movies_df)
    tm_size = int(n * (n - 1) / 2)

    # Initialize lower triangular matrix counters
    triangular_matrix = [0] * tm_size 

    for i,b in enumerate(user_baskets):
        b_combos = get_pairs(b)
        print("User: ", i + 1, "/ 100")
        for c in b_combos:
            
            pos = get_tm_pos((c[0],c[1]), movies_df)
            triangular_matrix[pos] += 1
    
    return triangular_matrix


def get_tm_pos(m_pair, movies_df):
    n = len(movies_df)
    m_index_1 = movies_df[movies_df['movieId'] == m_pair[0]].index[0]
    m_index_2 = movies_df[movies_df['movieId'] == m_pair[1]].index[0]
    pair = (m_index_1, m_index_2)
    if pair[0] < pair[1]:
        i = pair[0]
        j = pair[1]
    else:
        i = pair[1]
        j = pair[0]
    # This formula
    return int(i * (n - (i + 1) / 2) + j - i - 1)


def HashCountersOfPairs(user_baskets):
    pair_dict = {}

    for i,b in enumerate(user_baskets):
        combos = get_pairs(b)
        print("User: ", i + 1, "/ 100")
        for c in combos:
            
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
    n_baskets = len(itemBaskets)

    L[1] = calculate_frequencies(itemBaskets, n_baskets)
    frequency_filter(min_frequency,L[1])
    print(1,"--------------------->",len(L[1].keys()))
    pairs = []
    for i in itemBaskets:
        pairs.append(get_pairs(sorted(i)))

    L[2] = calculate_frequencies(pairs, n_baskets)
    frequency_filter(min_frequency, L[2])
    print(2,"--------------------->",len(L[2].keys()))
    
    i = 3
    while i <= max_length and len(L[i-1].keys()) != 0:
        tmp_combos = get_combos(itemBaskets, L, i)
        L[i] = calculate_frequencies(tmp_combos, n_baskets)
        frequency_filter(min_frequency, L[i])
        print(i,"--------------------->",len(L[i].keys()))
        i += 1

    return L


def calculate_frequencies(object_list, N):
    vector_dict = {}

    for b_i in range(len(object_list)):
        for ce in object_list[b_i]:
            
            if type(ce) == int:
                c = frozenset([ce])
            else:
                c = ce

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



def get_combos(ub, L, k):
    combo_list = []

    for i_b, basket in enumerate(ub): # Iterate the baskets
        #print("k:", k,"User: ", i_b + 1, "/", len(ub))
        combo_list.append(set())
        if len(basket) >= k: # Baskets with size less than k can't have k-combo

            for i in basket: # Iterate the objects in the basket
                i_set = {i}
                if i_set in list(L[1]): # If the object not in L1, it isn't frequent
                    #print("L[1] check!")
                    for previous_combo in list(L[k-1]): # Iterate the L_k-1 dict which holds the frequenct k-1 combos
                        # i_b: index of user_basket
                        # previous_combo: key of the L[k-1]
                        if i_b in L[k-1][previous_combo]['baskets'] and i not in previous_combo:
                            #print("COMBO GENERATOR check!")
                            # combo_list[-1].add(create_new_combo(i,previous_combo))
                            combo_list[-1].add(previous_combo.union(i_set))
                        
            #combo_list[-1] = list(set(combo_list[-1]))
            
    return combo_list
                        

'''def create_new_combo(new_object, old_combo):
    combo_list = list(old_combo)
    combo_list.append(new_object)
    sorted_combo = sorted(combo_list, reverse=True)
    
    return tuple(sorted_combo) '''


###################
# SAMPLED APRIORI #
###################

def sampledApriori(sample_size, ratings_stream, min_frequency, max_length):
    print("========FIRST EXECUTION OF SAMPLED APRIORI========")
    combos_1, key_stopped = run_apriori(sample_size, ratings_stream, min_frequency, max_length, key_enabled=True)
    
    if key_stopped:
        return combos_1
    
    print("========SECOND EXECUTION OF SAMPLED APRIORI=======")
    combos_2, key_stopped = run_apriori(sample_size, ratings_stream, min_frequency, max_length)
    fp_counter = 0
    for l in range(1,max_length):
        l_combos = list(combos_1[l].keys())
        for i in l_combos:
            if i not in combos_2[l].keys():
                del combos_1[l][i]
                fp_counter += 1
    print(f"*** {fp_counter} false-positives were removed in the second execution.")
    
    return combos_1


def run_apriori(sample_size, ratings_stream, min_frequency, max_length, key_enabled=False):
    SetOfUsers = [] # User so far
    sampleOfBaskets = {} # Key: userId, Value: movie_basket
    sample_map = [] # Mapping between sample index and userId
    stream_size = len(ratings_stream)

    key_pressed = False
    for i in range(stream_size):
        print(f'Reading rating {i} / {stream_size}', end='\r')

        if key_enabled and (keyboard.is_pressed('y') or keyboard.is_pressed('Y')) and len(sampleOfBaskets) == sample_size:
            key_pressed = True
            break
        else:
            current_assessment = ratings_stream.iloc[i]
            current_user = int(current_assessment['userId'])
            current_movie = int(current_assessment['movieId'])

            if current_user not in SetOfUsers:
                SetOfUsers.append(current_user)
                #sampleOfBaskets, sample_map = 
                reservoir_sampling(len(SetOfUsers), sample_size, sampleOfBaskets, sample_map, current_user)

            if current_user in sampleOfBaskets.keys():
                sampleOfBaskets[current_user].append(current_movie)
    
    combos = myApriori(list(sampleOfBaskets.values()), min_frequency, max_length)
    #combos = export_combos(combos_dict)


    return combos, key_pressed


def reservoir_sampling(n_distinct_users, sample_size, sample_of_baskets, sample_map, current_user):
    seed()
    if n_distinct_users <= sample_size:
        sample_of_baskets[current_user] = []
        sample_map.append(current_user)
    else:
        tmp = randint(0, n_distinct_users)

        if tmp < sample_size:
            old_user = sample_map[tmp]
            sample_map[tmp] = current_user
            del sample_of_baskets[old_user]
            sample_of_baskets[current_user] = []
            
    #return sample_of_baskets, sample_map


def export_combos(combos_dict):
    combos = []
    for i in combos_dict.keys():
        for j in combos_dict[i].keys():
            combos.append(j)
    return combos

###########
# SCORING #
###########

def get_scores(classic_apriori, sampled_apriori):
    tp = []
    fp = []
    fn = []
    for i in classic_apriori:
        if i in sampled_apriori:
            tp.append(i)
        else:
            fn.append(i)
    for i in sampled_apriori:
        if i not in classic_apriori:
            fp.append(i)
    tp = len(tp)
    fp = len(fp)
    fn = len(fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * (precision * recall) / (precision + recall)

    results = {
        "tp" : tp,
        "fp" : fp,
        "fn" : fn,
        "precision" : precision,
        "recall" : recall,
        "f1" : f1
    }
    return results

#########
# RULES #
#########

def rule_generator(combos, min_confidence, min_lift, max_lift):
    MaxCombo = max(combos.keys())

    input_dict = {
            'MinConfidence': min_confidence,
            'MinLift': min_lift,
            'MaxLift': max_lift,
            'collection': combos,
            'rule_id': 1,
            'rules': []
        }

    for i in range(2, MaxCombo):    
        combo_size = i
        final_hypothesis =  list(range(1,combo_size))
        current_hypothesis = list(range(combo_size - 1))

    for c in combos[i]:
        
        input_dict['current_hypothesis'] = current_hypothesis
        input_dict['final_hypothesis'] = final_hypothesis
        input_dict['ban_set'] = set()
        input_dict['h_set'] = set()
        input_dict['itemset'] = c

        generate_rules(input_dict)


    rules = pd.DataFrame(input_dict['rules'])

    return rules

def generate_rules(input_dict):

    MinConfidence = input_dict['MinConfidence']
    MinLift = input_dict['MinLift']
    MaxLift = input_dict['MaxLift']
    current_h = input_dict['current_hypothesis']
    final_h = input_dict['final_hypothesis']
    itemset_fs = input_dict['itemset']
    itemset_l = sorted(list(itemset_fs))
    set_size = len(itemset_l)
    h_size = len(current_h)
    c_size = set_size - h_size
    while True:
        h = frozenset([itemset_l[i] for i in current_h])
        c = itemset_fs.difference(h)
        if h not in input_dict['h_set'] and c not in input_dict['ban_set']:
            i_f = input_dict['collection'][set_size][itemset_fs]['frequency']
            h_f = input_dict['collection'][h_size][h]['frequency']
            c_f = input_dict['collection'][c_size][c]['frequency']
            confidence = get_confidence(i_f, h_f)
            lift = get_lift(i_f, c_f)
            
            if confidence >= MinConfidence and \
            (lift >= MinLift or MinLift == -1) and \
            (lift <= MaxLift or MaxLift == -1):
                #print(input_dict['rule_id'])
                # Append
                h_sl = sorted(list(h))
                c_sl = sorted(list(c))
                tmp_rule = {
                    'itemset': itemset_l,
                    'rule': f"{h_sl}-->{c_sl}",
                    'hypothesis': h_sl,
                    'conclusion': c_sl,
                    'frequency': i_f,
                    'confidence': confidence,
                    'lift': lift,
                    'interest': get_interest(i_f, c_f),
                    'rule_id': input_dict['rule_id']
                }

                input_dict['rules'].append(tmp_rule)
                input_dict['h_set'].add(h)
                input_dict['rule_id'] += 1
                
                if len(current_h) > 1:
                    # Generate rules with smaller hypothesis
                    input_dict['current_hypothesis'] = current_h[:-1]
                    input_dict['final_hypothesis'] = current_h[1:]
                    generate_rules(input_dict)
            else:
                input_dict['ban_set'].add(c)
        
        if next_hypothesis(current_h, final_h) == -1:
            break


def next_hypothesis(current, final):
    h_size = len(current)
    pointer = h_size - 1
    if current == final:
        #print("Already at final hypothesis!!")
        return -1
    #print(h_size)
    while True:
        if current[pointer] != final[pointer]:
        
            current[pointer] += 1
            for i in range(pointer + 1, h_size):
                current[i] = current[i-1] + 1
            break
        else:
            pointer -= 1


def get_confidence(itemset_f, hypothesis_f):
    return itemset_f / hypothesis_f


def get_lift(rule_confidence, conclusion_f):
    return rule_confidence / conclusion_f


def get_interest(rule_confidence, conclusion_f):
    return rule_confidence - conclusion_f