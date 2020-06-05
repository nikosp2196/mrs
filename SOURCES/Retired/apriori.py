import pandas as pd
import csv
from loader import *
from pair_finder import *
import time
from random import seed
import keyboard
from random import seed
from random import randint


ratings_path_s = "DATA\\ratings_100users_shuffled.csv"
ratings_path = "DATA\\ratings_100users.csv"
movies_path =  "DATA\\movies.csv"

MinScore = 4
MaxCombo = 4
MinFrequency = 0.1
start_time = time.time()
ratings_stream = createRatingsStream(ratings_path_s, MinScore)
userBaskets, movie_list = CreateMovieBaskets(ratings_path, MinScore, 1000)
movies_df = ReadMovies(movies_path, movie_list)
print("Loading Time--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
myApriori = myApriori(userBaskets, MinFrequency, MaxCombo)
c_combos = export_combos(myApriori)
print("Classic Apriori Time--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
s_combos = sampledApriori(50, ratings_stream, MinFrequency, MaxCombo)
print("Sampled Apriori Time--- %s seconds ---" % (time.time() - start_time))
print(get_scores(c_combos, s_combos))