from flask import render_template, request, redirect
from application import app, db
from application.collections.models import Collection
@app.route("/collections/new")
def collection_form():
  return render_template("collections/new.html")

@app.route("/collections", methods=["POST"])
def collection_create():
  print(request.form.get("name"))
  if "file" not in request.files:
    return redirect(request.url+"?error=no file")
    #return redirect(geturl_for('error'))
  c = Collection(request.form.get("name"))
  db.session().add(c)
  db.session().commit()
  return "hello world"

@app.route("/collections", methods=["GET"])
def list_collections():
  return "listing all collections..."
