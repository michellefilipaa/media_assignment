import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
import pandas as pd
import numpy as np
import streamlit as st
import recommendation_page as rp

class ChildAppropriatenessScore:
    def __init__(self, age, genre, regenerate, again_df):
        self.age_ranges = {
            (4, 8): '48',
            (9, 11): '911',
            (12, 14): '1214',
            (15, 17): '1517'
        }

        self.cas_to_csv_mapping = {
            '48': '../data/recommendations/ages4_8.csv',
            '911': '../data/recommendations/ages9_11.csv',
            '1214': '../data/recommendations/ages12_14.csv',
            '1517': '../data/recommendations/ages15_17.csv'
        }
        
        self.cas_id = self.get_cas_id(age)


        df = self.get_dataframe_for_cas()
        if genre == 'Any':
            self.make_recommendations(df)
        else:
            self.filter_data(df, genre)

    def get_dataframe_for_cas(self):
        csv_path = self.cas_to_csv_mapping.get(self.cas_id)
        if csv_path:
            return pd.read_csv(csv_path)
        else:
            return None 
    
    def get_cas_id(self, age):
        for (start, end), cas_id in self.age_ranges.items():
            if start <= age <= end:
                return cas_id
        return '18'
        
    def filter_data(self, df, genre):
        filtered_df =  df[df['category'] == genre]
        self.make_recommendations(filtered_df)
    
    def make_recommendations(self, df):
        rp.recommendations(df, self.cas_id)