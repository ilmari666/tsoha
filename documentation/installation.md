Setting up
====================
Requirements:
Python3, PIP

Install other dependencies 
pip install --user --requirement requirements.txt

Set system variable SECRET_KEY to your secret.
For example
export SECRET_KEY="ananassalasananas"

Run with
python3 run.py


Deployment to Heroku

In Heroku you have to set the environmental variable HEROKU=1, SQLALCHEMY_DATABASE_URI to point to your database instance as well as the SECRET_KEY. You also n

Setting environmental variables in Heroku is done as follows
heroku config:set HEROKU=1

you can optionally setup a postgres database with
heroku pg:psql
and by selecting a suitable addon
heroku addons:add heroku-postgresql:hobby-dev


