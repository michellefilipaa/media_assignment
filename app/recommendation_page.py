import streamlit as st

def recommendations(df, cas_id):
    
    cas_string = 'cas' + cas_id

    if len(df) == 0:
        st.title("No results found")
        st.markdown("Unforunately there is no appropriate content available for your search criteria.")
        st.markdown("Please try another search.")

        if st.button("Back to home"):
            st.session_state.page = "first_page"
    
    else:
        st.title("Top Recommendations")

        for i, col in df.head(10).iterrows():
            st.write('---')

            cover, title = st.columns(2)
            info, description = st.columns(2)

            with cover:
                st.image(col['image'], caption="Cover", use_column_width=True)

            with title:
                st.title(col['title'])
            
            with info:
                st.markdown(f"**Category:** {col['category']}")
                st.markdown(f"**Tags:** {col['tags']}")
                st.markdown(f"**Age Rating:** {col['age_rating']}")
                if cas_string != 'cas18':
                    st.markdown(f"**Child Appropriateness Score:** {round(col[cas_string], 3)}")

            with description:
                st.markdown("**Synopsis**")
                st.markdown(col['description'])
            
            if st.button("Back to home"):
                st.session_state.page = "first_page"