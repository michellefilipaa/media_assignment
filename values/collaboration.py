#!/usr/bin/env python
# coding: utf-8

# # Collaboration

# In[373]:


import numpy as np
import itertools
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


# In[374]:


user_ratings = pd.read_csv('../data/user_ratings.csv')
movies = pd.read_csv('../data/all_data.csv')


# In[375]:


df = pd.merge(user_ratings, movies, on='showId', how='left')
genres = df['category'].str.get_dummies('|')
df = pd.concat([df, genres], axis=1)
df = df[['userId', 'showId', 'rating', 'CBBC', 'Comedy', 'Documentaries', 'Entertainment', 'From the Archives', 'Science & Nature', 'Sports']]


# In[376]:


df


# # Collaborative filtering (Jaccard similarity)
# In the function below the jaccard similarity is written based on the ratings of the users

# In[377]:


import pandas as pd
import os

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
    
    # Use the defined directory path to save recommendations to CSV
    csv_file_path = os.path.join(directory, "collaboration_" + "_".join(user_ids) + ".csv")
    
    # Save recommendations to CSV
    df_recommendations_with_info.to_csv(csv_file_path, index=False)
    
    return df_recommendations_with_info



# In[378]:


user_ids = ["michelle_1", "asha_1"]  # List of user IDs in the group
recommendations = get_jaccard_recommendations(user_ids, df, movies)
recommendations


# In[379]:


user_ids = ["sine_1", "zang_1", "zane_1"]  # List of user IDs in the group
recommendations = get_jaccard_recommendations(user_ids, df, movies)
recommendations


# In[380]:


user_ids = ["sine_1", "asha_1"]  # List of user IDs in the group
recommendations = get_jaccard_recommendations(user_ids, df, movies)
recommendations


# In[ ]:





# In[ ]:





# In[ ]:




