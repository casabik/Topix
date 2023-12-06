import requests
import sqlite3
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from PIL import Image


name = "film.sqlite"
con = sqlite3.connect(name)
cur = con.cursor()
names = cur.execute(f"""SELECT film FROM films""").fetchall()
pictures = cur.execute(f"""SELECT url_picture FROM films""").fetchall()
names = [item[0] for item in names]
pictures = [item[0] for item in pictures]
for i in range(len(pictures)):
    if pictures[i] is not None:
        p = requests.get(pictures[i])
        out = open(f"pictures_for_films/{names[i]}.jpg", "wb")
        out.write(p.content)
        width = 330
        img = Image.open(f"pictures_for_films/{names[i]}.jpg")
        width_percent = (width / float(img.size[0]))
        height = int((float(img.size[1]) * float(width_percent)))
        img = img.resize((width, height))
        img.save(f"pictures_for_films/{names[i]}.jpg")
        out.close()
con.close()