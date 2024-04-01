import streamlit as st

def transparency_explanations():
    st.title("Transparency Explanations")

    with open('../data/explanations/design_objective.txt', 'r') as file:
        objectives = file.read()
    st.markdown(objectives)

    with st.expander("**Generations of Recommendations**"):
        with open('../data/explanations/generated_recommendations.txt', 'r') as file:
            generations = file.read()
        st.markdown(generations)

    with st.expander("**Displaying Recommendations**"):
        with open('../data/explanations/display_recommendations.txt', 'r') as file:
            display = file.read()
        st.markdown(display)

    with st.expander("**Data**"):
        with open('../data/explanations/data_sets.txt', 'r') as file:
            data = file.read()
        st.markdown(data)

    st.title("Methods and Values")

    with st.expander("**Child Appropriateness Scores**"):
        with open('../data/explanations/child_appropriateness.txt', 'r') as file:
            cas = file.read()
        st.markdown(cas)
        st.latex(r"s \times \text{sentiment} + t1 \times \text{freq1} + t2 \times \text{freq2} + r1 \times \text{rating} + r2 \times \text{rating\_desc\_score}")
        st.markdown("Where:")
        st.latex(r"s = \text{weight for the Sentiment Analysis score}")
        st.latex(r"t1 = \text{weight for the Term Frequency score for the synopses}")
        st.latex(r"t2 = \text{weight for the Term Frequency score for the age description}")
        st.latex(r"r1 = \text{weight for the Age Rating score}")
        st.latex(r"r2 = \text{weight for the Age Rating Description score}")

    with st.expander("**Community**"):
        with open('../data/explanations/community.txt', 'r') as file:
            community = file.read()
        st.markdown(community)

    with st.expander("**Positivity**"):
        with open('../data/explanations/positivity.txt', 'r') as file:
            positivity = file.read()
        st.markdown(positivity)

    with st.expander("**Fairness**"):
        with open('../data/explanations/fairness.txt', 'r') as file:
            fairness = file.read()
        st.markdown(fairness)
        st.latex(r"\text{Majority Representation} = \frac{\text{Number of majority represented mediated}}{\text{Number of total recommendations}}")
        st.latex(r"\text{Minority Representation} = \frac{\text{Number of minority represented mediated}}{\text{Number of total recommendations}}")
        st.latex(r"\text{Mixed Representation} = \frac{\text{Number of mixed represented mediated}}{\text{Number of total recommendations}}")
        st.markdown("Then an intermediate score can be calculated as follows by comparing the actual recommendation ratios to an ideal target distribution.")
        st.latex(r" \text{Intermediate Score =} \sum_{i} \left| \text{Actual Ratio}_i - \text{Target Ratio}_i \right|")

        st.latex(r"i: \text{ethnic representation category (Majority, Minority, Mixed)}")
        st.markdown("The final fairness score is calculated as follows:")
        st.latex(r"\text{Fairness Score} = 1- \text{Intermediate Score}")
        st.markdown("The score is in the range (0,1).")

    if st.button("Back to recommendations", key= "back_rec"+ str(st.session_state.key)):
            st.session_state.page = "recommendations"