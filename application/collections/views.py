from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required

from application import app, db, role_required
from application.collections.models import Collection
from application.collections.forms import CollectionForm
from application.authors.models import Author, Alias
 
@app.route("/collections/new")
@login_required
def collection_new_form():
  return render_template("collections/new.html", form=CollectionForm())

@app.route("/collections/edit/<collection_id>")
@login_required
def collection_edit_form(collection_id):
  c = Collection.query.get(collection_id)
  return render_template("collections/new.html", form=CollectionForm(), name=c.name, author=c.author, public=c.public, id=collection_id)

@app.route("/collections", methods=["POST"])
@login_required
def collection_create():
  form =  CollectionForm(request.form)

  author_alias = form.author.data
  alias=Alias.query.filter_by(name=author_alias).first()
  tag="add"
  #if a non existing author (alias) given create and author and alias, organize later in the flow
  if (alias==None):
    author=Author(author_alias)
    db.session().add(author)
    db.session().commit()
    alias=Alias(author_alias, tag, author.id)
    alias.is_primary=True

    db.session().add(alias)
    db.session().commit()
  else:
    author=Author.query.filter_by(id=alias.id).first()

  #if existing collection
  if ('id' in form):
    collection = Collection.query.get(form.id.data)
    collection.name=form.name.data
    collection.author_id=author.id
    collection.public=form.public.data
  else:
    #author = form.author.data
    name = form.name.data
    collection = Collection(name=name, author=author.id, uploader=current_user.id, alias=alias.id)
    collection.author_id=author.id
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
@role_required(role="ADMIN")
def collection_set_public(collection_id):
  collection = Collection.query.get(collection_id)
  collection.public = True
  db.session().commit()
  return redirect(url_for("collections_list"))

@app.route("/collections/hide/<collection_id>/", methods=["GET"])
@role_required(role="ADMIN")
def collection_set_private(collection_id):
  collection = Collection.query.get(collection_id)
  collection.public = False
  db.session().commit()
  return redirect(url_for("collections_list"))
