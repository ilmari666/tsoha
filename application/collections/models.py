from application import db
from application.auth.models import User
from application.authors.models import Author, Alias
from application.groups.models import Group

class Collection(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
  # name of the collection
  name = db.Column(db.String(144), nullable=False)
  # author
  author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

  alias_id = db.Column(db.Integer, db.ForeignKey('alias.id'), nullable=False)
  # author used alias
  alias = db.relationship("Alias")


#  author_alias = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
  #filename 8+3 including space for dot
  filename = db.Column(db.String(12), nullable=False)
  # uploader id
  uploader = db.relationship("User")
  uploader_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
  # the actual collection
  # collection = db.Column(db.Binary, nullable=False)
  # release primary group
#  label = db.relationship("Group")
  # visibility
  public = db.Column(db.Boolean, unique=False, default=False)

  def __init__(self, name, author, uploader, alias):
    self.name = name
    self.author_id = author
    self.alias_id=alias
    self.done = False
    self.uploader_id=uploader
  


