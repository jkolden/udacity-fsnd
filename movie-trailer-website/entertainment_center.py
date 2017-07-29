from media import Movie
import fresh_tomatoes

bttf = Movie("Back to the future",
             "https://upload.wikimedia.org/wikipedia/en/d/d2/Back_to_the_Future.jpg",
             "https://www.youtube.com/watch?v=qvsgGtivCgs")

movies = [bttf]

fresh_tomatoes.open_movies_page(movies)
