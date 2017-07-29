import webbrowser


# A class describing movies class
# Compatible with "fresh_tomatoes" web page generator
class Movie():
    def __init__(self, title, poster_image_url, trailer_youtube_url):
        self.title = title
        self.poster_image_url = poster_image_url
        self.trailer_youtube_url = trailer_youtube_url

    # Open the youtube trailer url by the machine's default web browser
    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
