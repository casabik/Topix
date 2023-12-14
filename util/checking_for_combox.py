import sqlite3

genre = dict()
duration = dict()
year = dict()
name = "film.sqlite"
con = sqlite3.connect(name)
cur = con.cursor()

genres = cur.execute(f"""SELECT genres FROM films""").fetchall()
genres = [item[0] for item in genres]
for i in genres:
    for j in i.split(', '):
        if j not in genre:
            genre[j] = 0
        genre[j] += 1
print(genre)
year['1970'] = 0
year['1980'] = 0
year['1990'] = 0
year['2000'] = 0
year['2010'] = 0
year['2020'] = 0
years = cur.execute(f"""SELECT year FROM films""").fetchall()
years = [item[0] for item in years]
for i in years:
    if i >= 1970 and i < 1980:
        year['1970'] += 1
    elif i >= 1980 and i < 1990:
        year['1980'] += 1
    elif i >= 1990 and i < 2000:
        year['1990'] += 1
    elif i >= 2000 and i < 2010:
        year['2000'] += 1
    elif i >= 2010 and i < 2020:
        year['2010'] += 1
    elif i >= 2020:
        year['2020'] += 1
print("genres")
for i in year.keys():
    print(i, year[i])

durations = cur.execute(f"""SELECT duration FROM films""").fetchall()
durations = [item[0] for item in durations]
duration["hour"] = 0
duration["2 hours"] = 0
duration["3 hours"] = 0
for i in durations:
    if len(i) < 2:
        continue
    if int(float(i)) >= 60 and int(float(i)) <= 120:
        duration["hour"] += 1
    elif int(float(i)) > 120 and int(float(i)) <= 180:
        duration["2 hours"] += 1
    elif int(float(i)) > 180 and int(float(i)) <= 240:
        duration["3 hours"] += 1
print("DURATIONS")
for i in duration.keys():
    print(i, duration[i])
country = dict()
countries = cur.execute(f"""SELECT country FROM films""").fetchall()
countries = [item[0] for item in countries]
for i in countries:
    if i not in country:
        country[i] = 0
    country[i] += 1
print("COUNTRIES")
print(country)
con.close()
