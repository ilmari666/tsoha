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
  authors = Author.query.all()
  #@TODO dont offer authors already in group
  form.alias_of.choices = [(0, 'Choose artist to add')]+[(a.id, a.name) for a in Author.query.order_by('name')]
  return render_template("groups/new.html", form=form, authors=authors)

@app.route("/groups/<group_id>", methods=["GET"])
@login_required
def group_view(group_id):
  group = Group.query.get(group_id)
  members = Membership.query.filter_by(group_id=group_id).with_entities(Membership.member_id)
  authors = Author.query.all()
  form=GroupForm()
  return render_template("groups/new.html", form=form, authors=authors, members=members)

@app.route("/groups/<group_id>", methods=["POST"])
@login_required
def group_submit(group_id):
  form = GroupForm(request.form)
  author_alias = form.author.data

  group = Group.query.get(group_id)
