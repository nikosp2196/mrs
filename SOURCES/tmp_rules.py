import pandas as pd
import csv
from loader import *
from pair_finder import *
import time
from random import seed
import keyboard
from random import seed
from random import randint
import math

def generate_rules(input_dict):

    MinConfidence = input_dict['MinConfidence']
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
            
            if confidence >= MinConfidence:
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
                    'lift': get_lift(i_f, c_f),
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


ratings_path_s = "DATA\\ratings.csv"
ratings_path = "DATA\\ratings_100users.csv"
movies_path =  "DATA\\movies.csv"

MinScore = 4
MaxCombo = 4
MinFrequency = 0.1
#ratings_stream = createRatingsStream(ratings_path_s, MinScore)
userBaskets, movie_list = CreateMovieBaskets(ratings_path, MinScore, 1000)
movies_df = ReadMovies(movies_path, movie_list)

myApriori = myApriori(userBaskets, MinFrequency, MaxCombo)



combo = frozenset({1210, 2571, 260, 1198})
combo_size = len(combo)

final_hypothesis =  list(range(1,combo_size))
current_hypothesis = list(range(combo_size - 1))


input_dict = {
    'MinConfidence': 0.5,
    'current_hypothesis': current_hypothesis,
    'final_hypothesis': final_hypothesis,
    'collection': myApriori,
    'ban_set': set(),
    'h_set': set(),
    'rule_id': 1,
    'rules': [],
    'itemset': combo
}

generate_rules(input_dict)

for i in input_dict['ban_set']:
    print(i)

for i in input_dict['rules']:
    print(i['rule_id'], i['rule'], i['confidence'])