from flask import Flask
app = Flask(__name__)

#Upload folder for collections 
UPLOAD_FOLDER="upload"

from flask_sqlalchemy import SQLAlchemy
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

# Create necessary db tables
db.create_all()
