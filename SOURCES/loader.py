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
            
            #if len(userBaskets) == limit:
            #    break
        
        return userBaskets#, list(set(movies))


def createRatingsStream(r_path, MinScore):
    ratings_stream = pd.read_csv(r_path)
    ratings_stream = ratings_stream.drop('timestamp', axis='columns') 
    ratings_stream = ratings_stream[ratings_stream['rating'] >= MinScore]
    ratings_stream = ratings_stream.reset_index(drop=True)

    return ratings_stream



def ReadMovies(m_path):
    movies_df = pd.read_csv(m_path)
    #movies_df['genres'] = [i.split(sep="|") for i in movies_df['genres']]
    
    #movies_df = movies_df[movies_df['movieId'].isin(movie_list)].reset_index(drop=True)
    
    return movies_df
