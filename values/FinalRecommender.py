"""
This file combines the values to make recommendations based on all of them.
"""
class FinalRecommender:
    def __init__(self, age, positivty, collaboration):
        self.age = age
        self.positivity = positivty
        self.collaboration = collaboration
    
    def generate_recommendations():
        pass

    def fairness(self, recommendations):
        # input code to see if the recommendations made are indeed representative
        # if not, regenerate the recommendations
        pass