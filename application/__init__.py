from flask import Flask
app = Flask(__name__)

#Upload folder for collections 
UPLOAD_FOLDER="upload"

from flask_sqlalchemy import SQLAlchemy

import os

# Heroku
if os.environ.get("HEROKU"):
  app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
  # Create a db called archive
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///archive.db"
  # Print out all queries
  app.config["SQLALCHEMY_ECHO"] = True


# Define upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create a database instance
db = SQLAlchemy(app)

from application import views
from application.collections import models
from application.collections import views

# Users
from application.auth import models 
from application.auth import views


# Logging in
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


# Create necessary db tables
try:
  db.create_all()
except:
  pass
