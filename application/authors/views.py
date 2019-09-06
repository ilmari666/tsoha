from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user,  logout_user, login_required, current_user
from application import app, db, role_required
from application.authors.models import Author, Alias
from application.groups.models import Membership
from application.collections.models import Collection
from application.authors.forms import AuthorForm


@app.route("/authors", methods=["GET"])
def list_authors():
  authors = Author.query.all()
  return render_template("authors/list.html", authors = authors)

@app.route("/authors/<author_id>/", methods=["GET"])
def view_author(author_id):
  author = Author.query.get(author_id)
  memberships=author.get_memberships()
  collections=Collection.query.filter_by(author_id=author.id)
  return render_template("authors/view.html", author = author, memberships=memberships, collections=collections)

@app.route("/authors/new")
@login_required
def author_new_form():
  form = AuthorForm()
#  form.alias_of.choices = [(0, 'Choose existing artist')]+[(a.id, a.name) for a in Author.query.order_by('name')]
  return render_template("authors/new.html", form=form)

@app.route("/authors/edit/<author_id>", methods=["GET"])
@role_required("ADMIN")
def author_edit_form(author_id):
  author = Author.query.get(author_id)
  
  form=AuthorForm()
  form.name.default=author.name
  form.tag.default=author.tag
  form.process()

  return render_template("authors/new.html", form=form, author=author)

@app.route("/authors/<author_id>/", methods=["POST"])
@role_required("ADMIN")
def author_update(author_id):
  form =  AuthorForm(request.form)
  author = Author.query.get(author_id)
  if not form.validate():
    return render_template("authors/new.html", author=author, form=form)

  author.name=form.name.data
  author.tag=form.tag.data
  db.session().commit()
  return redirect(url_for("list_authors"))

@app.route("/authors/delete/<author_id>", methods=["GET","POST"])
@role_required("ADMIN")
def delete_author(author_id):
  #delete traces of author
  Membership.query.filter_by(author_id=author_id).delete()
  Collection.query.filter_by(author_id=author_id.delete())
  Author.query.filter_by(id=author_id).delete()

  db.session.commit()
  return redirect(url_for("list_authors"))


@app.route("/authors", methods=["POST"])
@login_required
def author_create():

  # if author name does not exist and it's not set as an alias to existing author create a new author with the alias

  form =  AuthorForm(request.form)
  name=form.name.data
  tag=form.tag.data

  author=Author.query.filter_by(name=name).first()

  if (author==None):
    author=Author(name, tag)
    db.session().add(author)
    db.session().commit()
  return redirect(url_for("list_authors"))

