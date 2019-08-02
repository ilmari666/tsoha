from flask import render_template, request, redirect, url_for
from application import app, db
from application.collections.models import Collection
@app.route("/collections/new")
def collection_form():
  return render_template("collections/new.html")

@app.route("/collections", methods=["POST"])
def collection_create():
#  print(request.form.get("name"))
#  if "file" not in request.files:
#    return redirect(request.url+"?error=no file")
  author = request.form.get("author")
  name = request.form.get("name")
  collection = Collection(name, author)

  db.session().add(collection)
  db.session().commit()
  return redirect(url_for("collections_list"))

@app.route("/collections", methods=["GET"])
def collections_list():
  return render_template("collections/list.html", collections = Collection.query.all())

@app.route("/collections/publish/<collection_id>/", methods=["GET"])
def collection_set_public(collection_id):
  collection = Collection.query.get(collection_id)
  collection.public = True
  db.session().commit()
  return redirect(url_for("collections_list"))

@app.route("/collections/hide/<collection_id>/", methods=["GET"])
def collection_set_private(collection_id):
  collection = Collection.query.get(collection_id)
  collection.public = False
  db.session().commit()
  return redirect(url_for("collections_list"))
