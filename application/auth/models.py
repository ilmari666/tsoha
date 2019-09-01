from application import db
from application.models import Base
from sqlalchemy import UniqueConstraint

class User(Base):

  __tablename__ = "account"
  __table_args__ = (UniqueConstraint('username', 'email', name='_user_uc'),)

  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

  username = db.Column(db.String(144), nullable=False, unique=True)
  email = db.Column(db.String(144), nullable=False, unique=True)
  password = db.Column(db.String(144), nullable=False)
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
    for role in self.roles:
      if role=='ADMIN':
        return True
    return False

  def get_roles(self):
    def get_rolename(role):
      return role.name
    return list(map(get_rolename, self.roles))

class Role(Base):
  def __init__(self, account_id, role):
    self.account_id=account_id
    self.name=role

  name = db.Column(db.String(12), nullable=False)
  account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
