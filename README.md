# HTN-2019 Backend Challenge

## Getting Started
1. Clone this repository.
2. Create a virtual environment in the top level directory of this project. The steps on creating a virtual environment in Python 3 are listed [here](https://docs.python.org/3/library/venv.html).
3. Activate your virtual environment.
4. In your terminal, run `pip install -r requirements.txt` to install all dependencies this project uses.
5. To populate the database, run `python populate_db.py`.
6. Finally, to launch the Flask app, run `python run.py`. Once you've executed the command, click on this [link](http://localhost:5000/api/v1.0/) to check if the app is running fine. You should see "Welcome to this API!" at this endpoint.

## Endpoints

### Users

**All users**: http://localhost:5000/api/v1.0/users
Supports GET requests. Returns a list of users in the form:

```json
{
  "name": <string>,
  "picture": <string>,
  "company": <string>,
  "email": <string>,
  "phone": <string>,
  "latitude": <float>,
  "longitude": <float>,
  "skills": [
    {
      "name": <string>,
      "rating": <int>
    }
  ]
}
```

**One user**: http://localhost:5000/api/v1.0/users/<int:user_id>

Supports GET and PUT requests.

GET: Will return user data in the form specified by the **All users** endpoint.

PUT: Updates data fields corresponding to the keys in the sent JSON. Returns updated user data JSON. Ignores any keys that are not part of the table's schema.

### Skills

Supports GET requests. Returns an HTML table of skill names (Skills) with the number of users with each skill (Count) and average skill rating for each skill (Average Rating). 
Query parameter filtering for min_rating and min_frequency is also supported. E.g:

http://http://localhost:5000/api/v1.0/skills/?min_rating=5&min_frequency=60 will only create the table for the skills that have a rating >= 5 and a user count of >= 60.
