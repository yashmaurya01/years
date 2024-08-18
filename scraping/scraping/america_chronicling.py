import requests


def get_chronicling_america_data():
    url = 'https://chroniclingamerica.loc.gov/ocr.json'
    response = requests.get(url)
    return response.json()


info = get_chronicling_america_data()
