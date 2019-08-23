from application import db
from sqlalchemy import UniqueConstraint

class User(db.Model):

  __tablename__ = "account"
  __table_args__ = (UniqueConstraint('username', 'email', name='_user_uc'),)

  id = db.Column(db.Integer, primary_key=True)
  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

  username = db.Column(db.String(144), nullable=False)
  email = db.Column(db.String(144), nullable=False)
  password = db.Column(db.String(144), nullable=False)
  accesslevel = db.Column(db.Integer)
  roles = db.relationship("Role")
  #uploads = db.relationship("Collection", backref="uploader", lazy=True)
#  uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = password

  def get_id(self):
    return self.id

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def is_authenticated(self):
    return True

  def is_admin(self):
    print ("IS_ADMIN ??")
    for role in self.roles:
      if role=='ADMIN':
        return True
    return False

  def get_roles(self):
    def get_rolename(role):
      return role.name
    return list(get_rolename, map(self.roles))

class Role(db.Model):
  def __init__(self, account_id, role):
    self.account_id=account_id
    self.name=role

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(12), nullable=False)
  account_id = db.Column(db.Integer, db.ForeignKey('account.id'))