from flask import Flask, render_template, redirect, request, url_for
from tables import Movie, Base
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from forms import EditForm, AddMovieForm
import os
import requests

# Constants and Important variables
# Movie DB API key
try:
    MOVIE_DB_KEY = os.environ["MOVIE_DB_KEY"]
except:
    print("Movie DB API Key not found!")
    print("Exiting.....")
    quit()

MOVIE_DB_API_URL = "https://api.themoviedb.org"
MOVIE_DB_IMG_ROOT_URL = "https://image.tmdb.org/t/p/w500"
matching_movies = []


def retrieve_data() -> list[Movie]:
    """Retrieves all movie data from the database

    Returns:
        list[Movie]: movies list
    """
    with Session(engine) as session:
        select_statement = select(Movie).order_by(Movie.rating.desc())
        movies = list(session.scalars(select_statement))
    return movies


def add_movie_details(title: str, year: int, description: str, rating: float, review: str, img_url: str) -> None:
    """Adds a new movie to the database

    Args:
        title (str): Movie title
        year (int): year of release
        description (str): Movie description
        rating (float): rating
        ranking (int): ranking
        review (str): review
        img_url (str): image link
    """
    movie = Movie(title=title, year=year, description=description,
                  rating=rating, review=review, img_url=img_url)
    add_movie(movie)


def add_movie(movie: Movie) -> None:
    try:
        with Session(engine) as session:
            session.add(movie)
            session.commit()
    except:
        print("Failed adding movie")
    else:
        print("Adding Movie...")


def delete_movie(id: int) -> None:
    """Delete the movie from the database

    Args:
        id (int): id of the movie to delete
    """
    try:
        with Session(engine) as session:
            movie = session.get(Movie, id)
            session.delete(movie)
            session.commit()
    except:
        print("Failed deleting movie")
    else:
        print("Deleting movie...")


def update_movie(id, rating: float, review: str) -> None:
    """Updates movie rating and review

    Args:
        id (_type_): id of the movie to update
        rating (float): new rating of the movie
        review (str): new review of movie
    """
    with Session(engine) as session:
        movie: Movie = session.get(Movie, id)
        if rating is not None:
            movie.rating = round(rating, 1)
            print("Updating rating...")

        if review != "":
            movie.review = review
            print("Updating review...")

        session.commit()


def search_movie(movie_name: str) -> list[Movie]:
    request_params = {
        "api_key": MOVIE_DB_KEY,
        "query": movie_name,
    }

    # Get results from API
    response = requests.get(
        f"{MOVIE_DB_API_URL}/3/search/movie", params=request_params)
    response.raise_for_status()
    movies = response.json()["results"]

    indexes_to_remove = []
    # Turn the data into Movie objects
    for index in range(len(movies)):
        movie = movies[index]

        try:
            year = int(movie.get("release_date").split("-")[0])
        except:
            indexes_to_remove.append(movies.index(movie))
            continue

        title = movie.get("title")
        poster_path = movie.get("poster_path")
        description = movie.get("overview").strip()
        rating = movie.get("vote_average")

        if title is None or description is None or description == "":
            indexes_to_remove.append(movies.index(movie))
            continue

        movie = Movie(title=title, year=year, description=description,
                      rating=rating, img_url=f"{MOVIE_DB_IMG_ROOT_URL}{poster_path}")
        movies[index] = movie

    # Remove movies that doesn't match my criteria
    for index in indexes_to_remove:
        try:
            del movies[index]
        except IndexError:
            pass

    for movie in movies:
        if isinstance(movie, dict):
            del movies[movies.index(movie)]

    return movies


def find_movie(movies: list[Movie], title: str, description: str) -> Movie:
    """Searches for the movie with the given title

    Args:
        movies (list[Movie]): List of movies to search in
        title (str): title of the movie to search for

    Returns:
        Movie: matched
    """
    for movie in movies:
        if movie.title == title and movie.description == description:
            return movie


# Database
engine = create_engine("sqlite:///movies-data.db")  # Connect to database
Base.metadata.create_all(engine)    # Create tables


# Server
app = Flask(__name__)
app.secret_key = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

@app.route("/")
def home():
    movies = retrieve_data()
    return render_template("index.html", movies = movies)

@app.route("/edit", methods= ["POST", "GET"])
def edit():
    movie_id = request.args["id"]   # Movie id is sent as argument in url
    form = EditForm(request.form)

    if request.method == "POST" and form.validate():
        update_movie(movie_id, form.rating.data, form.review.data)
        return redirect(url_for('home'))

    # Get movie from database
    with Session(engine) as session:
        movie = session.get(Movie, movie_id)

    return render_template("edit.html", movie= movie, form= form, request_method= request.method)

@app.route("/delete")
def delete():
    delete_movie(request.args["id"])
    return redirect(url_for('home'))

@app.route("/add", methods= ["POST", "GET"])
def add():
    form = AddMovieForm(request.form)
    if request.method == "POST" and form.validate():
        return redirect(url_for('select_movie', search= form.title.data))

    return render_template("add.html", form= form)

@app.route("/select")
def select_movie():
    global matching_movies
    try:
        selected_title = request.args["title"]
        selected_description = request.args["description"]
    except:
        matching_movies = search_movie(request.args["search"])
        return render_template("select.html", movies= matching_movies)
    else:
        movie = find_movie(matching_movies, selected_title, selected_description)
        movie_title = movie.title
        movie_description = movie.description
        add_movie(movie)

        # Get the movie id after adding it to database
        select_statement = select(Movie).where(Movie.title == movie_title).where(Movie.description == movie_description)
        with Session(engine) as session:
            movie:Movie = session.scalars(select_statement).one()
            movie_id = movie.id

        return redirect(url_for('edit', id= movie_id))


if __name__ == '__main__':
    app.run()