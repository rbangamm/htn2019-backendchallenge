import sqlite3
import config
from flask import Flask, g
from backend.api.users import users
from backend.api.skills import skills

app = Flask(__name__)

app.register_blueprint(users, url_prefix='%s/users' % config.ROOT)
app.register_blueprint(skills, url_prefix='%s/skills' % config.ROOT)

@app.route('%s/' % config.ROOT)
def index():
    return "Welcome to this API!"

## DB HELPER FUNCTIONS
DB = config.DATABASE
SCHEMAS = {}

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

def get_schema(table_name):
    if SCHEMAS.get(table_name) is None:
        cur = get_db().execute('select * from %s' % table_name)
        return [member[0] for member in cur.description]
    return SCHEMAS.get(table_name)
        

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
