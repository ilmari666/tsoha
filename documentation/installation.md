Setting up
====================
Requirements:
Python3, PIP

Install other dependencies 
"pip install --user --requirement requirements.txt"

Set system variable SECRET_KEY to your secret.
For example
export SECRET_KEY="ananassalasananas"

Run with
"python3 run.py" which runs an instance at port 5000

After registering a user you can manually grant the user ADMIN priviledges manually with the SQL query
INSERT INTO role (role, user_id) VALUES ("ADMIN", 1)


Deployment to Heroku
--------------------

In Heroku you have to set the environmental variable HEROKU=1, SQLALCHEMY_DATABASE_URI to point to your database instance as well as the SECRET_KEY.
The application also expects a Postgres database set up which you can following these steps:
"heroku pg:psql"
and by selecting a suitable addon
"heroku addons:add heroku-postgresql:hobby-dev"

Setting environmental variables in Heroku is done as follows
"heroku config:set HEROKU=1"
sets the environmental variable HEROKU to value 1



