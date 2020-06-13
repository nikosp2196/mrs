##############################
#                            #
#  PANTELIDIS NIKOS AM 2787  #
#                            #
##############################
from pair_finder import TriangularMatrixOfPairsCounters, HashCountersOfPairs
from loader import ReadMovies, CreateMovieBaskets
import time


ratings_path = "DATA\\ratings_100users.csv"
movies_path =  "DATA\\movies.csv"
MinScore = 4


user_baskets = CreateMovieBaskets(ratings_path,MinScore)
movies_df = ReadMovies(movies_path)


'''start_time = time.time()

triangular_matrix = TriangularMatrixOfPairsCounters(movies_df, user_baskets)

tm_time = time.time() - start_time
print("TRIANGULAR MATRIX PAIR GENERATOR --->", tm_time, 'sec')

count = 0
for i in triangular_matrix:
    if i != 0:
        count += i

print("TM PAIRS:",count)'''

start_time = time.time()

hash_pair_counters = HashCountersOfPairs(user_baskets)

hash_time = time.time() - start_time
print("HASH PAIR GENERATOR --->", hash_time, 'sec')

count = 0
for i in hash_pair_counters.keys():
    count += hash_pair_counters[i]

print("HASH PAIRS:", count)