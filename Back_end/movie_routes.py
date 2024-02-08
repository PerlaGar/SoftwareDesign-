from flask import Flask, session, jsonify, request
from movie_db import Movies
from bson import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

movies_r = Movies()
client = MongoClient("mongodb+srv://user_2:Zwut9Ul2IlLG2noo@cluster0.37fbdrx.mongodb.net/")
db = client["Movies"]
movies_collection = db["Movies"]
user_collection = db["Users"]

@app.route('/movies', methods=['GET'])
def getMovie():
    movieList = movies_r.getMovie()
    return jsonify ({'movies': movieList})

@app.route('/<string:_id>', methods=['GET'])
def getMovie_by_id(_id: str):
    movie = movies_r.getMovie_by_id(_id)
    if movie is None:
        return jsonify({'message': 'No se encontró la película'}), 400
    else: 
        return jsonify(movie), 200


@app.route('/create', methods=['POST'])
def create_Movie():
    movie = {
        "name": request.json['name'],
        "imdb": request.json['imdb'],
        "price": request.json['price'],
        "status": request.json['status'],
        "overview": request.json['overview'],
        "image": request.json['image']
    }

    movies_r.collection.insert_one(movie)
    return jsonify({'message': 'Producto creado correctamente'}), 201


@app.route('/<string:_id>', methods = ['PUT'])
def editMovie(_id: str):
    new_movie = movies_r.getMovie_by_id(_id)
    if new_movie is None:
        return jsonify({'message': 'No se encontró la película a editar'}), 400
    else:
        if "name" in request.json:
            new_movie["name"] = request.json["name"]
        if "imdb" in request.json:
            new_movie["imdb"] = request.json["imdb"]
        if "price" in request.json:
            new_movie["price"] = request.json["price"]
        if "status" in request.json:
            new_movie["status"] = request.json["status"]
        if "overview" in request.json:
            new_movie["overview"] = request.json["overview"]

        movies_r.collection.update_one({'id':_id}, {'$set': new_movie})
        return jsonify({'message': 'Película actualizada corectamente'}), 200

@app.route('/<string:_id>', methods=['DELETE'])
def deleteMovie(_id: str):
    movie = movies_r.getMovie_by_id(_id)
    if movie is None:
        return jsonify({'message': 'Película no encontrada'}), 404
    else:
        movies_r.deleteMovie(_id)
        return jsonify({'message': 'Película eliminada corectamente'}), 200
    
# Ruta para el login
@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    user = user_collection.find_one({"email": email, "password": password})
    if user:
        session['user_id'] = str(user['_id'])
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401
    
@app.route('/<string:email>', methods=['GET'])
def getClient_by_email(email: str):
    client = user_collection.find_one({"email":email})
    if client is None:
        return jsonify({'message': 'No se encontró la película'}), 400
    else: 
        return jsonify(client), 200

# Verificar si el usuario está logueado antes de ejecutar las rutas de películas
@app.before_request
def before_request():
    if request.endpoint != 'login' and 'user_id' not in session:
        return jsonify({'message': 'Unauthorized access'}), 401

if __name__ == '__main__':
    app.run(debug=True)
