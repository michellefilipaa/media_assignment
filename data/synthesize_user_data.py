#!/usr/bin/env python
# coding: utf-8

# In[99]:


from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import random


# In[108]:


import pandas as pd

# Read the CSV file
df_shows = pd.read_csv('../data/all_data.csv')


# In[109]:


genres = df_shows['category'].unique()


# In[110]:


genres


# In[111]:


def generate_user_ratings_with_profile(df_shows, personas, min_history=5, max_history=15):
    user_data = []

    for persona, preferences in personas.items():
        # Generating user IDs for each persona
        user_ids = [f"{persona}_{i+1}" for i in range(preferences['n_users'])]

        for user_id in user_ids:
            # Shuffle the preferred genres for each persona
            shuffled_genres = preferences['preferred_genres']
            random.shuffle(shuffled_genres)
            
            # If the persona is children_viewer, exclude 'CBBC' genre from additional genres
            if persona == 'children_viewer':
                additional_genres = list(set(df_shows['category'].unique()) - set(shuffled_genres) - {'CBBC'})
            else:
                additional_genres = list(set(df_shows['category'].unique()) - set(shuffled_genres))
            random.shuffle(additional_genres)
            selected_additional_genres = additional_genres[:random.randint(1, 2)]
            genres_to_watch = shuffled_genres + selected_additional_genres

            # Determine the number of shows the user has seen within the specified range
            num_shows = random.randint(min_history, max_history)

            # Select shows to add to user's viewing history
            shows_watched = df_shows[df_shows['category'].isin(genres_to_watch)].sample(n=num_shows, replace=True)

            for _, row in shows_watched.iterrows():
                # Assigning rating based on user's preferences
                rating = np.nan if random.random() > preferences['rating_probability'] else random.randint(1, 5)
                if not np.isnan(rating):
                    # Generating a random date within the past year
                    date_watched = datetime.now() - timedelta(days=random.randint(0, 365))
                    user_data.append({
                        "userId": user_id,
                        "showId": row["showId"],  
                        "rating": rating,
                        "date_watched": date_watched
                    })

    user_ratings_df = pd.DataFrame(user_data)

    # Save data for specific users to separate CSV files
    specific_users = ["zang", "michelle", "asha", "sine", "zane"]
    for userId in specific_users:
        user_df = user_ratings_df[user_ratings_df['userId'].str.startswith(userId)]
        user_df.to_csv(f"{userId}_ratings.csv", index=False)

    return user_ratings_df


# In[112]:


personas = {
    "sports_fan": {
        "preferred_genres": ["Sports"],
        "rating_probability": 0.8,
        "n_users": 100
    },
    "documentary_enthusiast": {
        "preferred_genres": ["Documentaries", "From the Archives", "Science & Nature"],
        "rating_probability": 0.7,
        "n_users": 130
    },
    "comedy_lover": {
        "preferred_genres": ["Comedy"],
        "rating_probability": 0.7,
        "n_users": 120
    },
    "entertainment_buff": {
        "preferred_genres": ["Entertainment"],
        "rating_probability": 0.7,
        "n_users": 120
    },
    
    "films_freak": {
        "preferred_genres": ["Entertainment"],
        "rating_probability": 0.7,
        "n_users": 90
    },
    "signed_fav": {
        "preferred_genres": ["Entertainment"],
        "rating_probability": 0.7,
        "n_users": 70
    },
    "children_viewer": {
        "preferred_genres": ["CBBC"],
        "rating_probability": 0.8,
        "n_users": 80
    }
}

# Our users
personas.update({
    "zang": {
        "preferred_genres": ["Entertainment", "Comedy", "From the Archives"],
        "rating_probability": 0.6,
        "n_users": 1
    },
    "michelle": {
        "preferred_genres": ["CBBC"],
        "rating_probability": 0.7,
        "n_users": 1
    },
    "asha": {
        "preferred_genres": ["Documentaries", "Entertainment", "CBBC", "Films"],
        "rating_probability": 0.7,
        "n_users": 1
    },
    "sine": {
        "preferred_genres": ["Comedy", "Sports", "Films"],
        "rating_probability": 0.8,
        "n_users": 1
    },
    "zane": {
        "preferred_genres": ["Sports", "Science & Nature", "Comedy", "Signed"],
        "rating_probability": 0.6,
        "n_users": 1
    }
})


# Generate user ratings with updated personas
user_ratings = generate_user_ratings_with_profile(df_shows, personas)
user_ratings.head()


# In[113]:


user_ratings[user_ratings["userId"]=="sports_fan_2"]


# In[114]:


user_ratings[user_ratings["userId"]=="michelle_1"]


# In[115]:


file_path = "user_ratings.csv"

# Save the DataFrame to a CSV file
user_ratings.to_csv(file_path, index=False)


# In[ ]:




