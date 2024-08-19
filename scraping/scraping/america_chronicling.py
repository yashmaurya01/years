import json

import requests


def get_chronicling_america_data():
    with open('data/ocr.json', 'r') as file:
        data = file.read()
        return json.loads(data)

info = get_chronicling_america_data()
urls = []

for i in info["ocr"]:

    print(i)
    break

