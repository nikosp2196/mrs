import pandas as pd
import csv
from loader import CreateMovieBaskets, ReadMovies
from pair_finder import TriangularMatrixOfPairsCounters, HashCountersOfPairs
import time



ratings_path = "SOURCES\\DATA\\ratings_100users.csv"
movies_path =  "SOURCES\\DATA\\movies.csv"
MinScore = 4.5 # CHANGE THIS TO USER INPUT
                 


UserBaskets,movies_list = CreateMovieBaskets(ratings_path,MinScore)
movies_df = ReadMovies(movies_path)

# Keep only the movies that we've found in our baskets and reset the index
movies_df = movies_df[movies_df['movieId'].isin(movies_list)].reset_index(drop=True)

start_time = time.time()
#tm_pair_counters = TriangularMatrixOfPairsCounters(movies_df, UserBaskets)
ub = [
    [0,1,2],
    [1,2,3],
    [0,1,3],
    [1,3,4]
]
hash_pair_counters = HashCountersOfPairs(ub)
for i in hash_pair_counters.keys():
    print("Pair: ", i, "Counter: ", hash_pair_counters[i])
print("--- %s seconds ---" % (time.time() - start_time))