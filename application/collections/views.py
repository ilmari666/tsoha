from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from jinja2 import Markup
from sqlalchemy import desc

from application import app, db, role_required
from application.collections.models import Collection
from application.collections.forms import CollectionForm
from application.authors.models import Author
from application.groups.models import Crew
import werkzeug
 
@app.route("/collections/new")
@login_required
def collection_new_form():
  form=CollectionForm()
  form.author_id.choices = [(0, 'Choose artist')]+[(a.id, a.name) for a in Author.query.all()]
  form.group_id.choices = [(0, 'Choose group')]+[(c.id, c.name) for c in Crew.query.all()]
  return render_template("collections/new.html", form=form)


@app.route("/collections/edit/<collection_id>")
@role_required("ADMIN")
def collection_edit_form(collection_id):

  form=CollectionForm()
  form.author_id.choices = [(0, 'Choose artist')]+[(a.id, a.name) for a in Author.query.all()]
  form.group_id.choices = [(0, 'Choose group')]+[(c.id, c.name) for c in Crew.query.all()]
  collection=Collection.query.get(collection_id)
  form.name.default=collection.name
  form.author_id.default = collection.author_id
  form.group_id.default = collection.group_id
  form.year.default=collection.year
  form.id.default=collection.id
  form.process()

  return render_template(
    "collections/new.html",
    form=form,
    collection=Collection.query.get(int(collection_id))
  )


@app.route("/collections/delete/<collection_id>")
@role_required("ADMIN")
def collection_delete(collection_id):
  Collection.query.filter(Collection.id==collection_id).delete()
  db.session().commit()
  return redirect(url_for("collections_list"))


@app.route("/collections", methods=["POST"])
@login_required
def collection_create():
  form =  CollectionForm(request.form)

  filename=request.files["upload"].filename
  upload = request.files["upload"].read()

  author_id = form.author_id.data
  author=Author.query.get(author_id)
  group_id = form.group_id.data
  group = Crew.query.get(group_id)
  print("????")
  print (form.id.data)
  #if existing collection
  if (form.id.data != None):
    collection = Collection.query.get(form.id.data)
    collection.name=form.name.data
    collection.author_id=author.id
    collection.group_id=form.group_id.data
    collection.public=form.public.data
    collection.year=form.year.data
  else:
    #author = form.author.data
    name = form.name.data
    year = form.year.data
    collection = Collection(name=name, author=author.id, group=group.id, uploader=current_user.id, year=year)
    collection.author_id=author.id
    collection.filename=filename
    collection.colly=upload
    db.session().add(collection)


  db.session().commit()
  return redirect(url_for("collections_list"))


@app.route("/collections", methods=["GET"])
def collections_list():
  
  #pythonically set pagination starting from 1
  try:
    page=int(request.args.get("page"))
  except:
    page=1
  #display up to 20 items per page
  paginated = Collection.query.order_by(Collection.date_created.desc()).paginate(page,20,False)
  return render_template("collections/list.html", paginated=paginated)

@app.route("/collections/<collection_id>/", methods=["GET"])
def collections_view(collection_id):
  collection=Collection.query.get(collection_id)
  content=collection.colly.decode("latin_1")
  return render_template("collections/view.html", collection = collection, content=content)


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

