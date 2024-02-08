from flask import Flask, render_template, session, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson import ObjectId
from movie_db import Movies # Ensure this import reflects the corrected Movies class structure

app = Flask(__name__)

# MongoDB setup
app.config["MONGO_URI"] = "mongodb+srv://user_2:Zwut9Ul2IlLG2noo@cluster0.37fbdrx.mongodb.net/Movies"
mongo = PyMongo(app)
db = mongo.db
movies_collection = db["Movies"]
user_collection = db["Users"]

movies_r = Movies() # Assuming Movies is correctly refactored

@app.route("/") 
def hello(): 
    return render_template('index.html') 

@app.route('/movies', methods=['GET'])
def get_movies():
    movieList = movies_r.getMovie()
    return jsonify({'movies': movieList})

@app.route('/movies/<string:_id>', methods=['GET'])
def get_movie_by_id(_id):
    movie = movies_r.getMovie_by_id(_id)
    if movie is None:
        return jsonify({'message': 'Movie not found'}), 404
    else:
        return jsonify(movie), 200

@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    movie_id = movies_r.createMovie(data['imdb'], data['name'], data['price'], data['status'], data['overview'], data['image'])
    return jsonify({'message': 'Movie created successfully', 'movie_id': movie_id}), 201

@app.route('/movies/<string:_id>', methods=['PUT'])
def update_movie(_id):
    data = request.get_json()
    result = movies_r.editMovie(_id, data)
    if result.modified_count == 0:
        return jsonify({'message': 'No changes made or movie not found'}), 404
    return jsonify({'message': 'Movie updated successfully'}), 200

@app.route('/movies/<string:_id>', methods=['DELETE'])
def delete_movie(_id):
    movies_r.deleteMovie(_id)
    return jsonify({'message': 'Movie deleted successfully'}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = user_collection.find_one({"email": data['email'], "password": data['password']})
    if user:
        session['user_id'] = str(user['_id'])
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/users/<string:email>', methods=['GET'])
def get_user_by_email(email):
    user = user_collection.find_one({"email": email})
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify(user), 200



if __name__ == '__main__':
    app.run(debug=True)
