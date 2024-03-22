import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
import base64
import pandas as pd
import streamlit as st
import values.FinalRecommender as r

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
            "Michelle" : "This is a child profile. Only child appropriate content is recommended here.",
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
        if "genre" not in st.session_state:
            st.session_state.genre = "Any"
        st.markdown("**Do you have a genre in mind?**")
        st.session_state.genre = st.radio("Genres:", ["Any","CBBC", "Comedy", "Documentary", "Entertainment", "Films", "History", "Science", "Signed", "Sports"])

        # Value = Positivity
        if "polarity" not in st.session_state:
            st.session_state.genre = "Neutral"
        st.markdown("**Positivity Level:**")
        st.markdown("What mood are you in? How positive would you like the recommendations content to be?")
        st.session_state.polarity = st.radio("Polarity:", ["Very Negative","Negative", "Neutral", "Positive", "Very Positive"])

        # Value = Collaboration
        st.markdown("**Who are you watching with?**")
        st.markdown("Leave empty if you're watching alone.")

        # Value = Transparency
        st.markdown("This is used to make recommendations based on all your interests!") #TODO
        checkbox_states = []
        for checkbox in checkboxes:
            checkbox_states.append(st.checkbox(checkbox))
        children = st.checkbox('Children')

        st.session_state.checked_checkboxes = [checkboxes[i] for i, state in enumerate(checkbox_states) if state]
        # Value = (Restricted) Access
        if children: 
            st.markdown("**Age of Children**")
            st.markdown("insert transparency explanation") # TODO
            st.session_state.age = st.slider('Select age of child', min_value=4, max_value=17, value=5)
        
        if st.button("Next"):
            if children:
                st.session_state.page = "child_recommendations"
            else:
                st.session_state.page = "recommendations"

    @staticmethod
    def generate_child_profile(person, checkboxes):
        st.title(person)

        # Value = (Restricted) Access
        st.markdown("**How old are you?**")
        st.markdown("insert transparency explanation") # TODO
        st.session_state.age = st.slider('Select age:', min_value=4, max_value=17, value=5)

        images = {
            "CBBC" : "images/kid_profile/cbbc.png",
            "Comedy" : "images/kid_profile/comedy.png",
            "Documentaries" : "images/kid_profile/documentaries.png",
            "Entertainment" : "images/kid_profile/entertainment.png",
            "Films" : "images/kid_profile/films.png",
            "From the Archives" : "images/kid_profile/archives.png",
            "Science & Nature" : "images/kid_profile/nature.png",
            "Sports" : "images/kid_profile/sports.png",
            "Any" : "images/kid_profile/any.png"
        }
        
        # choose a genre
        if "genre" not in st.session_state:
            st.session_state.genre = "Any"
        st.markdown("**Do you have a genre in mind?**")
        cols = st.columns(3)

        for idx, (genre, img_path) in enumerate(images.items()):
            row = idx // 3  # Calculate row index
            col = idx % 3   # Calculate column index
            if st.session_state.age < 9 and genre in ["From the Archives", "Comedy"]:
                continue  # Skip these genres if age < 9
            elif st.session_state.age < 12 and genre == "Comedy":
                continue  # Skip "comedy" genre if age < 12
            with cols[col]:
                st.image(img_path, use_column_width=True)
                if st.button(f"{genre}"):
                    st.session_state.genre = genre
        
        st.markdown("**Selected Genre:** " + st.session_state.genre)

        # Value = Positivity
        if "polarity" not in st.session_state:
            st.session_state.genre = "Neutral"
        st.markdown("**Positivity Level:**")
        st.markdown("What mood are you in? How positive would you like the recommendations content to be?")
        st.session_state.polarity = st.radio("Polarity:", ["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"])

        # Value = Collaboration
        st.markdown("**Who are you watching with?**")
        st.markdown("Leave empty if you're watching alone.")

        # Value = Transparency
        st.markdown("This is used to make recommendations based on all your interests!") #TODO
        checkbox_states = []
        for checkbox in checkboxes:
            checkbox_states.append(st.checkbox(checkbox))
        children = st.checkbox('Children')

        st.session_state.checked_checkboxes = [checkboxes[i] for i, state in enumerate(checkbox_states) if state]           
        
        if st.button("Next"):
            st.session_state.page = "child_recommendations"

    @staticmethod
    def asha():
        checkboxes = ['Michelle', 'Sine', 'Zane', 'Zang']
        app.generate_profile("Asha's Profile", checkboxes)

    @staticmethod
    def michelle():
        checkboxes = ['Asha', 'Sine', 'Zane', 'Zang']
        app.generate_child_profile("Michelle's Profile", checkboxes)

    @staticmethod
    def sine():
        checkboxes = ['Asha', 'Michelle', 'Zane', 'Zang']
        app.generate_profile("Sine's Profile", checkboxes)
    
    @staticmethod
    def zane():
        checkboxes = ['Asha', 'Michelle', 'Sine', 'Zang']
        app.generate_profile("Zane's Profile", checkboxes)

    @staticmethod
    def zang():
        checkboxes = ['Asha','Michelle', 'Sine', 'Zane']
        app.generate_profile("Zang's Profile", checkboxes)

streamlit_app = app()
st.session_state.key = 0
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
    age = st.session_state.age if "age" in st.session_state else 18
    genre = st.session_state.genre
    polarity = st.session_state.polarity
    collaboration = st.session_state.checked_checkboxes
    recommender = r.FinalRecommender(genre, polarity, collaboration, age)
elif st.session_state.page == "child_recommendations":
    age = st.session_state.age
    genre = st.session_state.genre
    polarity = st.session_state.polarity
    collaboration = st.session_state.checked_checkboxes
    recommender = r.FinalRecommender(genre, polarity, collaboration, age)