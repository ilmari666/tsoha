from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, SelectField
from wtforms.fields.html5 import EmailField
  
class LoginForm(FlaskForm):
  username = StringField("Username")
  password = PasswordField("Password")
  
  class Meta:
    csrf = True

class RegistrationForm(FlaskForm):
  username = StringField("Username", [validators.Length(min=2)])
  email = EmailField("Email", [validators.DataRequired("Please enter an e-mail address."), validators.Email("Please enter a valid e-mail address.")])
  password = PasswordField("Password", [validators.Length(min=7)])
  password_verify = PasswordField("Verify password", [validators.Length(min=7)])

  def validate(self):
      success = super().validate()
      if not (self.password.data == self.password_verify.data):
        self.password_verify.errors.append("Password mismatch!")
        return False
      return success
  
  class Meta:
    csrf = True
   
class EditForm(FlaskForm):
  username = StringField("Username", [validators.Length(min=2)])
  email = EmailField("Email", [validators.Email()])
  role = SelectField("Access group:")
  class Meta:
    csrf = True
