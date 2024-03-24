"""
This file combines the values to make recommendations based on all of them.
"""
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
import values.ChildAppropriatenessScore as cas
import pandas as pd
import string
import recommendation_page as rp
import streamlit as st
import numpy as np

class FinalRecommender:
    """
    age: the age selected
    polarity: the desired polarity
    collaboration: who the collaboration is with
    """
    def __init__(self, genre, polarity, collaboration, age):
        self.genre = genre
        self.age = age
        self.polarity = polarity
        self.collaboration = collaboration
        cas_id = '18'

        if age<18:
            self.cas_instance = cas.ChildAppropriatenessScore(age, genre, False, None)
            df, cas_id = self.access()
        else:
            df = pd.read_csv('../data/all_data.csv')

        if not self.collaboration:
            collab_df = None
        else:
            collab_df = self.collab()
        
        polarity_df = self.filter_polarity_and_genre(df)
        final_df = self.combine(df, polarity_df, collab_df)
        final_df, best = self.fairness(final_df)
        self.display_recommendations(final_df, cas_id, best)

    def collab(self):
        file_name = "../data/recommendations/collaboration_" + (st.session_state.person).lower()
        if self.collaboration: 
            file_name += "".join(item.lower() for item in self.collaboration)
            file_name += ".csv"
            if os.path.exists(file_name):
                return pd.read_csv(file_name)
            else:
                return pd.DataFrame(columns=['title'])
        

    def access(self):
        return self.cas_instance.make_recommendations(self.genre)

    def fairness(self, recommendations):
        top10 = recommendations.head(10)  # Select the first 10 entries
        total_recommendations = len(top10)

        nonMinority_ratio = top10['representation'].eq(1).sum() / total_recommendations
        minority_ratio = top10['representation'].eq(2).sum() / total_recommendations
        # NA items are mixed sport teams and other mixed stuff (cartoons)
        mixed_ratio = (top10['representation'].eq(3).sum() + top10['representation'].isna().sum()) / total_recommendations

        #print(nonMinority_ratio, minority_ratio, mixed_ratio)

        # target distribution for each category (majority are mixed that way 2/4 and others 1/4)
        target_distribution = np.array([1/4, 1/4, 2/4])

        # Intermediate fairness scores
        intermediate_scores = np.abs(np.array([nonMinority_ratio, minority_ratio, mixed_ratio]) - target_distribution)
        print(intermediate_scores)

        found_better = True
        # Fairness score of the current top 10 recommendation
        overall_fairness_score = 1 - np.max(intermediate_scores)
        print(overall_fairness_score)

    
        # Check if fairness score is less than 0.5, if not make a better/more fair recommendation
        if overall_fairness_score < 0.5:
            found_better = False
            
            # Find 'group' that is most represented
            highest_representation = 0

            if nonMinority_ratio > minority_ratio and nonMinority_ratio > mixed_ratio:
                highest_representation = 0
            elif minority_ratio > nonMinority_ratio and minority_ratio > mixed_ratio:
                highest_representation = 1
            else:
                highest_representation = 2


            # Find the index of a row with a movie with overrepresented group, this will be replaced
            index_to_replace = top10[top10['representation'] == highest_representation].index[0]

            # Look for other recommendations that improve the score
            for i in range(total_recommendations, len(recommendations)):
                next_entry = recommendations.iloc[i]

                # Add the next entry to df and recalculate fairness score
                new_df = pd.concat([top10.drop(index_to_replace), next_entry.to_frame().T], ignore_index=True)
                total_recommendations = len(new_df)

                nonMinority_ratio = new_df['representation'].eq(1).sum() / total_recommendations
                minority_ratio = new_df['representation'].eq(2).sum() / total_recommendations
                mixed_ratio = (new_df['representation'].eq(3).sum() + new_df['representation'].isna().sum()) / total_recommendations

                new_intermediate_scores = np.abs(np.array([nonMinority_ratio, minority_ratio, mixed_ratio]) - target_distribution)
                new_overall_fairness_score = 1 - np.max(new_intermediate_scores)

                # If the score is greater than or equal to 0.5, update df and return the "fairer" recommendation
                if new_overall_fairness_score >= 0.5:
                    overall_fairness_score = new_overall_fairness_score
                    top10 = new_df
                    found_better = True
                    break

                # If no better recommendation is found, return the "unfair" recommendation

        print("Final overall fairness score:", overall_fairness_score)
        return top10, found_better
    
    def filter_polarity_and_genre(self, df):
        if self.genre != 'Any':
            filtered_df = df[(df['vader_sentiment'] == self.polarity) & (df['category'] == self.genre)]
        else:
            filtered_df = df[df['vader_sentiment'] == self.polarity]
        
        return filtered_df

    def combine(self, df, polarity_df, collab_df=None):
        df1 = pd.merge(df, polarity_df, how='inner')
        if collab_df is not None:
            df1 = pd.merge(df1, collab_df, how='inner')
        
        return df1
    
    def display_recommendations(self, df, cas_id, best):
        rp.recommendations(df, cas_id, best)
