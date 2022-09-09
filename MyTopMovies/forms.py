from wtforms import Form, FloatField, StringField, validators

class EditForm(Form):
    rating = FloatField(label="You rating out of 10 e.g. 7.5", validators=[validators.NumberRange(
        min=0.1, max=10, message="The range of rating is between 0.1 and 10"), validators.Optional()], id="rating")

    review = StringField(label="Your Review", validators=[validators.Length(
        max=50, message="Max allowed characters is 50")], id="review")


class AddMovieForm(Form):
    title = StringField(label="Movie title", validators=[validators.InputRequired(message="This input is required.")])
