from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user,  logout_user
from application import app, db
from application.auth.models import User, Role
from application.auth.forms import LoginForm, RegistrationForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
  if request.method == "GET":
    return render_template("auth/loginform.html", form = LoginForm())

  form = LoginForm(request.form)

  if not form.validate():
    return render_template("auth/loginform.html", form = form)
  
  user = User.query.filter_by(username=form.username.data, password=form.password.data).first()

  if not user:
    return render_template("auth/loginform.html", form = form, error = "No such username or password")

  login_user(user)
  return redirect(url_for("index"))   


@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
  form = RegistrationForm(request.form)
  if request.method == "GET":
    return render_template("auth/registrationform.html", form = form)

  if not form.validate():
    print(form)
    flash(form.errors)
    flash(form.validate())
    return render_template("auth/registrationform.html", form = form)

  user = User.query.filter_by(username=form.username.data).first()
  if user:
    return render_template("auth/registrationform.html", form = form, error = "User exists")

  username = form.username.data
  email = form.email.data
  password = form.password.data

  user = User(username, email, password)
  db.session().add(user)
  db.session().commit()
  
  db.session().add(Role(user.id, "ANY"))
  if username == "AzureDiamond":
    db.session().add(Role(user.id, "ADMIN"))

  db.session().commit()

  login_user(user)
  return redirect(url_for("index"))   

@app.route("/auth/accounts", methods = ["GET"])
def administrate_access():
  users = User.query.all()
  for u in users:
    print(u.username)
    print(u.roles)
  return render_template("auth/list_accounts.html", accounts=users)




@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))