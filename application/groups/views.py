from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user,  logout_user
from application import app, db
from application.groups.models import Group

@app.route("/groups")
def list_groups():
  return render_template("groups/list.html", groups = Group.query.all())

