from flask import render_template, request, redirect
from application import app

@app.route("/")
def index():
  return redirect("/collections")

