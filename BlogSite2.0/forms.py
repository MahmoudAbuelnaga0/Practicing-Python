from wtforms import Form, StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, URL, Length, Email
from flask_ckeditor import CKEditorField

#WTForm 
class CreatePostForm(Form):
    title = StringField("Blog Post Title", validators=[InputRequired()])
    subtitle = StringField("Subtitle", validators=[InputRequired()])
    # author = StringField("Your Name", validators=[InputRequired()], id = "author")
    img_url = StringField("Blog Image URL", validators=[InputRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[InputRequired()])

class RegistrationForm(Form):
    name = StringField(label = "Name", validators=[InputRequired(), Length(max=250)])
    email = EmailField(label = "Email", validators=[InputRequired(), Length(max=250), Email()])
    password = PasswordField(label= "Password", validators=[InputRequired(), Length(max=30)])
    
class LoginForm(Form):
    email = EmailField(label = "Email", validators=[InputRequired(), Length(max=250), Email()])
    password = PasswordField(label= "Password", validators=[InputRequired(), Length(max=30)])

class CommentForm(Form):
    comment = CKEditorField(label="Comment", validators=[InputRequired(), Length(max = 3000)])