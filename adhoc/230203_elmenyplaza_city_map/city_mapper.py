from bs4 import BeautifulSoup as bs
import requests
import pickle
from copy import deepcopy
import streamlit as st
import os
import dotenv
def get_path_filename(filename):
    return os.path.normpath(os.path.dirname(os.path.realpath(__file__))) + '/' + filename

def get_cities():
    if not full_ref:
        return pickle.load(open(get_path_filename('cities.p'), 'rb'))
    page = 1
    cities = []
    while page != 10:
        url = f"https://elmenyplaza.hu/elmeny-kategoriak/szallas-es-wellness?page={page}"
        response = requests.get(url)
        html = response.content
        soup = bs(html, "lxml")
        for city in soup.find_all("span", class_="city"):
          city_name = city.get_text(strip=True)
          print(city_name)
          cities.append(city_name)
        page = page + 1
    cities = set(cities)

    for city in deepcopy(cities):
        sub_cities = city.replace(" ", "").split(",")
        if isinstance(sub_cities, list) and len(sub_cities) > 1:
            cities.remove(city)
            for sub_city in sub_cities:
                cities.update([sub_city])
    pickle.dump(cities, open(get_path_filename('cities.p'), 'wb'))
    return cities


def get_pos(cities):
    if not full_ref:
        return pickle.load(open(get_path_filename('cords.p'), 'rb'))

    api_key = dotenv.dotenv_values('.env')['API_KEY']
    lats = []
    lons = []
    for city in cities:
        res = requests.get(f"http://api.positionstack.com/v1/forward?access_key={api_key}&query={city}&country=HU")
        positions = res.json()
        try:
            lats.append(positions['data'][0]['latitude'])
            lons.append(positions['data'][0]['longitude'])
        except IndexError:
            print(f'{city} not found')
            continue
    cords = {'lat': lats,
            'lon': lons}
    print(city,cords)
    pickle.dump(cords, open(get_path_filename('cords.p'), 'wb'))
    return cords

full_ref = False

if not os.path.exists(get_path_filename('cities.p'))\
or not os.path.exists(get_path_filename('cords.p')):
    full_ref = True


cities = get_cities()
cords = get_pos(cities)

st.map(data=cords, zoom=None, use_container_width=True)
