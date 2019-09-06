from application import db
from application.models import Base
from application.authors.models import Author
from sqlalchemy.sql import text

class Crew(Base):
  __tablename__ = "crew"
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
    query="select author.id,  author.name, author.tag, count(collection.author_id) as release_count from (select * from membership where group_id="+str(self.id)+") as ms LEFT JOIN author on author.id=ms.author_id LEFT JOIN collection ON collection.author_id=ms.author_id GROUP BY collection.author_id, author.name, author.tag, author.id;"
    return db.engine.execute(query)

  def get_members_with_alias_and_release_count(self):
    query="SELECT a.author_id, release_count, name FROM (SELECT ms.author_id AS author_id, COUNT(ms.author_id) AS release_count FROM (SELECT author_id FROM membership WHERE group_id="+str(self.id)+") AS ms LEFT JOIN Collection AS c ON ms.author_id = c.author_id GROUP BY ms.author_id) LEFT JOIN alias AS a ON ms.author_id = a.author_id WHERE a.is_primary=True"
    return db.engine.execute(query)

  @staticmethod
  def get_groups_with_stats():
    query = text("SELECT name, r.abbreviation as abbreviation, count(ms.id) as member_count, r.id as id, release_count "
    "FROM (select g.abbreviation as abbreviation, g.name as name, g.id as id, count(c.group_id) as release_count "
    "FROM Crew as g LEFT JOIN (SELECT * FROM Collection WHERE public=true ) AS c  ON g.id=c.group_id GROUP BY c.group_id, g.name, g.id) AS r LEFT JOIN Membership AS ms ON r.id = ms.group_id GROUP BY r.name, r.id, r.release_count, ms.group_id, r.abbreviation;"
    return db.engine.execute(query)



class Membership(db.Model):
  __tablename__ = "membership"
  id = db.Column(db.Integer, primary_key=True)
  author_id =  db.Column(db.Integer, db.ForeignKey('author.id'))
  author = db.relationship("Author", uselist=False)
  group_id =  db.Column(db.Integer, db.ForeignKey('crew.id'))
  def __init__(self, group_id, author_id):
    self.group_id=group_id
    self.author_id=author_id

