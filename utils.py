import requests
import random


def getter():
    response = requests.get('https://jsonplaceholder.typicode.com/photos')
    obj = response.json()
    return random.choice(obj)


def get_nationalize(name):
    response = requests.get('https://api.nationalize.io/?name={0}'.format(name))
    text = response.json()
    name = text['name']
    countries = ""
    for country in text['country']:
        countries += "страна="+country['country_id'] + "%=" + str(country['probability']) + "\n"
    otvet = ("Имя: {name}\n"
            "Список государств: {countries}").format(name=name, countries=countries)
    return otvet

