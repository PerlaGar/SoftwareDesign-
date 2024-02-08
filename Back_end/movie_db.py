from pymongo import MongoClient
from bson import ObjectId, Decimal128
import json

# Initialize MongoDB client and collections
client = MongoClient("mongodb+srv://user_2:Zwut9Ul2IlLG2noo@cluster0.37fbdrx.mongodb.net/")
db = client["Movies"]
movies_collection = db["Movies"]
user_collection = db["Users"]

class Movie:
    def __init__(self, imdb: str, name: str, price: float, status: str, overview:str, image: str) -> None:
        '''Initialize movie class'''
        self.imdb = imdb
        self.name = name
        self.price = price
        self.status = status
        self.overview = overview
        self.image = image 

class Movies:
    @staticmethod
    def editMovie(movie_id, data):
        return movies_collection.update_one({"_id":ObjectId(movie_id)}, {"$set": data})
    
    @staticmethod
    def getMovie() -> list:
        '''Return the list of all movies'''
        movieList = []
        for movie in movies_collection.find():
            print(movie)
            movieList.append({
                "id": str(movie['_id']),
                "name": str(movie['name']),
                "price": float(str(movie['price'])),
                "status": bool(movie['status']),
                "overview": str(movie['overview']),
                "imdb": str(movie['imdb']),
                "image": str(movie['image'])
            })
        return movieList

    @staticmethod
    def getMovie_by_id(movie_id):
        '''Returns the movie with the given ID'''
        movie =  movies_collection.find_one({"_id": ObjectId(movie_id)})
        movie['_id'] =  str(movie['_id'])
        return movie
    
    @staticmethod
    def getMovie_by_name(movie_title):
        '''Returns the movie with the given name'''
        movie =  movies_collection.find_one({"name": str(movie_title)})
        movie['_id'] =  str(movie['_id'])
        return movie
        
    @staticmethod
    def createMovie(imdb:str, name:str, price:float, status:str, overview:str, image:str) -> str:
        '''Creates a movie'''
        new_movie = {
            "imdb": imdb,
            "name": name,
            "price": price,
            "status": status,
            "overview": overview,
            "image": image
        }
        result = movies_collection.insert_one(new_movie)
        res = Movies.getMovie_by_name(new_movie["name"])
        return str(res['_id'])

    @staticmethod
    def deleteMovie(_id) -> None:
        '''Deletes the movie with the given ID'''
        movies_collection.delete_one({"_id": ObjectId(_id)})

class User:

    def __init__(self, name, email, password) -> None:
        self.name = name
        self.email = email
        self.password = password
        self.status = True

    def createUser(self):
        user_data = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "type": "client",
            "status": self.status
        }
        return user_collection.insert_one(user_data).inserted_id
    
    def createAdmin(self):
        admin_data = {
                    "name": self.name, 
                    "email":self.email, 
                    "password": self.password, 
                    "type":"admin", 
                    "status": self.status}
        return user_collection.insert_one(admin_data).inserted_id
    
    def getUserByEmail(self, email:str):
        return user_collection.find_one({"email":email})
    

class Client(User):

    def rentMovie(self, movie_id):
        if self.status == False:
            return False

        movie = movies_collection.find_one({"_id":ObjectId(movie_id)})
        
        if movie is None:
            return False
        if movie.get('status') is True:
            return False, "Movie is already rented"
        
        result = movies_collection.update_one({"_id":ObjectId}, {"$set": {"staus": True}})
        
        if result.modified_count > 0:
            self.rented.append(movie_id)
            return True
        else:
            return False, "Failed to rent the movie"

    def returnMovie(self, movie_id):
        movie = movies_collection.find_one({"_id":ObjectId(movie_id)})

        if movie is None:
            return False
        if movie.get('status') is False:
            return False, "Movie is not rented"
        
        result = movies_collection.update_one({"_id":ObjectId(movie_id)}, {"$set":{"status":False}})
        if result.modified_count > 0:
            self.rented.remove(movie_id)
            return True
        else:
            return False, "Failed to return the movie"  

    def pay(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False, "Insufficient balance"

class Administrator(User):
    
    def banUser(self, email:Client):
        query = {"email": email.email}
        user_collection.update_one(query, {"$set":{"status":False}})
        email.status = False

    def freeUser(self, email:Client):
        query = {"email": email.email}
        user_collection.update_one(query, {"$set":{"status":True}})
        email.status = True

# Crear una nueva película con imagen
#new_movie = Movies("tt789012", "Nueva Película", 12.99, False, "Una película emocionante", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/IMDB_Logo_2016.svg/1200px-IMDB_Logo_2016.svg.png")
#new_movie_id = new_movie.createMovie(new_movie.imdb, new_movie.name, new_movie.price, new_movie.status, new_movie.overview, new_movie.image)
#print(f"Nueva película creada con ID: {new_movie_id}")

# Crear un nuevo usuario
#new_user = User("Usuario1", "nuevo_usuario@example.com", "contraseña123")
#new_user_id = new_user.createUser()
#print(f"Nuevo usuario creado con ID: {new_user_id}")
##movie_instance = Movies()

#new_user1 = Administrator("Uziel", "uziel.solis@iteso.mx", "1234")
#new_user2 = Client("Chava", "chava@iteso.mx", "4321")
#cliente1 = Client("Aldair", "aldair@iteso.mx", "2468")


#print(cliente1.status)
#new_user1.freeUser(cliente1.id)
#print(cliente1.status)
#new_user1.banUser(cliente1)
#print(cliente1.status)
#print(cliente1.rentMovie('65c025b74c719debcbd8132b'))
#new_user1.freeUser(cliente1)
#print(cliente1.rentMovie('65c025b74c719debcbd8132b'))

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