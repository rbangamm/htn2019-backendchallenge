import backend
import backend.helpers
from flask import Blueprint, jsonify, request

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
