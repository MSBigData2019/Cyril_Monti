from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import json

def get_url(url):
    url = url
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return(soup)

def get_ville(soup):
    tableau = soup.find('tbody')
    villes = tableau.findAll('tr')
    i = 1
    liste_ville = []
    while i < 50:
        ville = villes[i].find('a').text
        liste_ville.append(ville)
        i += 1
    return liste_ville

soup = get_url("https://fr.wikipedia.org/wikiListe_des_communes_de_France_les_plus_peupl%C3%A9es")
villes = get_ville(soup)
villes_1 = villes[:4]

KEY = open("key_api_google.txt",'r').read()

villes_concat = "|".join(villes_1)
api_prefix = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metrics"
api_address = f"{api_prefix}&origins={villes_concat}&destinations={villes_concat}&key={KEY}"
response = get(api_address).json()
distances = list(map(lambda x : list(map(lambda y : y['distance']['text'], x['elements'])), response['rows']))

df = pd.DataFrame(distance, index=villes, columns=villes)

