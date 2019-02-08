import sqlite3
from flask import Flask, g, jsonify

DB = 'htn.db'

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
        db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/api/v1.0/')
def index():
    return "Welcome to the API!"

@app.route('/api/v1.0/users/')
def get_users():
    c = get_db().cursor
    users = query_db('select * from users')
    return jsonify(users)

@app.route('/api/v1.0/users/<int:user_id>')
def get_user(user_id):
   c = get_db().cursor()
   user = query_db('select * from users where id = ?', [user_id], one=True)
   return jsonify(user)


