from application import db
  
# link authors to groups
memberships  = db.Table('memberships',
  db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True),
  db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

class Author(db.Model):
  __tablename__ = "author"
  def __init__(self, name):
    self.name=name
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  collection = db.relationship("Collection", backref="author", lazy='joined')
#  aliases = db.relationship("Alias",  backref='author', lazy=True)

class Alias (db.Model):
  def __init__(self, name, author_id):
    self.name=name
    self.author_id=author_id
  
  __tablename__ = "alias"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  db.Column('is_primary', db.Boolean)
  author_id =  db.Column(db.Integer, db.ForeignKey('author.id'))
  #author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
#  release_id =  db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=False)


