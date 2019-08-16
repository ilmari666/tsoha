from application import db
from application.auth.models import User

class Collection(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
  # name of the collection
  name = db.Column(db.String(144), nullable=False)
  # author
  author = db.relationship("Author")

  author = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
  # author used alias
  alias = db.relationship("Alias")


#  author_alias = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
  #filename 8+3 including space for dot
  filename = db.Column(db.String(12), nullable=False)
  # uploader id
  uploader = db.relationship("User")
  uploader_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
  # the actual collection
#  collection = db.Column(db.Binary, nullable=False)
  # release primary group
#  label = db.relationship("Group")
  # visibility
  public = db.Column(db.Boolean, unique=False, default=False)

  def __init__(self, name, author, uploader):
    self.name = name
    self.author = author
    self.done = False
    self.uploader_id=uploader


  #  uploads = db.relationship("Collection", backref='account', lazy=True)
  
class Author(db.Model):
  __tablename__ = "author"
  id = db.Column(db.Integer, primary_key=True)
  primary_alias = db.Column(db.String(30), nullable=False)
  collection = db.relationship("Collection")
  #aliases = db.relationship("Alias", backref='author', lazy=True)
  #groups=db.Column()
  aliases = db.relationship("Alias")

#class Group(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(30))
#    members = db.relationship("Author", backref="groups", lazy=True)

class Alias (db.Model):
  def __init__(self, name, author_id):
    self.name=name
    self.author_id=author_id
  
  __tablename__ = "alias"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
  release_id =  db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=False)
#    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
   # author = db.relationship("Author", backref="aliases")
