import backend

FIELDS = []

def format_user(user_skills, user):
    user_skills = [{"name":skill['name'], "rating":skill["rating"]} for skill in user_skills]
    user['skills'] = user_skills


def remove_fields(data):
    for key, value in data.iteritems():
        if not key in FIELDS:
            del data[key]

def sanitize_inputs(data):
    for key, value in data.iteritems():
        if key == "email":
            pass
