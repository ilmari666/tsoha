from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required

from application import app, db, role_required
from application.collections.models import Collection
from application.collections.forms import CollectionForm
from application.authors.models import Author
from application.groups.models import Group
 
@app.route("/collections/new")
@login_required
def collection_new_form():
  form=CollectionForm()
  form.author_id.choices = [(0, 'Choose artist')]+[(a.id, a.name) for a in Author.query.all()]
  form.group_id.choices = [(0, 'Choose group')]+[(a.id, a.name) for a in Group.query.all()]
  return render_template("collections/new.html", form=form)


@app.route("/collections/edit/<collection_id>")
@login_required
def collection_edit_form(collection_id):
  return render_template(
    "collections/new.html",
    form=CollectionForm(),
    collection=Collection.query.get(collection_id)
  )

@app.route("/collections", methods=["POST"])
@login_required
def collection_create():
  form =  CollectionForm(request.form)

  filename=request.files["upload"].filename
  upload = request.files["upload"].read()

  author_id = form.author_id.data
  author=Author.query.get(author_id)
  group_id = form.group_id.data
  group = Group.query.get(group_id)
  
  #if a non existing author (alias) given create and author and alias, organize later in the flow
  #author_name = form.author_name.data
  #if (author_id==0 and author_name != ""):
  #  author=Author(author_name, author_name)
  #  db.session().add(author)
  #  db.session().commit()

  #if existing collection
  if ('id' in form):
    collection = Collection.query.get(form.id.data)
    collection.name=form.name.data
    collection.author_id=author.id
    collection.group_id=form.group.data
    collection.public=form.public.data
  else:
    #author = form.author.data
    name = form.name.data
    collection = Collection(name=name, author=author.id, group=group_id, uploader=current_user.id)
    collection.author_id=author.id
    collection.filename=filename
    collection.colly=upload
    db.session().add(collection)


  db.session().commit()
  return redirect(url_for("collections_list"))


@app.route("/collections", methods=["GET"])
def collections_list():
  return render_template("collections/list.html", collections = Collection.query.all())

@app.route("/collections/<collection_id>/", methods=["GET"])
def collections_view(collection_id):
  return render_template("collections/view.html", collection = Collection.query.get(collection_id))


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
