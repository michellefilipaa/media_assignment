import streamlit as st

def recommendations(df, cas_id):
    st.title("Recommendations")
    cas_string = 'cas' + cas_id
    for i, row in df.iterrows():
        st.write("---") 

        cover, title = st.columns(2)  
        info, description = st.columns(2) 

        # Display movie cover
        with cover:
            st.image(row['image'], caption="Cover", use_column_width=True)

        # Display movie title
        with title:
            st.title(row['title'])

        # Display movie information
        with info:
            st.markdown(f"**Category:** {row['category']}")
            st.markdown(f"**Tags:** {row['tags']}")
            st.markdown(f"**Age Rating:** {row['age_rating']}")
            st.markdown(f"**Child Appropriateness Score:** {round(row[cas_string], 3)}")
            st.markdown(f"**Sentiment Score:** {col['vader_polarity']}")

        # Display movie description
        with description:
            st.markdown("**Synopsis:**")
            st.markdown(row['synopsis_small'])
