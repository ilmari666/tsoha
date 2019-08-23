from application import db
from application.authors.models import Author



class Group(db.Model):
  __tablename__ = "group"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30))
#  members = db.relationship("Author", backref="groups", lazy=True)
#  members=db.relationship("Author", secondary=memberships, lazy="subquery", backref=db.backref("groups", lazy=True))

