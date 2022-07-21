import requests
import os
import time


class MovieDescriptionMicroservice:
    def __init__(self):
        self.API_KEY = 'a7ef20454443b2f70d29336687a3d60a'

    def getMovieDescription(self, movie_title):
        # send request to the movie db searching for the movie
        r = requests.get(
            f'https://api.themoviedb.org/3/search/movie?api_key={self.API_KEY}&language=en-US&query={movie_title}&page=1&include_adult=false')

        # turn response into json/dictionary format
        json_data = r.json()

        # find description of the closest matching movie
        if 'results' in json_data:
            description = json_data['results'][0]['overview']
            return description

    def start(self):
        while True:
            time.sleep(3)

            # if file is empty continue on
            if os.path.getsize('movie-names.txt') == 0:
                continue

            # otherwise it has movie titles to be searched
            with open('movie-names.txt', 'r') as infile:
                movieTitles = ""
                for line in infile:
                    movieTitles = movieTitles + line

            # separate movie titles into an array without the commas
            movieTitles = movieTitles.split(",")
            descriptions = []

            # for each movie then call the getMovieDescription function
            for movie in movieTitles:
                descriptions.append(self.getMovieDescription(movie))

            # manipulate descriptions so there is a quote in the front and the end of the list for better writing
            descriptions[0] = '"' + descriptions[0]
            descriptions[-1] = descriptions[-1] + '"'
            # write the descriptions to the file separated by a comma
            with open('movie-descriptions.txt', 'w') as infile:
                # write each description into the file
                infile.write('","'.join(descriptions))

            # empty the movie-title txt file
            with open('movie-names.txt', 'w') as infile:
                continue


if __name__ == "__main__":
    descriptionGetter = MovieDescriptionMicroservice()
    descriptionGetter.start()
