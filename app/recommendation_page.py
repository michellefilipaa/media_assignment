import streamlit as st

if 'generate_new' not in st.session_state:
    st.session_state.generate_new = False

def generate_new_recommendations(df, cas_id):
        new_df = df.sample(n=10)
        st.session_state.key += 1
        recommendations(new_df, cas_id) 

def recommendations(df, cas_id, best):
    cas_string = 'cas' + cas_id
    
    st.markdown("Click on the button below if you would like to know more about how recommendations are made.")
    if st.button("Transparency Info.", key= "transparency"+ str(st.session_state.key)):
            st.session_state.page = "transparency_page"
            st.session_state.generate_new = False 

    if len(df) == 0:
        st.title("No results found")
        st.markdown("Unfortunately there is no appropriate content available for your search criteria.")
        st.markdown("Please try another search.")

        if st.button("Back to home", key='back2_' + str(st.session_state.key)):
            st.session_state.page = "first_page"
            st.session_state.generate_new = False  
    
    else:
        st.title("Top Recommendations")
        if not best:
            st.markdown("We were unable to provide a set of recommendations with a diverse representation due to sample size.")

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
                st.markdown(f"**Sentiment Score:** {col['vader_sentiment']}")
                if cas_string != 'cas18':
                    st.markdown(f"**Child Appropriateness Score:** {round(col[cas_string], 3)}")
            with description:
                st.markdown("**Synopsis**")
                st.markdown(col['description'])
        
        st.markdown("---")

        if st.button("Back to home", key= "back"+ str(st.session_state.key)):
            st.session_state.page = "first_page"
            st.session_state.generate_new = False  
    
        # This is done because sometimes (on the child's profile), there are less than 10 movies in a genre.
        # In this scenario, more recommendations would not be able to be made.
        if len(df) > 10:
            st.markdown("**Are you happy with the recommendations?**")
        
            st.markdown("If not,")

            if st.button("Generate new recommendations", key="gen"+ str(st.session_state.key)):
                if cas_string != 'cas18':
                    age = st.session_state.age
                    genre = st.session_state.genre
                    st.session_state.generate_new = True
                    generate_new_recommendations(df, cas_id)


