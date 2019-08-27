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

In Heroku you have to set the environmental variable HEROKU=1, SQLALCHEMY_DATABASE_URI to point to your database instance as well as the SECRET_KEY.

