from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,EmailField,PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class blog(FlaskForm):
    title=StringField("Title",validators=[DataRequired()])
    subtitle=StringField("Subtitle",validators=[DataRequired()])
    img_url=StringField("Backgound URL",validators=[DataRequired()])
    check=CKEditorField("Write Blog")
    submit=SubmitField("Save Post")
    
class registration(FlaskForm):
    email=EmailField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    name=StringField("NAME",validators=[DataRequired()])
    submit=SubmitField("Register")
    
class login(FlaskForm):
    email=EmailField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("Login")
    
class comments(FlaskForm):
    comment_box=CKEditorField("Comments")
    submit=SubmitField("comments")