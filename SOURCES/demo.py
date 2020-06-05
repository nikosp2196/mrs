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


ratings_path_s = "DATA\\ratings.csv"
ratings_path = "DATA\\ratings_100users.csv"
movies_path =  "DATA\\movies.csv"

MinScore = 4
MaxCombo = 4
MinFrequency = 0.1
#ratings_stream = createRatingsStream(ratings_path_s, MinScore)
userBaskets, movie_list = CreateMovieBaskets(ratings_path_s, MinScore, 1000)
movies_df = ReadMovies(movies_path, movie_list)


start_time = time.time()
myApriori = myApriori(userBaskets, MinFrequency, MaxCombo)

print("Apriori Time--- %s seconds ---" % (time.time() - start_time))


start_time = time.time()

input_dict = {
            'MinConfidence': 0.5,
            'collection': myApriori,
            'rule_id': 1,
            'rules': []
        }



for i in range(2, MaxCombo):    
    combo_size = i
    final_hypothesis =  list(range(1,combo_size))
    current_hypothesis = list(range(combo_size - 1))

    for c in myApriori[i]:
        
        input_dict['current_hypothesis'] = current_hypothesis
        input_dict['final_hypothesis'] = final_hypothesis
        input_dict['ban_set'] = set()
        input_dict['h_set'] = set()
        input_dict['itemset'] = c

        generate_rules(input_dict)


rules = pd.DataFrame(input_dict['rules'])

#for i in input_dict['rules']:
#    print(i['rule_id'], i['rule'], i['confidence'])

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#    print(rules)
print(rules)


print("Rule Generation Time--- %s seconds ---" % (time.time() - start_time))