from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb+srv://user_2:Zwut9Ul2IlLG2noo@cluster0.37fbdrx.mongodb.net/")
db = client["Movies"]
movies_collection = db["Movies"]
user_collection = db["Users"]

class Movies:
    def __init__(self, imdb, name, price, status, overview, image) -> None:
        '''Inicializa la clase películas'''
        self.imdb = imdb
        self.name = name
        self.price = price
        self.status = status
        self.overview = overview
        self.image = image 

#    def createMovie(self):
#        movie_data = self.__dict__
#        return movies_collection.insert_one(movie_data).inserted_id
    
    def editMovie(movie_id, data):
        return movies_collection.update_one({"_id":ObjectId(movie_id)}, {"$set": data})
    
    def getMovie(self) -> list:
        '''Devuelve la lista de todas las películas'''
        movieList = []
        for movie in self.movies_collection.find():
            movieList.append(
                {
                    "id": str (movie['_id']),
                    "name":movie['name'],
                    "price":movie['price'],
                    "status":movie['status'],
                    "overview":movie['overview'],
                    "imdb" : movie['imdb'],
                    "image":movie['image']
                }
            )
        return movieList

    def getMovie_by_id(self, movie_id) -> dict:
        '''Regresa la película con el ID dado'''
        return movies_collection.find_one({"_id": ObjectId(movie_id)})

    def get_movies_by_title(self, title:str):
        return self.movies_collection.find('movies', {'name':name})

    def get_status(self, _id) -> None:
        movie = self.movies_collection.find_one({"_id": ObjectId(_id)})
        if movie:
            return movie.get('status')
        return None
    
    def isRented(self, _id) -> bool:
        '''Regresa true si una película esta rentada o false si no lo esta'''
        status = self.get_status(_id)
        return status is not None  and status

    def createMovie(self, imdb:str, name:str, price:float, status:bool, overview:str, image:str) -> str:
        '''Crea una pelicula'''
        new_movie ={
            "imdb": imdb,
            "name": name,
            "price": price,
            "status": status,
            "overview": overview,
            "image": image
        }
        result = movies_collection.insert_one(new_movie)
        return str(result.inserted_id) 

    def deleteMovie(self, _id) -> None:
        '''Elimina la película con el ID dado'''
        self.movies_collection.delete_one({"_id": ObjectId(_id)})



class User:
    def __init__(self, name, email, password) ->None:
        self.name = name
        self.email = email
        self.password = password

    def createUser(self):
        user_data = {"name": self.name, "email":self.email, "password": self.password, "type":"client"}
        return user_collection.insert_one(user_data).inserted_id
    
    def createAdmin():
        admin_data = {"name": self.name, "email":self.email, "password": self.password, "type":"admin"}
        return user_collection.insert_one(admin_data).inserted_id
    

class Client(User):
    def __init__(self, name, email, password, id, rented, balance, isEnabled) ->None:
        super().__init__(user.name, user.email, user.password)
        self.id = id
        self.rented = rented
        self.balance = balance
        self.isEnabled = isEnabled

    def rentMovie(self, movie_id):
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
    def __init__(self, name, email, password, users, movies_in_stock):
        super().__init__(self.name, self.email, self.password)
        self.users = users
        self.movies_in_stock = movies_in_stock
    
    def banUser():
        pass
    def freeUser():
        pass
# Crear una nueva película con imagen
#new_movie = Movies("tt789012", "Nueva Película", 12.99, False, "Una película emocionante", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/IMDB_Logo_2016.svg/1200px-IMDB_Logo_2016.svg.png")
#new_movie_id = new_movie.createMovie(new_movie.imdb, new_movie.name, new_movie.price, new_movie.status, new_movie.overview, new_movie.image)
#print(f"Nueva película creada con ID: {new_movie_id}")

# Crear un nuevo usuario
#new_user = User("Usuario1", "nuevo_usuario@example.com", "contraseña123")
#new_user_id = new_user.createUser()
#print(f"Nuevo usuario creado con ID: {new_user_id}")
##movie_instance = Movies()

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