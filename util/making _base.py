import pandas as pd
import sqlite3
import chardet
import csv 
import requests
from configuration.config import *

class Make_base:
    def __init__(self):
        self.TOKEN = token
        with open('newfilm.csv', 'rb') as f:
            encoding = chardet.detect(f.read())['encoding']
        self.df = pd.read_csv('newfilm.csv', delimiter=';', encoding=encoding)

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
            film = self.df.iloc[i]['Film']
            year = self.df.iloc[i]['Year']
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
            age = data['docs'][0]['ageRating']
            if age != None:
                age = str(int(age)) + '+'
            ages.append(age)
            genre = []
            for j in data['docs'][0]['genres']:
                if j['name'] != None:
                    genre.append(j['name'])
            genre = ', '.join(genre)
            genres.append(genre)
            rating.append(data['docs'][0]['rating']['kp'])
            duration.append(data['docs'][0]['movieLength'])
            actor = []
            for j in data['docs'][0]['persons']:
                if j['name'] != None:
                    actor.append(j['name'])
            print(actor)
            actor = ', '.join(actor)
            actors.append(actor)
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
        self.df.to_csv('film.csv', sep=';', index=False)

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
    
    def tables(self):
        with sqlite3.connect('film.sqlite') as db:
            cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS films (film TEXT, rus_name TEXT, year INTEGER, type TEXT, country TEXT, age TEXT, genres TEXT, rating TEXT, duration TEXT, actors TEXT, description TEXT, url_picture TEXT, url_trailer TEXT, url_watch TEXT) """ 
            cursor.execute(query)
        db.close()
    
    def info_for_tables(self):
        con = sqlite3.connect('film.sqlite')
        cur = con.cursor()
        with open('film.csv', 'rb') as f:
            encoding = chardet.detect(f.read())['encoding']
        with open('film.csv','rt', encoding=encoding) as fin:
            dr = csv.DictReader(fin, delimiter=';')
            to_db = [(i['Film'], i['rus_name'], i['Year'], i['type'], i['country'], i['age'], i['genres'], i['rating'], i['duration'], i['actors'], i['description'], i['url_picture'], i['url_trailer'], i['url_watch']) for i in dr]
        cur.executemany("INSERT INTO films (film, rus_name, year, type, country, age, genres, rating, duration, actors, description, url_picture, url_trailer, url_watch) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
        con.commit()
        con.close()

download = Make_base()
download.add_information()
download.tables()
download.info_for_tables()