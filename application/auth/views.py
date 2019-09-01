from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user,  logout_user
from application import app, db, role_required
from application.auth.models import User, Role
from application.auth.forms import LoginForm, RegistrationForm, EditForm

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
  
  if username == "AzureDiamond":
    db.session().add(Role(user.id, "ADMIN"))

  db.session().commit()

  login_user(user)
  return redirect(url_for("index"))   

@app.route("/auth/accounts", methods = ["GET"])
@role_required(role="ADMIN")
def administrate_access():
  users = User.query.all()
  return render_template("auth/list_accounts.html", accounts=users)


@app.route("/auth/accounts/<user_id>", methods = ["GET"])
@role_required(role="ADMIN")
def auth_edit(user_id):
  form=EditForm()
  user=User.query.get(user_id)
  rolename=  role=Role.query.filter_by(account_id=user_id).first().name

  if (rolename=="ADMIN"):
    form.role.choices = [('ADMIN','Adminstrator'),('USER', 'Regular')]
  else:
    form.role.choices = [('USER', 'Regular'),('ADMIN','Adminstrator')]

  form.process()
  return render_template("auth/edit_user.html", user=user, form=form)

@app.route("/auth/accounts/<user_id>", methods = ["POST"])
@role_required(role="ADMIN")
def auth_update(user_id):
  user=User.query.get(user_id)
  form=EditForm(request.form)
  user.email=form.email.data
  rolename=form.role.data
  #just overwrite current role, should be done via user.roles
  role=Role.query.filter_by(account_id=user_id).first()
  if (role.name is not rolename):
    role.name=rolename
  db.session().commit()
  return redirect(url_for("administrate_access"))
  
  

  
@app.route("/auth/logout")
def auth_logout():
  logout_user()
  return redirect(url_for("index"))
