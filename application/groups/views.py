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
  return redirect(url_for("view_group", group_id=group.id))

@app.route("/groups/new")
@login_required
def group_new_form():
  # for new groups just offer (value=group.name)a simple form with group name and acronym
  form = GroupForm()
  authors = Author.query.all()
  return render_template("groups/new.html", form=form, authors=authors)


@app.route("/groups/<group_id>/add_member", methods=["GET"])
@login_required
def add_member(group_id):
  form=AddMemberForm(request.args)
  author_id=form.member_id.data
  membership = Membership.query.filter_by(group_id=group_id, author_id=author_id).first()
  if (membership == None):
    membership = Membership(group_id, author_id)
    db.session().add(membership)
    db.session().commit()
  return redirect(url_for("view_group", group_id=group_id))

@app.route("/groups/<group_id>/remove_member", methods=["GET"])
@login_required
def remove_member(group_id):
  form=AddMemberForm(request.args)
  author_id=form.member_id.data
  membership=Membership.query.filter_by(group_id=group_id, author_id=author_id).first()
  if (membership is not None):
    print("remove")
    db.session().delete(membership)
    db.session().commit()
    
  return redirect(url_for("view_group", group_id=group_id))



@app.route("/groups/<group_id>", methods=["GET"])
@login_required
def view_group(group_id):
  group_id=int(group_id)
  group = Group.query.get(group_id)
#  members = Membership.query.filter_by(group_id=group_id).with_entities(Membership.author_id)
#  non_members = Author.query.all()
  members = group.get_members_with_release_count()
  form=GroupForm()
  non_members= group.get_non_members()
  memberform=AddMemberForm()
  memberform.member_id.choices = [(0, 'Choose existing artist')]+[(a.id, a.name) for a in non_members]

  return render_template("groups/edit.html", form=form, memberform=memberform, group=group, authors=non_members, members=members)


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


