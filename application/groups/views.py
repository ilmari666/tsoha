from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from application import app, db
from application.groups.models import Group
from application.groups.models import Membership
from application.authors.models import Author
from application.groups.forms import GroupForm


@app.route("/groups", methods=["GET"])
def list_groups():
  groups = Group.query.all()
  return render_template("groups/list.html", groups = groups)

@app.route("/groups/new")
@login_required
def group_new_form():
  # for new groups just offer a simple form with group name and acronym
  form = GroupForm()
  authors = Author.query.all()
  return render_template("groups/new.html", form=form, authors=authors)

@app.route("/groups/<group_id>", methods=["GET"])
@login_required
def group_view(group_id):
  group = Group.query.get(group_id)
  members = Membership.query.filter_by(group_id=group_id).with_entities(Membership.member_id)
  authors = Author.query.all()
  form=GroupForm()
  return render_template("groups/new.html", form=form, authors=authors, members=members)

@app.route("/groups", methods=["GET"])
@login_required
def group_create():
  #create group if unique name. forward to existing groups view
  form=GroupForm(request.form)
  name=form.data.name
  abbreviation=form.data.abbreviation
  group=Group.query.filter_by(name=name).first()
  if (group == None):
    group=Group(name, abbreviation)
    db.session().add(group)
    db.session().commit()
  return redirect(url_for("group_view")+"/"+group.id)


@app.route("/groups/<group_id>/add_member/<member_id>", methods=["GET"])
@login_required
def add_member(group_id, member_id):
  membership = Membership.query.filter_by(group_id=group_id).with_entities(Membership.member_id)
  if (membership == None):
    membership = Membership(group_id, member_id)
    db.session().add(membership)
    db.session().commit()
  # possible cache issues will ensue
  return redirect(url_for("group_view")+"/"+group_id)



@app.route("/groups/<group_id>", methods=["POST"])
@login_required
def group_submit(group_id):
  form=GroupForm(request.form)
  name=form.data.name
  abbreviation=form.data.abbreviation
  group=Group.query.filter_by(name=name).first()
  group.abbreviaion=abbreviation
  group.name=name
  db.session().commit()

