##############################
#                            #
#  PANTELIDIS NIKOS AM 2787  #
#                            #
##############################
from loader import *
from pair_finder import *
import time
import pandas as pd
import json

ratings_path_s = "DATA\\ratings_100users.csv"
ratings_path = "DATA\\ratings_100users.csv"
movies_path =  "DATA\\movies.csv"

MinScore = 4
MaxCombo = 4
MinFrequency = 0.1


ratings_stream = createRatingsStream(ratings_path_s, MinScore)
userBaskets = CreateMovieBaskets(ratings_path, MinScore)
movies_df = ReadMovies(movies_path)


start_time = time.time()
myApriori = myApriori(userBaskets, MinFrequency, MaxCombo)


print("Apriori Time--- %s seconds ---" % (time.time() - start_time))
ca = export_combos(myApriori)


start_time = time.time()
sampledApriori = sampledApriori(50, ratings_stream, MinFrequency, MaxCombo)


print("Sampled Apriori Time--- %s seconds ---" % (time.time() - start_time))
sa = export_combos(sampledApriori)

print(get_scores(ca,sa))
