import streamlit as st
import pandas as pd
import st_template as t
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
    def asha():
        st.title("Asha's Profile")

        st.markdown("**Positivity Level:**")
        st.markdown("What mood are you in? How positive would you like the recommendations content to be?")

        # this is for the transparency value
        st.markdown("This is used to ...*finish explanation*...") #TODO

        positivity = st.slider('', min_value=0, max_value=10, value=5)

        st.markdown("**Who are you watching with?**")

        # this is for the transparency value
        st.markdown("This is used to make recommendations based on all your interests!") #TODO

        no_one = st.checkbox('No one')
        michelle = st.checkbox('Michelle')
        sine = st.checkbox('Sine')
        zane = st.checkbox('Zane')
        zang = st.checkbox('Zang')
        children = st.checkbox('Children')

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
    def michelle():
        st.title("Michelle's Profile")
        pass

    @staticmethod
    def sine():
        st.title("Sine's Profile")
        pass

    @staticmethod
    def zane():
        st.title("Zane's Profile")
        pass

    @staticmethod
    def zang():
        st.title("Zang's Profile")
        pass

    @staticmethod
    def recommendations():
        st.title("Top 10 recommendations")
        df = pd.read_csv('../recommendations/ages12_14.csv')

        t.recommendations(df)

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
    app.recommendations()
elif st.session_state.page == "child_recommendations":
    age = st.session_state.age
    cas = ChildAppropriatenessScore(age)
    cas.child_recommendations()