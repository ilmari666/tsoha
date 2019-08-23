from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user,  logout_user
from application import app, db
from application.authors.models import Author

@app.route("/authors")
def list_authors():
  authors = Author.query.all()
  for n in authors:
    print(n)
    print(n.id)

  return render_template("authors/list.html", authors = authors)



@app.route("/authors/<author_id>/", methods=["GET"])
def view_author(author_id):
  author = Author.query.get(author_id)
  return render_template("authors/view.html", author = author)
