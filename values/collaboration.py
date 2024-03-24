#!/usr/bin/env python
# coding: utf-8

# # Collaboration

# In[1]:


import numpy as np
import itertools
import pandas as pd
import warnings
import os
warnings.filterwarnings('ignore')


# In[2]:


user_ratings = pd.read_csv('../data/user_ratings.csv')
movies = pd.read_csv('../data/all_data.csv')


# In[3]:


df = pd.merge(user_ratings, movies, on='showId', how='left')
genres = df['category'].str.get_dummies('|')
df = pd.concat([df, genres], axis=1)
df = df[['userId', 'showId', 'rating', 'CBBC', 'Comedy', 'Documentaries', 'Entertainment', 'From the Archives', 'Science & Nature', 'Sports']]


# # Collaborative filtering (Jaccard similarity)
# In the function below the jaccard similarity is written based on the ratings of the users

# In[11]:


def get_jaccard_recommendations(user_ids, df, movies):
    users = df.groupby('userId')['showId'].apply(set)
    
    group_movies = set()
    for user_id in user_ids:
        group_movies.update(users.get(user_id, set()))
    
    similar_users = []
    new_content = set()  # Use set to store unique recommended items

    for user, value in users.items():
        if user in user_ids:
            continue
        
        other_user_set = value
        
        # Calculate Jaccard similarity for each user separately
        intersection = len(group_movies.intersection(other_user_set))
        union = len(group_movies.union(other_user_set))
        user_similarity = float(intersection) / union

        # Tweak this parameter. Closer to 0.0 is more similar.
        if user_similarity < 0.1 and user_similarity != 0.00:
            differences = group_movies.symmetric_difference(other_user_set)
            new_content.update(differences)  

            # Add the user to similar_users
            similar_users.append(user)
            
            if len(similar_users) >= 15:  # Limit to 10 similar users
                break
    
    # Create DataFrame with unique recommended show IDs
    df_recommendations = pd.DataFrame(list(new_content), columns=['showId'])
    
    # Merge recommendations DataFrame with movies DataFrame based on showId
    df_recommendations_with_info = pd.merge(df_recommendations, movies, on='showId', how='left')
    
    # Define the directory path
    directory = "../data/recommendations"
    
    # Concatenate user IDs without the suffix _1 to form the CSV file name
    users_concatenated = "_".join(user_id.split("_")[0] for user_id in user_ids)
    
    # Use the defined directory path and concatenated user IDs to save recommendations to CSV
    csv_file_path = os.path.join(directory, "collaboration_" + users_concatenated + ".csv")
    
    # Save recommendations to CSV
    df_recommendations_with_info.to_csv(csv_file_path, index=False)
    
    return df_recommendations_with_info


# In[10]:


# List of all user IDs
all_user_ids = ["sine_1", "asha_1", "michelle_1", "zang_1", "zane_1"]

# Generate combinations of user IDs with different lengths
user_id_combinations = []
for r in range(2, len(all_user_ids) + 1):
    user_id_combinations.extend(itertools.combinations(all_user_ids, r))

# Iterate over each combination and generate recommendations
for user_ids_combination in user_id_combinations:
    recommendations = get_jaccard_recommendations(list(user_ids_combination), df, movies)

