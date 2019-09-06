from application import db
from application.models import Base
from application.auth.models import User
from application.authors.models import Author, Alias
from application.groups.models import Crew
from sqlalchemy.sql import text

class Collection(db.Model):
  __tablename__="collection"
  id = db.Column(db.Integer, primary_key=True)
  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
  # name of the collection
  name = db.Column(db.String(144), nullable=False)
  # author
  author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
  #filename 8+3 including space for dot
  filename = db.Column(db.String(12), nullable=False)
  # uploader id
  uploader = db.relationship("User")
  uploader_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
  # the actual collection
  colly = db.Column(db.Binary, nullable=False)
  # release primary group
  group = db.relationship("Crew")
  group_id = db.Column(db.Integer, db.ForeignKey('crew.id'))
  # release year
  year=db.Column(db.Integer)
  # visibility
  public = db.Column(db.Boolean, unique=False, default=False)


  def __init__(self, name, author, group, uploader, year):
    self.name = name
    self.author_id = author
    self.group_id = group
    self.uploader_id=uploader
    self.year=year
  
  @staticmethod
  def get_stats():
    query = text("SELECT "
    "count(c.id) as collection_count, "
    "count(DISTINCT a.id) as author_count, "
    "count(DISTINCT u.id) as uploader_count, "
    "count(DISTINCT g.id) as group_count "
    "FROM (SELECT * FROM Collection WHERE public=true) AS c "
    "LEFT JOIN Author AS a ON (c.author_id=a.id) " 
    "LEFT JOIN Crew AS g ON (c.group_id=g.id) "
    "LEFT JOIN Account AS u ON (c.uploader_id=u.id) "
    )
    return db.engine.execute(query)
 
  @staticmethod
  def get_stats_admin():
    query = text("SELECT "
    "count(c.id) as collection_count, "
    "count(DISTINCT a.id) as author_count, "
    "count(DISTINCT u.id) as uploader_count, "
    "count(DISTINCT g.id) as group_count, "
    "count(CASE WHEN c.public THEN 1 END) as published_count "
    "FROM (SELECT * FROM Collection) AS c "
    "LEFT JOIN Author AS a ON (c.author_id=a.id) " 
    "LEFT JOIN Crew AS g ON (c.group_id=g.id) "
    "LEFT JOIN Account AS u ON (c.uploader_id=u.id) "
    )
    return db.engine.execute(query)
