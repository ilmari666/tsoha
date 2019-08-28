from application import db
from application.models import Base
from application.authors.models import Author

class Group(Base):
  __tablename__ = "group"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30))

class Membership():
  __tablename__ = "membership"
  id = db.Column(db.Integer, primary_key=True)
  author_id =  db.Column(db.Integer, db.ForeignKey('author.id'))
  group_id =  db.Column(db.Integer, db.ForeignKey('group.id'))
  def __init__(self, group_id, author_id):
    self.group_id=group_id
    self.author_id=author_id

