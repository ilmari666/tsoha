from flask_wtf import FlaskForm
from wtforms import StringField, FileField, IntegerField, BooleanField, validators, SelectField

class AuthorForm(FlaskForm):
    name = StringField("Artist name", [validators.Length(min=2)])
    tag = StringField("Tag",  [validators.Length(min=1)])
    alias_of = SelectField("Alias of", coerce=int)
    class Meta:
      csrf = True

#= SelectField(u'Group', coerce=int)