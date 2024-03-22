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
            "Asha" : "Asha is an avid sports fan.",
            "Michelle" : "Michelle is a child. She only gets to watch certain content.",
            "Sine" : "Sine enjoys wildlife documentaries and good old fashioned movies.",
            "Zane" : "Zane enjoys documentaries and sports.",
            "Zang" : "Zang loves a good comedy and wildlife documentaries."
        }

        cols = st.columns(5)
        for idx, (profile, img_path) in enumerate(user_profiles.items()):
            with cols[idx]:
                st.image(img_path, use_column_width=True)
        
                if st.button(f"{profile}"):
                    st.session_state.person = profile
                    st.session_state.page = "user_home"

                st.markdown(profile_description[profile])

    @staticmethod
    def user_home(person):
        st.title(person + "'s Profile")
        if st.button("New Search"):
            st.session_state.page = "search"

        path = '../data/ratings/' + person.lower() + '_ratings.csv'
        user_ratings_csv = pd.read_csv(path)
        most_recent = user_ratings_csv.sort_values(by='rating')
        favorites = user_ratings_csv.sort_values(by='date_watched')

        st.markdown("**Most recently watched:**")
        cols = st.columns(2)
        for i, row in most_recent.head(2).iterrows():
            movie_id = row['showId'] 
            movie_data = st.session_state.all_data.loc[st.session_state.all_data.index == movie_id]
            if not movie_data.empty:
                cols[i % 2].image(movie_data['image'].values[0], caption=movie_data['title'].values[0], width=250)
                
        st.markdown("**Highest rated:**")
        cols2 = st.columns(2)
        for i, row in user_ratings_csv.head(2).iterrows():
            movie_id = row['showId'] 
            movie_data = st.session_state.all_data.loc[st.session_state.all_data.index == movie_id]
            if not movie_data.empty:
                cols2[i % 2].image(movie_data['image'].values[0], caption=movie_data['title'].values[0], width=250)
        
        if st.button("Back"):
            st.session_state.page = "first_page"

    @staticmethod
    def search_profile(checkboxes):
        # choose a genre
        if "genre" not in st.session_state:
            st.session_state.genre = "Any"
        st.markdown("**Do you have a genre in mind?**")
        st.session_state.genre = st.radio("Genres:", ["Any","CBBC", "Comedy", "Documentary", "Entertainment", "Films", "History", "Science", "Signed", "Sports"])

        # Value = Positivity
        if "polarity" not in st.session_state:
            st.session_state.polarity = "Neutral"
        st.markdown("**Positivity Level:**")
        st.markdown("What mood are you in? How positive would you like the recommendations content to be?")
        st.session_state.polarity = st.radio("Polarity:", ["Very Negative","Negative", "Neutral", "Positive", "Very Positive"])

        # Value = Collaboration
        st.markdown("**Who are you watching with?**")
        st.markdown("Leave empty if you're watching alone.")

        # Value = Transparency
        st.markdown("This is used to make recommendations based on all your interests!") 
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
    def search_child_profile(checkboxes):
        # Value = (Restricted) Access
        st.markdown("**How old are you?**")
        # Value = Transparency
        st.markdown("This is used to make sure we recommend the right content.") # TODO
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
            st.session_state.polarity = "Neutral"
        st.markdown("**Positivity Level:**")
        st.markdown("What mood are you in? How positive would you like the recommendations content to be?")
        st.session_state.polarity = st.radio("Polarity:", ["Neutral", "Positive", "Very Positive"])

        # Value = Collaboration
        st.markdown("**Who are you watching with?**")
        st.markdown("Leave empty if you're watching alone.")

        # Value = Transparency
        st.markdown("This is used to make recommendations based on all your interests!") #TODO
        checkbox_states = []
        for checkbox in checkboxes:
            checkbox_states.append(st.checkbox(checkbox))

        st.session_state.checked_checkboxes = [checkboxes[i] for i, state in enumerate(checkbox_states) if state]           
        
        if st.button("Next"):
            st.session_state.page = "child_recommendations"

    @staticmethod
    def asha():
        app.user_home('Asha')

    @staticmethod
    def michelle():
        app.user_home('Michelle')

    @staticmethod
    def sine():
        app.user_home('Sine')
    
    @staticmethod
    def zane():
        app.user_home('Zane')

    @staticmethod
    def zang():
        app.user_home('Zang')
    
    @staticmethod
    def handle_search():
        st.title(st.session_state.person + "'s Search Profile")

        person = st.session_state.person
        if person is None:
            st.error("No user selected.")
            return

        checkboxes = ['Asha', 'Michelle', 'Sine', 'Zane', 'Zang']
        if person == 'Asha':
            checkboxes.remove('Asha')
            app.search_profile(checkboxes)
        elif person == 'Michelle':
            checkboxes.remove('Michelle')
            app.search_child_profile(checkboxes)
        elif person == 'Sine':
            checkboxes.remove('Sine')
            app.search_profile(checkboxes)
        elif person == 'Zane':
            checkboxes.remove('Zane')
            app.search_profile(checkboxes)
        elif person == 'Zang':
            checkboxes.remove('Zang')
            app.search_profile(checkboxes)

streamlit_app = app()
st.session_state.key = 0
st.session_state.all_data = pd.read_csv('../data/all_data.csv')

if "page" not in st.session_state:
    st.session_state.page = "first_page"

if st.session_state.page == "first_page":
    app.home_page()
elif st.session_state.page in "user_home":
    app.user_home(st.session_state.person)
elif st.session_state.page == "search":
    app.handle_search()
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