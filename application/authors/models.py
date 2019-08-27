from application import db
from application.models import Base



class Author(Base):
  __tablename__ = "author"
  def __init__(self, name):
    self.name=name
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  collection = db.relationship("Collection", backref="author", lazy='joined')
#  aliases = db.relationship("Alias",  backref='author', lazy=True)

class Alias (Base):
  def __init__(self, name, tag, author_id):
    self.name=name
    self.author_id=author_id
    self.tag=tag
  
  __tablename__ = "alias"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  tag = db.Column(db.String(12), nullable=False)
  db.Column('is_primary', db.Boolean)
  author_id =  db.Column(db.Integer, db.ForeignKey('author.id'))
  #author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
#  release_id =  db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=False)


