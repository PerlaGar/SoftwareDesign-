from pymongo import MongoClient
from bson import ObjectId

class Movies():

    def __init__(self) -> None:
        '''Inicializa la conexión con la base de datos'''
        self.client = MongoClient("mongodb+srv://user_2:Zwut9Ul2IlLG2noo@cluster0.37fbdrx.mongodb.net/")
        self.db = self.client["Movies"]
        self.collection = self.db["Movies"]

    
    def getMovie(self) -> list:
        '''Devuelve la lista de todas las películas'''
        movieList = []
        for movie in self.collection.find():
            movieList.append(
                {
                    "id": str (movie['_id']),
                    "name":movie['name'],
                    "price":movie['price'],
                    "status":movie['status'],
                    "overview":movie['overview'],
                    "image":movie['image']
                }
            )
        return movieList

    def getMovie_by_id(self, _id) -> dict:
        '''Regresa la película con el ID dado'''
        search = self.collection.find_one({"_id": ObjectId(_id)})
        if search is None:
            return None

        movie = {
            "id":search['_id'],
            "name":search['name'],
            "price":search['price'],
            "status":search['status'],
            "overview":search['overview'],
            "image": search['image']
        }
        return movie

    def get_status(self, _id) -> None:
        movie = self.collection.find_one({"_id": ObjectId(_id)})
        if movie:
            return movie.get('status')
        return None
    
    def isRented(self, _id) -> bool:
        '''Regresa true si una película esta rentada o false si no lo esta'''
        status = self.get_status(_id)
        return status is not None  and status

    def createMovie(self, name, price, status, overview, image) -> str:
        '''Crea una pelicula'''
        new_movie ={
            "name": name,
            "price": price,
            "status": status,
            "overview": overview,
            "image": image
        }
        result = self.collection.insert_one(new_movie)
        return str(result.inserted_id) 

    #def editMovie(_id):



    def deleteMovie(self, _id) -> None:
        '''Elimina la película con el ID dado'''
        self.collection.delete_one({"_id": ObjectId(_id)})


#movie_instance = Movies()

#new_movie_id = movie_instance.createMovie("The Dark Knight:",100, True, "Batman se enfrenta al Joker en una batalla épica por la justicia en Gotham City.", "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg")
#print(f"New movie created with ID: {new_movie_id}")

#movies_list = movie_instance.getMovie()
#movi_id_check = '65bef950b34728516d395888'
#rented_status = movie_instance.isRented(movi_id_check)
#movie_delete = '65c003967df8b2462cc4094f'
#movie_instance.deleteMovie(movie_delete)

#mov = movie_instance.getMovie_by_id(movi_id_check)
#print(mov)

#if rented_status:
#    print("The movie is rented.")
#else:
#    print("Movie not found or not rented.")

#for movie in movies_list:
#    print(movie)

