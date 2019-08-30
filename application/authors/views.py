from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user,  logout_user, login_required, current_user
from application import app, db
from application.authors.models import Author, Alias
from application.collections.models import Collection
from application.authors.forms import AuthorForm


@app.route("/authors", methods=["GET"])
def list_authors():
  authors = Author.query.all()
  return render_template("authors/list.html", authors = authors)

@app.route("/authors/<author_id>/", methods=["GET"])
def view_author(author_id):
  author = Author.query.get(author_id)
  return render_template("authors/view.html", author = author)


@app.route("/authors/new")
@login_required
def author_new_form():
  authors = Author.query.all()
  form = AuthorForm()
  form.alias_of.choices = [(0, 'Choose existing artist')]+[(a.id, a.name) for a in Author.query.order_by('name')]
  return render_template("authors/new.html", form=form, authors=authors)

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

