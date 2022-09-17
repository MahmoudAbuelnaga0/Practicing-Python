# Flask server modules
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
# Hashing modules
from werkzeug.security import check_password_hash
# Database modules
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from tables import BlogPost, Base, User
# Form modules
from forms import CreatePostForm, LoginForm, RegistrationForm


# CONNECT TO DB
engine = create_engine('sqlite:///blog.db?check_same_thread=False')
Base.metadata.create_all(engine)


# Setup Sever
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
##LoginManager to manage user sessions
login_manager = LoginManager(app)
###This callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    with Session(engine) as session:
        user:User = session.get(User, user_id)

    return user


@app.route('/')
def get_all_posts():
    with Session(engine) as session:
        posts = list(session.scalars(select(BlogPost)))

    return render_template("index.html", all_posts=posts)


@app.route('/register', methods = ["POST", "GET"])
def register():
    form = RegistrationForm(request.form)
    
    if request.method == "POST" and form.validate():    # If the user filled the form and sent it, and the form validates
        # Create a new user
        new_user = User()
        new_user.set_attrs(dict(request.form))  # Fill new_user attributes with the data received from Form

        # Add him to my database
        session = Session(engine)

        try:    # Try adding user to the database
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        except: # If failed that means that the email already exists in the database
            session.close()
            flash('That email already exists. Try logging in.', 'warning')
            return redirect(url_for('login'))
        else:
            session.close()

        # Login the new user
        login_user(new_user)

        # Redirect user to home page
        return redirect(url_for('get_all_posts'))

    return render_template("register.html", form = form, request_method = request.method)


@app.route('/login', methods = ["POST", "GET"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():    # If user tried to login
        # Go check for the user with the email sent in form
        with Session(engine) as session:
            user:User = session.scalars(select(User).where(User.email == form.email.data)).first()

        if user is None:    # If user wasn't found
            form.email.errors.append("That email doesn't exist.")    # I could have done: flash("_____") --> return redirect(url_for('login')) --> add templating required in "login.html" to show flash message
        else:   # If found
            # Check that he entered correct password
            pass_correct = check_password_hash(user.password, form.password.data)

            if pass_correct:
                login_user(user)    # Login user and give him authentication (access)
                # Redirect to homepage
                return redirect(url_for('get_all_posts'))
            else:
                form.password.errors.append("Password is incorrect.")

    return render_template("login.html", form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()   # Logout user and delete his cookies
    # Redirect to homepage
    return redirect(url_for('get_all_posts'))


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    with Session(engine) as session:
        requested_post:BlogPost = session.get(BlogPost, post_id)
        author = requested_post.user

    if requested_post is None:
        return abort(404)
   
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/add", methods = ["POST", "GET"])
@login_required
def add_new_post():
    form = CreatePostForm(request.form)
    if request.method == "POST" and form.validate():
        # Create new post
        new_post = BlogPost()
        new_post.set_attrs(dict(request.form), update_date=True)    # Set its attributes
        new_post.author_id = current_user.id

        # Add it to the database
        with Session(engine) as session:
            session.add(new_post)
            session.commit()

        return redirect(url_for("get_all_posts"))

    return render_template("make-post.html", form=form, request_method = request.method)


@app.route("/edit/<int:post_id>", methods = ["POST", "GET"])
@login_required
def edit_post(post_id:int):
    ##Get the record we want to edit from the database
    session = Session(engine)
    post_to_edit:BlogPost = session.get(BlogPost, post_id)

    ## If request method was GET, the form will be filled with the record data
    ## If request method was POST, the form will be filled with the form data
    form = CreatePostForm(request.form, post_to_edit)

    if request.method == "POST" and form.validate():
        # Update record data in database
        post_to_edit.set_attrs(dict(request.form))
        session.commit()
        session.close()

        # Show the post after update
        return redirect(url_for('show_post', post_id = post_id))

    session.close()
    return render_template("make-post.html", form = form, request_method = request.method, post_id = post_id)


@app.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    with Session(engine) as session:
        post_to_delete = session.get(BlogPost, post_id)
        if post_to_delete is not None:
            session.delete(post_to_delete)
            session.commit()

    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug= True)
