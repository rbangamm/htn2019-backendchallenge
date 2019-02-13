import backend
import backend.helpers
import re
from flask import Blueprint, jsonify, request, abort

users = Blueprint('users', __name__)

@users.route('/', methods=['GET'])
def get_users():
    users = backend.query_db('select * from users')
    for ind, user in enumerate(users):
        user_skills = backend.query_db('select * from skills where user_id = ?', [user['id']])
        user_skills = [{"name":skill['name'], "rating":skill["rating"]} for skill in user_skills]
        users[ind]['skills'] = user_skills
    return jsonify(users)

@users.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
   user = backend.query_db(
           'select * from users where id = ?', [user_id], one=True)
   user_skills = backend.query_db('select * from skills where user_id = ?', [user_id])
   backend.helpers.format_user(user_skills, user)
   return jsonify(user)

@users.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    c = backend.get_db().cursor()
    data = request.json
    schema = backend.get_schema('users')
    for key, value in data.items():
        if key != 'skills':
            # Don't do anything if the key isn't valid
            if key not in schema:
                continue
            c.execute('UPDATE users SET ' + key + ' = ? WHERE id = ?', [value, user_id])
        else:
            for skill in data[key]:
                skill_ratings = backend.query_db(
                    'SELECT * FROM skills WHERE user_id=? AND name=?', 
                    [user_id, skill['name']])
                if len(skill_ratings) == 0:
                    # If the skill doesn't exist, insert into the skills table
                    c.execute(
                        '''INSERT INTO skills (name, rating, user_id) 
                        VALUES (?, ?, ?)''', 
                        [skill['name'], skill['rating'], user_id])
                else:
                    # Otherwise, update the rating for the appropriate skill
                    c.execute('UPDATE skills SET rating=? WHERE user_id=? AND name=?',
                            [skill['rating'], user_id, skill['name']])
    backend.get_db().commit()
    user = backend.query_db('SELECT * FROM users WHERE id = ?', [user_id], one=True)
    user_skills = backend.query_db('select * from skills where user_id = ?', [user_id])
    backend.helpers.format_user(user_skills, user)
    return jsonify(user)

@users.route('/', methods=['POST'])
def create_user():
    c = backend.get_db().cursor()
    data = request.json
    schema = backend.get_schema('users')
    
    # Since skills is not in table schema
    schema.append('skills')

    schema.remove('id')

    keys = set(data.keys())
    schema_set = set(schema)

    # If the data is missing keys, abort
    if schema_set.difference(keys) != set():
        abort(400)

    ### Data sanity checks ###
    phone_exp = re.compile("^(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$")
    email_exp = re.compile("^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$")
    
    # Check if name, picture and company are strings
    if (not isinstance(data["name"], str) or 
        not isinstance(data["picture"], str) or
        not isinstance(data["company"], str)):
        abort(400)

    # Check if phone number has a valid format
    if not phone_exp.match(data["phone"]):
        abort(400)

    # Check if email address has a valid format
    if not email_exp.match(data["email"]):
        abort(400)

    # Check if latitude and longitude are floats
    try:
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])
    except ValueError as err:
        abort(400)

    # Check if skills is a list
    if not isinstance(data["skills"], list):
        abort(400)

    tup = (data["name"], data["picture"], data["company"], data["email"], 
           data["phone"], data["latitude"], data["longitude"])
    c.execute('''INSERT INTO users 
                (name, picture, company, email, phone, latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', tup)

    # The last row id will be the user_id for the skill
    last_row = c.lastrowid
    
    skills_to_append = []
    for skill in data["skills"]:
        if (not isinstance(skill.get("name"), str) or 
            not isinstance(skill.get("rating"), int)):
            abort(400)
        skills_to_append.append((skill["name"], skill["rating"], last_row))
    
    c.executemany('''INSERT INTO skills (name, rating, user_id)
                     VALUES (?, ?, ?) ''', skills_to_append)
    
    backend.get_db().commit()
    user = backend.query_db('SELECT * FROM users WHERE id = ?', [last_row], one=True)
    user_skills = backend.query_db('SELECT * FROM skills WHERE user_id = ?', [last_row])
    backend.helpers.format_user(user_skills, user)
    return jsonify(user)


@users.errorhandler(400)
def user_error(e):
    return "400 - Invalid data", 400
