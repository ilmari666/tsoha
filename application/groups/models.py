from application import db
from application.models import Base
from application.authors.models import Author

class Membership():
  __tablename__ = "membership"
  id = db.Column(db.Integer, primary_key=True)
  author_id =  db.Column(db.Integer, db.ForeignKey('author.id'))
  group_id =  db.Column(db.Integer, db.ForeignKey('group.id'))



class Group(Base):
  __tablename__ = "group"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30))
#  members = db.relationship("Author", backref="groups", lazy=True)
#  members=db.relationship("Author", secondary=memberships, lazy="subquery", backref=db.backref("groups", lazy=True))

