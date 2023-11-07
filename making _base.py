import pandas as pd
import chardet
import csv 
import requests

class CSV:
    def __init__(self):
        self.TOKEN = "1GW0Z48-1QQ48JG-GJ7AWHZ-7R1WY9T"
        with open('films.csv', 'rb') as f:
            encoding = chardet.detect(f.read())['encoding']
        self.df = pd.read_csv('films.csv', sep=';', encoding=encoding)

    def add_information(self):
        rus_name = []
        type = []
        country = []
        ages = []
        genres = []
        rating = []
        duration = []
        actors = []
        description = []
        url_picture = []
        url_trailer = []
        url_watch = []
        
        for i in range(self.df.shape[0]):
            film = self.df.iloc[i]['film']
            year = self.df.iloc[i]['year']
            print(film, year)
            text = film.encode('cp1251')
            language = chardet.detect(text)['language']
            if language == '':
                data = self.find_film(self.TOKEN, film, year)
            else:
                data = self.find_film(self.TOKEN, film, year, language)
            print(data['docs'][0]['name'])
            rus_name.append(data['docs'][0]['name'])
            type.append(data['docs'][0]['type'])
            country.append(data['docs'][0]['countries'][0]['name'])
            ages.append(data['docs'][0]['ageRating'])
            genres.append([])
            for j in data['docs'][0]['genres']:
                genres[i].append(j['name'])
            rating.append(data['docs'][0]['rating']['kp'])
            duration.append(data['docs'][0]['movieLength'])
            actors.append([])
            for j in data['docs'][0]['persons']:
                actors[i].append(j['name'])
            description.append(data['docs'][0]['shortDescription'])
            url_picture.append(data['docs'][0]['poster']['url'])
            if len(data['docs'][0]['videos']['trailers']) > 0:
                url_trailer.append(data['docs'][0]['videos']['trailers'][0]['url'])
            else:
                url_trailer.append(None)
            if data['docs'][0]['watchability']['items'] is not None:
                if len(data['docs'][0]['watchability']['items']) > 0:
                    url_watch.append(data['docs'][0]['watchability']['items'][-1]['url'])
                else:
                    url_watch.append(None)
            else:
                url_watch.append(None)

        self.df.insert(1, 'rus_name', rus_name, False)
        self.df['type'] = type
        self.df['rating'] = rating
        self.df['country'] = country
        self.df['duration'] = duration
        self.df['age'] = ages
        self.df['genres'] = genres
        self.df['actors'] = actors
        self.df['description'] = description
        self.df['url_picture'] = url_picture
        self.df['url_trailer'] = url_trailer
        self.df['url_watch'] = url_watch
        self.df.to_csv('films.csv', index=False)

    def getjson(self, url, data=None, headers=None):
        response = requests.get(url, params=data, headers=headers)
        response = response.json()
        return response


    def find_film(self, access_token, film, year, language='English', limit=1): 
        headers = {"X-API-KEY": access_token}
        
        fields = ['ageRating', 'name', 'type', 'countries', 'genres', 'rating', 'movieLength', 'persons', 'shortDescription', 'watchability', 'alternativeName', 'poster', 'videos', 'url']
        print(language)
        if language == 'English':
            responses = self.getjson("https://api.kinopoisk.dev/v1.3/movie", {'selectFields': fields, 'alternativeName': film, 'year' : year, 'limit': limit}, headers)
        else:
            responses = self.getjson("https://api.kinopoisk.dev/v1.3/movie", {'selectFields': fields, 'name': film, 'year' : year, 'limit': limit}, headers)
        return responses

download = CSV()
download.add_information()