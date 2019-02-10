import backend
from flask import Blueprint, jsonify

users = Blueprint('users', __name__)

@users.route('/')
def get_users():
    c = backend.get_db().cursor()
    users = backend.query_db('select * from users')
    return jsonify(users)

@users.route('/<int:user_id>')
def get_user(user_id):
   c = backend.get_db().cursor()
   user = backend.query_db(
           'select * from users where id = ?', [user_id], one=True)
   return jsonify(user)


