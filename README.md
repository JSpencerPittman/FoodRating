# Food Rating
2300 Databases Project
Rate your favorite foods.

## Setup
### Setup Database
After cloning this repo you will need to setup a database.
In pgAdmin4 create a PostgreSQL database (name must match with the one in the database.ini file described below, as it will be used for connection). In this database copy and paste the `Rating.sql` code. This will initialize all tables and functions necessary for the operation of this project.
If you would like some sample entries to start off with, then also copy and paste `Sample.sql` to populate the database tables.

Create a `database.ini` file in the `src/databases` directory. This file should look like this:
```
[postgresql]
host=localhost
database=<database name>
user=postgres
password=<password used for postgres>
```

### Setup User Interface
With a functional database waiting to be used lets set up the user interface.
Go ahead and create a python virtual environment and then install the required dependencies for PyQT5 and Psycopg2 from `requirements.txt` like so.
```
python -m venv env
# Activate the environment
pip install -r requirements.txt
```

### Run It!
Now all you need to do to start it is:
```
python main.py
```
