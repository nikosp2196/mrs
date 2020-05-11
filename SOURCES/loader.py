import pandas as pd
import csv


def CreateMovieBaskets(r_path, MinScore):
    userBaskets = []
    movies = []
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
                movies.append(movieId)
        
        return userBaskets, list(set(movies))


def ReadMovies(m_path):
    movies_df = pd.read_csv(m_path)
    movies_df['genres'] = [i.split(sep="|") for i in movies_df['genres']]
    #print(movies_df.head())

    return movies_df