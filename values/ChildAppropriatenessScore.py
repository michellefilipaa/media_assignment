import pandas as pd
import numpy as np
import streamlit as st
import st_template as t

class ChildAppropriatenessScore:
    def __init__(self, age):
        # self.st = session
        # read the data
        # TODO: make a dataset with content suitable for children only
        self.df = pd.read_csv('../data/recommendation_csv/ages4_8.csv') 
        self.age = age

    def child_recommendations(self):
        st.title("Top 10 recommendations")
        
        if self.age <= 8:
            df = pd.read_csv('../data/recommendation_csv/ages4_8.csv')
        elif self.age <= 10:
            df = pd.read_csv('../data/recommendation_csv/ages9_11.csv')
        elif self.age <=14:
            df = pd.read_csv('../data/recommendation_csv/ages12_14.csv')
        else:
            df = pd.read_csv('../data/recommendation_csv/ages15_17.csv')

        t.recommendations(df)