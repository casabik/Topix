import pandas as pd
import chardet
import requests

with open('films.csv', 'rb') as f:
    encoding = chardet.detect(f.read())['encoding']
df = pd.read_csv('films.csv', sep=',', encoding=encoding)
print(df)