from application import db
from application.models import Base
from application.authors.models import Author
from sqlalchemy.sql import text

class Group(Base):
  __tablename__ = "group"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30),nullable=False)
  abbreviation = db.Column(db.String(7))
  def __init__(self, name, abbreviation):
    self.name=name
    self.abbreviation=abbreviation

  def get_members(self):
    query="SELECT a.id, a.name FROM membership AS ms LEFT JOIN author AS a ON a.id = ms.author_id WHERE group_id = "+str(self.id)
    return db.engine.execute(query)

  def get_non_members(self):
    query="SELECT a.id, a.name FROM author AS a WHERE a.id NOT IN (SELECT author_id FROM membership WHERE group_id = "+str(self.id)+")"
    return db.engine.execute(query)

  def get_members_with_release_count(self):
    # get member details including amount of collections credited
    query="SELECT author_id, release_count, name, tag FROM (SELECT ms.author_id as author_id, COUNT(ms.author_id) as release_count FROM (SELECT author_id FROM membership WHERE group_id="+str(self.id)+") as ms LEFT JOIN Collection as c ON ms.author_id = c.author_id GROUP BY ms.author_id) LEFT JOIN author as a ON author_id = a.id"

    postgresquery="SELECT ff.count, author.name, author.id FROM public.author LEFT JOIN (SELECT * FROM public.membership WHERE group_id="+str(self.id)+") AS ms ON ms.author_id=author.id LEFT JOIN public.group ON ms.group_id = public.group.id LEFT JOIN (SELECT author_id, COUNT(*) FROM collection GROUP BY collection.author_id) AS ff ON ff.author_id=author.id;"

    return db.engine.execute(postgresquery)

  def get_members_with_alias_and_release_count(self):
    query="SELECT a.author_id, release_count, name FROM (SELECT ms.author_id AS author_id, COUNT(ms.author_id) AS release_count FROM (SELECT author_id FROM membership WHERE group_id="+str(self.id)+") AS ms LEFT JOIN Collection AS c ON ms.author_id = c.author_id GROUP BY ms.author_id) LEFT JOIN alias AS a ON ms.author_id = a.author_id WHERE a.is_primary=True"
    return db.engine.execute(query)





class Membership(db.Model):
  __tablename__ = "membership"
  id = db.Column(db.Integer, primary_key=True)
  author_id =  db.Column(db.Integer, db.ForeignKey('author.id'))
  author = db.relationship("Author", uselist=False)
  group_id =  db.Column(db.Integer, db.ForeignKey('group.id'))
  def __init__(self, group_id, author_id):
    self.group_id=group_id
    self.author_id=author_id

