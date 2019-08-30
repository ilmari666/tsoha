from flask_wtf import FlaskForm
from wtforms import StringField, FileField, IntegerField, BooleanField, validators, SelectField, HiddenField

class GroupForm(FlaskForm):
    id = HiddenField("id")
    name = StringField("Group name", [validators.Length(min=2)])
    abbreviation = StringField("Abbreviation",  [validators.Length(min=1)])

class AddMemberForm(FlaskForm):
    member_id = SelectField("Select new member to add", coerce=int)
    

#= SelectField(u'Group', coerce=int)