from flask_wtf import FlaskForm
from wtforms import StringField, FileField, BooleanField, validators

class CollectionForm(FlaskForm):
    name = StringField("Collection name", [validators.Length(min=2)])
    author = StringField("Author name",  [validators.Length(min=1)])
    file = FileField("File")
    public = BooleanField("Public")
 
    class Meta:
        csrf = False