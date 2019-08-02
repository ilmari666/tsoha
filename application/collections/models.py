from application import db

class Collection(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
  # name of the collection
  name = db.Column(db.String(144), nullable=False)
  # author
  author = db.Column(db.Integer, nullable=False)
  # filename 8+3 including space for dot
  # filename = db.Column(db.String(12), nullable=False)
  # author used alias
  #author_alias = db.Column(db.Integer, nullable=False)
  # uploader id
  #uploader = db.Column(db.Integer, nullable=False)
  # the actual collection
  #collection = db.Column(db.Binary, nullable=False)
  # release primary group
  #label = db.Column(db.Integer)
  # visibility
  public = db.Column(db.Boolean, unique=False, default=False)

  def __init__(self, name, author):
    self.name = name
    self.author = author
    self.done = False

