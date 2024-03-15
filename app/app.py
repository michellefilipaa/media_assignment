import streamlit as st

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

        cols = st.columns(5)
        for idx, (profile, img_path) in enumerate(user_profiles.items()):
            with cols[idx]:
                st.image(img_path, use_column_width=True)
        
                if st.button(f"{profile}"):
                    st.session_state.page = profile.lower()

    @staticmethod
    def asha():
        st.title("Asha's Profile")
        pass

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
