import requests
import sqlite3
import os
import config
from sqlite3 import Error


def check_dir(path_name):
    if not os.path.exists('.' + path_name):
        dir_name = os.path.dirname(path_name)
        os.mkdir(dir_name)

def setup(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
              (id integer primary key,
              name text NOT NULL, 
              picture text, 
              company text, 
              email text, 
              phone text, 
              latitude real, 
              longitude real)''')
    c.execute('''CREATE TABLE IF NOT EXISTS skills
              (id integer primary key,
              name text NOT NULL,
              rating int,
              user_id int,
              foreign key (user_id) references users)''')

def populate(url, conn):
    c = conn.cursor()
    r = requests.get(url)
    if r.status_code == 200:
        print("Success")
        users = []
        skills = []
        for ind, item in enumerate(r.json()):
            users.append(
                    (item.get('name'), 
                    item.get('picture'), 
                    item.get('company'),
                    item.get('email'),
                    item.get('phone'),
                    item.get('latitude'),
                    item.get('longitude')))
            if item.get('skills'):
                for skill in item.get('skills'):
                    skills.append(
                            (skill.get('name'),
                            skill.get('rating'),
                            ind + 1))
        c.executemany('''INSERT INTO users 
                (name, picture, company, email, phone, latitude, longitude) 
                VALUES (?,?,?,?,?,?,?)''', users)
        c.executemany('''INSERT INTO skills 
                (name, rating, user_id)
                VALUES (?,?,?)''', skills)

def create_connection(db_file):
    """Create a connection to a SQLite DB"""
    check_dir(db_file)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys=1")
        setup(conn)
        populate('https://htn-interviews.firebaseio.com/users.json?download', conn)
        conn.commit()
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()

create_connection(config.DATABASE)
