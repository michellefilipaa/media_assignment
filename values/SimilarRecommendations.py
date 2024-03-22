"""
This file arranges the data in the `all_data.csv` file in such a way that 
the content most similar to each user is placed at the top.
"""
import functools
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import streamlit as st

df = pd.read_csv('../data/all_data.csv')
# Calculate the diversity score
similarities_df = pd.read_csv('../data/all_data_similarity.csv')

# Gets similarity scores for all other movies
def get_similarities(movie_index):
    similarities = similarities_df.loc[movie_index]
    # similarities.drop(movie_index, inplace=True)
    return similarities.rename('similarity').to_frame()

# Scales relevant features to domain [0, 1]
def scale_features(movie_df):
    scaler = MinMaxScaler((0,1))
    scaler.fit(movie_df.similarity.to_frame())
    movie_df['similarity_scaled'] = scaler.transform(movie_df.similarity.to_frame())
    scaler.fit(movie_df.diversity.to_frame())
    movie_df['diversity_scaled'] = scaler.transform(movie_df.diversity.to_frame())
    return movie_df

# Calculates weighter average for relevant (scaled) features
def weighted_score(movie, similarity_weight, diversity_weight):
    sw = movie ['similarity_scaled'] * similarity_weight
    dw = movie['diversity_scaled'] * diversity_weight
    total_weights = similarity_weight + diversity_weight
    return (sw + dw) / total_weights

# recommmends the movies + uses function from above
def recommend_movies(movie_index, diversity_factor=0.5, similarity_factor=1):
    # Filter movies with the sentiement thats is given in streamlit
    filtered_df = df[df['vader_sentiment'] == st.session_state.polarity] 
    similarities = get_similarities(movie_index)
    # DataFrame with relevant features for filtered movies
    movie_df = filtered_df.join(similarities)
    movie_df = scale_features(movie_df)
    # Calculate the weighted score
    weight_func = functools.partial(weighted_score, 
                                    similarity_weight=similarity_factor,
                                    diversity_weight=diversity_factor)
    movie_df['recommender_score'] = movie_df.apply(weight_func, axis='columns')
    return movie_df.sort_values('recommender_score', ascending=False)