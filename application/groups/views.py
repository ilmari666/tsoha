from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from application import app, db
from application.groups.models import Group
from application.groups.models import Membership
from application.authors.models import Author
from application.groups.forms import GroupForm, AddMemberForm


@app.route("/groups", methods=["GET"])
def list_groups():
  groups = Group.query.all()
  return render_template("groups/list.html", groups = groups)

@app.route("/groups", methods=["POST"])
@login_required
def group_create():
  #create group if unique name. forward to existing groups view
  form=GroupForm(request.form)
  name=form.name.data
  abbreviation=form.abbreviation.data
  group=Group.query.filter_by(name=name).first()
  if (group == None):
    group=Group(name, abbreviation)
    db.session().add(group)
    db.session().commit()
  return redirect(url_for("group_view")+"/"+group.id)

@app.route("/groups/new")
@login_required
def group_new_form():
  # for new groups just offer a simple form with group name and acronym
  form = GroupForm()
  authors = Author.query.all()
  return render_template("groups/new.html", form=form, authors=authors)

@app.route("/groups/<group_id>", methods=["GET"])
@login_required
def view_group(group_id):
  group = Group.query.get(group_id)
  members = Membership.query.filter_by(group_id=group_id).with_entities(Membership.author_id)
  authors = Author.query.all()
  form=GroupForm()
  memberform=AddMemberForm()
  memberform.member_id.choices = [(0, 'Choose existing artist')]+[(a.id, a.name) for a in Author.query.order_by('name')]

  return render_template("groups/new.html", form=form, memberform=memberform, group=group, authors=authors, members=members)


@app.route("/groups/<group_id>", methods=["POST"])
@login_required
def update_group(group_id):
  form=GroupForm(request.form)
  name=form.name.data
  abbreviation=form.abbreviation.data
  group=Group.query.get(group_id)
  group.abbreviaion=abbreviation
  group.name=name
  db.session().commit()

  return redirect(url_for("view_group", group_id=group.id))


@app.route("/groups/<group_id>/add_member", methods=["GET"])
@login_required
def add_member(group_id):
  form=AddMemberForm(request.form)
  author_id=form.member_id.data
  membership = Membership.query.filter_by(group_id=group_id).with_entities(Membership.author_id)
  if (membership == None):
    membership = Membership(group_id, author_id)
    db.session().add(membership)
    db.session().commit()
  # possible cache issues will ensue
  return redirect(url_for("view_group")+"/"+group_id)


