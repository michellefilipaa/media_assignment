import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

import streamlit as st
import pandas as pd
import recommendation_page as rp
from values.ChildAppropriatenessScore import ChildAppropriatenessScore

class app: 

    @staticmethod
    def home_page():
        st.markdown("<h1 style='text-align: center; color: black;'>Select your profile</h1>", unsafe_allow_html=True)

        user_profiles = {
            "Asha" : "images/asha.png",
            "Michelle" : "images/michelle.png",
            "Sine" : "images/sine.png",
            "Zane" : "images/zane.png",
            "Zang" : "images/zang.png"
        }

        profile_description = {
            "Asha" : "insert description of profile/user character",
            "Michelle" : "insert description of profile/user character",
            "Sine" : "insert description of profile/user character",
            "Zane" : "insert description of profile/user character",
            "Zang" : "insert description of profile/user character"
        }

        cols = st.columns(5)
        for idx, (profile, img_path) in enumerate(user_profiles.items()):
            with cols[idx]:
                st.image(img_path, use_column_width=True)
        
                if st.button(f"{profile}"):
                    st.session_state.page = profile.lower()

                st.markdown(profile_description[profile])

    @staticmethod
    def generate_profile(person, checkboxes):
        st.title(person)

        # choose a genre
        st.markdown("**Do you have a genre in mind?**")
        st.session_state.genre = st.radio("Genres:", ["Any","CBBC", "Comedy", "Documentary", "Entertainment", "Films", "History", "Science", "Signed", "Sports"])

        # Value = Positivity
        st.markdown("**Positivity Level:**")
        st.markdown("What mood are you in? How positive would you like the recommendations content to be?")
        positivity = st.slider('', min_value=0, max_value=10, value=5)

        # Value = Collaboration
        st.markdown("**Who are you watching with?**")

        # this is for the transparency value
        st.markdown("This is used to make recommendations based on all your interests!") #TODO
        for checkbox in checkboxes:
            st.checkbox(checkbox)
        children = st.checkbox('Children')

        # Value = (Restricted) Access
        if children: 
            st.markdown("**Age of Children**")
            st.markdown("insert transparency explanation") # TODO
            age = st.slider('Select age of child', min_value=4, max_value=17, value=5)
            st.session_state.age = age
        
        if st.button("Next"):
            if children:
                st.session_state.page = "child_recommendations"
            else:
                st.session_state.page = "recommendations"

    @staticmethod
    def asha():
        checkboxes = ['No one','Michelle', 'Sine', 'Zane', 'Zang']
        app.generate_profile("Asha's Profile", checkboxes)

    @staticmethod
    def michelle():
        checkboxes = ['No one','Asha', 'Sine', 'Zane', 'Zang']
        app.generate_profile("Michelle's Profile", checkboxes)

    @staticmethod
    def sine():
        checkboxes = ['No one','Asha', 'Michelle', 'Zane', 'Zang']
        app.generate_profile("Sine's Profile", checkboxes)
    
    @staticmethod
    def zane():
        checkboxes = ['No one','Asha', 'Michelle', 'Sine', 'Zang']
        app.generate_profile("Zane's Profile", checkboxes)

    @staticmethod
    def zang():
        checkboxes = ['No one','Asha','Michelle', 'Sine', 'Zane']
        app.generate_profile("Zang's Profile", checkboxes)

    @staticmethod
    def recommendations():
        st.title("Top 10 recommendations")
        df = pd.read_csv('../recommendations/ages12_14.csv')
        rp.recommendations(df, '18')

streamlit_app = app()

# Check if session_state.page exists and set it to default value if not
if "page" not in st.session_state:
    st.session_state.page = "first_page"

# Display content based on the session_state.page value
if st.session_state.page == "first_page":
    app.home_page()
elif st.session_state.page == "asha":
    app.asha()
elif st.session_state.page == "michelle":
    app.michelle()
elif st.session_state.page == "sine":
    app.sine()
elif st.session_state.page == "zane":
    app.zane()
elif st.session_state.page == "zang":
    app.zang()
elif st.session_state.page == "recommendations":
    st.session_state.key = 0
    app.recommendations()
elif st.session_state.page == "child_recommendations":
    st.session_state.key = 0
    age = st.session_state.age
    genre = st.session_state.genre
    cas = ChildAppropriatenessScore(age, genre, False, None)