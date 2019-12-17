# 영화정보 DB에 넣기 위한 코드
import os
import django
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SW2019test1_.settings')
django.setup()

from users.models import Movie

f = open('movie_df_drop1123.csv', 'r', encoding='utf-8')
info = []

rdr = csv.reader(f)
for row in rdr:
    #print(row)
    index, id, title, director, year, genre = row
    tuple = (int(id), title, director, year, genre)
    info.append(tuple)
f.close()
print(info)

instances = []
for (id, title, director, year, genre) in info:
    instances.append(Movie(id=id, title=title, director=director, year=year, genre=genre))
print(instances)

Movie.objects.bulk_create(instances)
