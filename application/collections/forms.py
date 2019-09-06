from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, BooleanField, validators, SelectField, HiddenField

class CollectionForm(FlaskForm):
  name = StringField("Collection name", [validators.Length(min=2)])
  author_id = SelectField("Select existing author", [validators.optional()], coerce=int)
  group_id = SelectField("Select existing group", [validators.optional()], coerce=int)
  year = StringField("Release year",[validators.Length(min=4)])
  upload = FileField('Collection', validators=[validators.optional()])

  class Meta:
    csrf = True

