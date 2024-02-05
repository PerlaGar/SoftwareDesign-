from flask import Flask, jsonify, request
from movie_db import Movies
from bson import ObjectId

app = Flask(__name__)

movies_r = Movies()

@app.route('/movies', methods=['GET'])
def getMovie():
    movieList = movies_r.getMovie()
    return jsonify ({'movies': movieList})

@app.route('/<string:_id>', methods=['GET'])
def getMovie_by_id(_id: str):
    movie = movies_r.getMovie_by_id(id)
    if movie is None:
        return jsonify({'message': 'No se encontró la película'}), 400
    else: 
        return jsonify(movie), 200


@app.route('/create', methods=['POST'])
def create_Movie():
    movie = {
        "name": request.json['name'],
        "price": request.json['price'],
        "status": request.json['status'],
        "overview": request.json['overview'],
        "image": request.json['image']
    }

    movies_r.collection.insert_one(movie)
    return jsonify({'message': 'Producto creado correctamente'}), 201


@app.route('/<string:_id>', methods = ['PUT'])
def editMovie(_id: str):
    new_movie = movies_r.getMovie_by_id(id)
    if new_movie is None:
        return jsonify({'message': 'No se encontró la película a editar'}), 400
    else:
        if "name" in request.json:
            new_movie["name"] = request.json["name"]
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
    movie = movies_r.getMovie_by_id(id)
    if movie is None:
        return jsonify({'message': 'Película no encontrada'}), 404
    else:
        movies_r.deleteMovie(id)
        return jsonify({'message': 'Película eliminada corectamente'}), 200

if __name__ == '__main__':
    app.run(debug=True)
