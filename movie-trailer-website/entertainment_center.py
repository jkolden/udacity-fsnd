from media import Movie
import fresh_tomatoes

# Instantiate Movie class representing my favorite movies
# Every poster image comes from Wikimedia
# Every trailer movie comes from Youtube
bttf = Movie("Back To The Future",
             "https://upload.wikimedia.org/wikipedia/en/d/d2/Back_to_the_Future.jpg",
             "https://www.youtube.com/watch?v=qvsgGtivCgs")

matrix = Movie("The Matrix",
               "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg",
               "https://www.youtube.com/watch?v=m8e-FF8MsqU")

terminator2 = Movie("Terminator 2",
                    "https://upload.wikimedia.org/wikipedia/en/8/85/Terminator2poster.jpg",
                    "https://www.youtube.com/watch?v=7QXDPzx71jQ")

sw_ep1 = Movie("Star Wars: Episode I",
               "https://upload.wikimedia.org/wikipedia/en/4/40/Star_Wars_Phantom_Menace_poster.jpg",
               "https://www.youtube.com/watch?v=bD7bpG-zDJQ")

pacific_rim = Movie("Pacific Rim",
                    "https://upload.wikimedia.org/wikipedia/en/f/f3/Pacific_Rim_FilmPoster.jpeg",
                    "https://www.youtube.com/watch?v=5guMumPFBag")

inception = Movie("Inception",
                  "https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg",
                  "https://www.youtube.com/watch?v=8hP9D6kZseM")

# Bundle all movie instances into a list
movies = [bttf, matrix, terminator2, sw_ep1, pacific_rim, inception]

# Generate a web page displaying movies
fresh_tomatoes.open_movies_page(movies)
