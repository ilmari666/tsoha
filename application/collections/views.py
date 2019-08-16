from flask import render_template, request, redirect, url_for
from application import app, db
from application.collections.models import Collection
from application.collections.forms import CollectionForm
from flask_login import login_required, current_user

@app.route("/collections/new")
@login_required
def collection_new_form():
  return render_template("collections/new.html", form=CollectionForm())

@app.route("/collections/edit//<collection_id>")
@login_required
def collection_edit_form(collection_id):
  c = Collection.query.get(collection_id)
  return render_template("collections/new.html", form=CollectionForm(), name=c.name, author=c.author, public=c.public, id=collection_id)

@app.route("/collections", methods=["POST"])
@login_required
def collection_create():
  form =  CollectionForm(request.form)
  if ('id' in form):
    collection = Collection.query.get(form.id.data)
    collection.name=form.name.data
    collection.author=form.author.data
    collection.public=form.public.data
  else:
    author = form.author.data
    name = form.name.data
    collection = Collection(name, author, current_user.id)
    collection.filename=form.filename.data
    db.session().add(collection)


  db.session().commit()
  return redirect(url_for("collections_list"))


#@app.route("/collections", methods=["POST"])
#def collection_create():
#  author = request.form.get("author")
#  name = request.form.get("name")
#  collection = Collection(name, author)
#  db.session().commit()
#  return redirect(url_for("collections_list"))


@app.route("/collections", methods=["GET"])
def collections_list():
  return render_template("collections/list.html", collections = Collection.query.all())

@app.route("/collections/publish/<collection_id>/", methods=["GET"])
@login_required
def collection_set_public(collection_id):
  collection = Collection.query.get(collection_id)
  collection.public = True
  db.session().commit()
  return redirect(url_for("collections_list"))

@app.route("/collections/hide/<collection_id>/", methods=["GET"])
@login_required
def collection_set_private(collection_id):
  collection = Collection.query.get(collection_id)
  collection.public = False
  db.session().commit()
  return redirect(url_for("collections_list"))
