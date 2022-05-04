import json

import numpy as np
import pandas as pd
from pandas import Series

meta = pd.read_csv("movies_metadata.csv")

meta = meta[["id", "original_title", "original_language", "genres"]]
meta = meta.rename(columns={"id": "movieId"})
meta = meta[meta["original_language"] == 'en']

print("=== MOVIES HEAD ===")
print(meta.head())
print("\n\n")


ratings = pd.read_csv('ratings_small.csv')
ratings = ratings[["userId", "movieId", "rating"]]

print("=== RATINGS HEAD ===")
print(ratings.head())
print("\n\n")


print("=== DESCRIBE ===")
print(ratings.describe())
print("\n\n")

meta.movieId = pd.to_numeric(meta.movieId, errors='coerce')
ratings.movieId = pd.to_numeric(ratings.movieId, errors='coerce')


def parse_genres(genres_str):
    genres = json.loads(genres_str.replace('\'', '"'))

    genres_list = []
    for g in genres:
        genres_list.append(g['name'])

    return genres_list


meta['genres'] = meta['genres'].apply(parse_genres)

print("=== CHECK GENRES HAVE BEEN UPDATED PROPERLY ===")
print(meta["genres"].head())
print("\n\n")


matrix_p = pd.merge(meta, ratings, on="movieId", how="inner")
print("=== CHECK DATA JOINED BY META AND RATINGS.. ===")
print(matrix_p.head())
print("\n\n")


print("=== WILL PIVOT TO MAKE DATA THE FOLLOWING WAY. ===")
print("       영화1, 영화2, 영화3, 영화4, ... 영화 N")
print("user1   0    3.5   0     0     ...  4")
print("user2   4.5   0    0     0     ...  0")
print("user3   0    3.5   0     0     ...  0")
print("user4   0     0    0     1     ...  5")
print("\n\n")


# matrix = pd.read_csv("matrix.csv")
matrix = matrix_p.pivot_table(index="userId", columns="original_title", values="rating")

print("=== CHECK DATA PIVOTED.. ===")
print(matrix[:5])
print("\n\n")


def pearsonR(s1: Series, s2: Series):
    """피어슨 스코어"""
    s1_c = s1 - s1.mean()  # 미리 계산 및 배열 저장 가능
    s2_c = s2 - s2.mean()  # 미리 계산 및 배열 저장 가능
    m = np.sum(s1_c * s2_c)  # faiss product

    # 제곱 값 역시 미리 계산 및 배열 저장 가능
    # faiss 로 product 시 faster.
    d = np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))
    return m / d if d else 0


def recommend(input_movie, m, n, similar_genre=True, genre_weight=0.1):

    movie_meta = meta[meta["original_title"] == input_movie]
    input_genres = movie_meta["genres"].iloc(0)[0]

    result = []
    for title in m.columns:

        # rating comparison
        cor = pearsonR(matrix[input_movie], matrix[title])

        if float(cor) <= 0:
            continue

        current_move_genres = meta[meta["original_title"] == title]["genres"].iloc(0)[0]

        # additional genre score calculation
        if similar_genre and len(input_genres) > 0:
            same_count = np.sum(np.isin(input_genres, current_move_genres))
            cor += (genre_weight * same_count)

        if np.isnan(cor):
            continue

        result.append((title, "{:.2f}".format(cor), current_move_genres))

    result.sort(key=lambda x: x[1], reverse=True)
    return result[:n]


print("=== CALCULATING RECOMMENDATION.. ===")
recommend_result = recommend("The Dark Knight", matrix, 5, similar_genre=True, genre_weight=0.1)

print(pd.DataFrame(recommend_result, columns=["title", "correlation", "genres"]))

print("BYE~")
