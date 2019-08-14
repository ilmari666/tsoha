from application import db

class User(db.Model):

  __tablename__ = "account"
  
  id = db.Column(db.Integer, primary_key=True)
  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

  username = db.Column(db.String(144), nullable=False)
  email = db.Column(db.String(144), nullable=False)
  password = db.Column(db.String(144), nullable=False)
  accesslevel = db.Column(db.Integer)
  #uploads = db.relationship("Collection", backref="uploader", lazy=True)
#  uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = password
    self.accesslevel=0
  
  def get_id(self):
    return self.id

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def is_authenticated(self):
    return True

    def get_accesslevel(self):
      return self.accesslevel
