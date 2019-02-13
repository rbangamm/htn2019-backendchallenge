# Helper functions
import backend

def format_user(user_skills, user):
    user_skills = [{"name":skill['name'], "rating":skill["rating"]} for skill in user_skills]
    user['skills'] = user_skills
