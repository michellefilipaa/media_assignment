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
        self.display_recommendations(final_df, cas_id)

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
        # input code to see if the recommendations made are indeed representative
        # if not, regenerate the recommendations
        pass
    
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
    
    def display_recommendations(self, df, cas_id):
        rp.recommendations(df, cas_id, self.collaboration)
