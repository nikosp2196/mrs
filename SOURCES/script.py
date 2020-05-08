import pandas as pd
import csv

ratings_path = "SOURCES\\DATA\\ratings_100users.csv"
movies_path =  "SOURCES\\DATA\\movies.csv"

MinScore = 4.5 # CHANGE THIS TO USER INPUT

def CreateMovieBaskets(r_path):
    userBaskets = []

    with open(r_path) as infile:
        ratings_reader = csv.reader(infile, delimiter=',')

        next(ratings_reader)
        current_userId = 0
        for i in ratings_reader:
            userId, movieId, rating = int(i[0]), int(i[1]), float(i[2])

            if current_userId != userId:
                userBaskets.append([])
                current_userId = userId

            if rating >= MinScore:
                userBaskets[-1].append(movieId)
        
        return userBaskets


def ReadMovies(m_path):
    movies_df = pd.read_csv(m_path)
    movies_df['genres'] = [i.split(sep="|") for i in movies_df['genres']]
    print(movies_df.head())

    return movies_df


def TriangularMatrixOfPairsCounters(movies_df):
    triangular_pair_counters = []
    
    # Triangular Matrix of Pairs initialization
    for i in range(1,10):
        tmp = []
        for j in range(i):
            tmp.append(0)
        print(tmp)
        triangular_pair_counters.append(tmp)
                 

def get_pairs(basket):
    for i in range(len(basket)):
        tmp = []
        for j in range(i+1, len(basket)):
            tmp.append((i,j))
        print(tmp)

UserBaskets = CreateMovieBaskets(ratings_path)
get_pairs(UserBaskets[0])




#movies_df = ReadMovies(movies_path)
#TriangularMatrixOfPairsCounters(movies_df)