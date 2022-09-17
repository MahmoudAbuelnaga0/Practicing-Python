# Database modules
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
# Login modules
from flask_login import UserMixin
# Datetime (I know that's tedious)
from datetime import datetime
# Security modules
from werkzeug.security import generate_password_hash

Base = declarative_base()
# CONFIGURE TABLES


class BlogPost(Base):
    __tablename__ = "blog_posts"

    # Table columns
    id = Column(Integer, primary_key=True)
    title = Column(String(250), unique=True, nullable=False)
    subtitle = Column(String(250), nullable=False)
    date = Column(String(250), nullable=False)
    body = Column(Text, nullable=False)
    img_url = Column(String(250), nullable=False)
    # Column that acts as Foreign Key taht links to "users.id" column (the value that it carries must be present as id in the users table)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Defines a relationship with the User class which complements with the "posts" relationship in User class
    user = relationship("User", back_populates="posts") # self.user represents the User object (user that wrote the post)

    comments = relationship("Comment", back_populates = "post", cascade = "all, delete-orphan")

    def set_attrs(self, data: dict, update_date: bool = False):
        """Set the attributes of the object with the dictionary data

        Args:
            data (dict): dict that have key, value pairs of (attrbute name, value)
        """
        for attribute, value in data.items():
            if attribute == "body": # Remove empty paragraph from body
                if "<p>&nbsp;</p>" in value:
                    value = value[:value.index("<p>&nbsp;</p>")]

            setattr(self, attribute, value)

        if update_date:
            self.date = datetime.now().strftime("%B %d, %Y")

    def __repr__(self) -> str:
        return f"BlogPost(title = '{self.title}')"


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String, nullable=False)

    posts = relationship("BlogPost", back_populates="user",
                         cascade="all, delete-orphan")  # cascade="all, delete-orphan" makes all parent(user) children(posts) get deleted when the user gets deleted
    
    comments = relationship("Comment", back_populates = "user", cascade = "all, delete-orphan")

    def set_attrs(self, data: dict):
        """Set the attributes of the object with the dictionary data

        Args:
            data (dict): dict that have key, value pairs of (attrbute name, value)
        """
        for attribute, value in data.items():
            if attribute == "password":  # If the attribute I'm setting is password
                value = generate_password_hash(
                    value)   # Hash the password value

            setattr(self, attribute, value)

    def __repr__(self) -> str:
        return f"User(name = '{self.name}')"

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key = True)
    text = Column(String(3000), nullable = False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    post_id = Column(Integer, ForeignKey("blog_posts.id"), nullable = False)

    post = relationship("BlogPost", back_populates= "comments")
    user = relationship("User", back_populates = "comments")