import pandas as pd
import numpy as np
import streamlit as st
import recommendation_page as rp

class ChildAppropriatenessScore:
    def __init__(self, age, genre):
        self.age = age
        self.cas_id = '18'

        if genre == 'Any':
            self.make_recommendations(self.age_range())
        else:
            self.filter_data(self.age_range(), genre)

    def filter_data(self, df, genre):
        filtered_df =  df[df['category'] == genre]
        self.make_recommendations(filtered_df)
    
    def age_range(self):
        if self.age <= 8:
            df = pd.read_csv('../data/recommendations/ages4_8.csv')
            self.cas_id = '48' # this is used to select the correct column to display the CAS
        elif self.age <= 10:
            df = pd.read_csv('../data/recommendations/ages9_11.csv')
            self.cas_id = '911'
        elif self.age <=14:
            df = pd.read_csv('../data/recommendations/ages12_14.csv')
            self.cas_id = '1214'
        else:
            df = pd.read_csv('../data/recommendations/ages15_17.csv')
            self.cas_id = '1517'

        return df
        
    def make_recommendations(self, df):
        rp.recommendations(df, self.cas_id)