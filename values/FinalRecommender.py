"""
This file combines the values to make recommendations based on all of them.
"""
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
import values.ChildAppropriatenessScore as cas
import pandas as pd
import recommendation_page as rp

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

        polarity_df = self.filter_polarity(df)
        self.display_recommendations(polarity_df, cas_id)

    def collaboration(self):
        pass

    def access(self):
        return self.cas_instance.make_recommendations(self.genre)

    def fairness(self, recommendations):
        # input code to see if the recommendations made are indeed representative
        # if not, regenerate the recommendations
        pass

    def filter_polarity(self, df):
        return df[df['vader_sentiment'] == self.polarity]

    def display_recommendations(self, df, cas_id):
        rp.recommendations(df, cas_id)
