# 3rd-party packages
from flask import Flask, render_template, render_template_string, request, redirect, url_for
from flask_pymongo import PyMongo

# stdlib
import os
from datetime import datetime

# local
from flask_app.forms import SearchForm, MovieReviewForm
from flask_app.model import MovieClient

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/my_database"
app.config['SECRET_KEY'] = "b'\x8bzG|\x99M@v\xa4\x19\xde\x05\xffwuY'"

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

mongo = PyMongo(app)

client = MovieClient(os.environ.get('OMDB_API_KEY'))

reviews = mongo.db["reviews"]

# --- Do not modify this function ---
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    
    if form.validate_on_submit():
        return redirect(url_for('query_results', query=form.search_query.data))
        
    return render_template('index.html', form=form)

@app.route('/search-results/<query>', methods=['GET'])
def query_results(query):
    try:
        results = client.search(query)
        return render_template('query_results.html', results=results)
    except ValueError as err:
        return render_template('query_results.html', error_msg=err)
    

@app.route('/movies/<movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    try:
        result = client.retrieve_movie_by_id(movie_id)

        if type(result) == dict:
            return render_template('movie_detail.html', error_msg=result['Error'])

        form = MovieReviewForm()
        if form.validate_on_submit():
            review = {
                'date': current_time(),
                'commenter': form.name.data, 
                'content': form.text.data
            }

            mongo.db.reviews.insert_one(review)

            return redirect(request.path)

        reviews_arr = []
        for r in reviews.find():
            reviews_arr.append(r)

        return render_template('movie_detail.html', form=form, movie=result, reviews=reviews_arr)
    except ValueError as err:
        return render_template('movie_detail.html', error_msg=err)
        

# Not a view function, used for creating a string for the current time.
def current_time() -> str:
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')