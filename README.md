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
Supports GET and POST requests. GET returns a list of all users in the form:

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

To create a new user, send a POST request to this endpoint matching the JSON format described above. Any additional fields will be ignored. If any keys are missing, the server will return a 400 error.

**One user**: http://localhost:5000/api/v1.0/users/<int:user_id>

Supports GET and PUT requests.

GET: Will return user data in the form specified by the **All users** endpoint.

PUT: Updates data fields corresponding to the keys in the sent JSON. Returns updated user data JSON. Ignores any keys that are not part of the table's schema.

### Skills

Supports GET requests. Returns an HTML table of skill names (Skills) with the number of users with each skill (Count) and average skill rating for each skill (Average Rating). 
Query parameter filtering for min_rating, min_frequency, and sorting is also supported. 

E.g:
http://http://localhost:5000/api/v1.0/skills/?min_rating=5&min_frequency=60&sort=count&order=desc will only create the table for the skills that have a rating >= 5 and a user count of >= 60. The table will be sorted by the 'Count' column in a descending order.

#### More details on query params

+ *min_rating* -> integer
+ *min_frequency* -> integer
+ *sort* -> x in ["name", "count", "rating"]
+ *order* -> x in ["asc", "desc"]

**min_rating** : The minimum rating for the skill to be considered in the table creation. I.e. if *min_rating* is 5, only the skills with a rating >= 5 will be considered during the counting as well as for the average rating calculation.

**min_frequency** : The minimum frequency for a skill to appear in the table. I.e. if the count value for the skill is less than *min_frequency*, the skill will not appear on the table.

**sort** : Specifies which column the table is being sorted by. Default is unsorted.

**order** : Describes the order in which the values are displayed. Defaults to ascending order("asc").
