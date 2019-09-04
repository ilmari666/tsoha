from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, BooleanField, validators,SelectField, HiddenField


class CollectionForm(FlaskForm):
    id = HiddenField("id")

    name = StringField("Collection name", [validators.Length(min=2)])
    author_id = SelectField("Select existing author", coerce=int)
    group_id = SelectField("Select existing group", coerce=int)
    year = StringField("Release year")

    collection = FileField('text', validators=[
        FileRequired(),
        FileAllowed(['txt','asc'], 'Text only!')
    ])


    public = BooleanField("Public")
    upload = FileField("Collection")

 
    class Meta:
        csrf = False
