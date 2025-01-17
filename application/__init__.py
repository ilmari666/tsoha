from flask import Flask
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__,static_url_path='/static')
csrf = CSRFProtect(app)
#csrf.init_app(app)

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


from os import urandom
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."





# roles in login_required
from functools import wraps
def role_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()

            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "ANY":
                unauthorized = True
                
                for user_role in current_user.get_roles():
                    if user_role == role:
                        unauthorized = False
                        break

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


# Logging in
from application.auth.models import User

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


# Load application views and models
from application.auth import models 
from application.groups import models 
from application.authors import models 

from application.collections import models



from application import views
from application.collections import views
from application.auth import views
from application.groups import views
from application.authors import views




# Create necessary db tables
if os.environ.get("HEROKU"):

  try:
    db.create_all()
  except:
    pass
else:
  db.create_all()
