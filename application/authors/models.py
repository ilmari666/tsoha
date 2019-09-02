from application import db
from application.models import Base
from sqlalchemy.sql import text

class Author(Base):
  __tablename__ = "author"
  def __init__(self, name, tag):
    self.name=name
    self.tag=tag
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(25))
  tag = db.Column(db.String(12))
  collection = db.relationship("Collection", backref="author", lazy='joined')

  @staticmethod
  def get_authors_with_memberships():
    query = text("SELECT * FROM Author LEFT JOIN Membership ON Author.id=Membership.author_id LEFT JOIN Crew ON Crew.id=Membership.group_id")
    return db.engine.execute(query)
  
  def get_memberships(self):
    query="SELECT g.id, g.name FROM (SELECT group_id FROM membership WHERE author_id="+str(self.id)+") AS ms LEFT JOIN crew AS g ON g.id = ms.group_id"
    return db.engine.execute(query)



class Alias (Base):
  def __init__(self, name, tag, author_id):
    self.name=name
    self.author_id=author_id
    self.tag=tag
  
  __tablename__ = "alias"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  tag = db.Column(db.String(12))
  is_primary = db.Column(db.Boolean)
  author_id =  db.Column(db.Integer, db.ForeignKey('author.id'))


