#!/usr/bin/env python
# coding: utf-8
import requests
from requests import get
from bs4 import BeautifulSoup
import json
import pandas as pd

url_256 = "https://gist.github.com/paulmillr/2657075"
response = get(url_256)
soup = BeautifulSoup(response.text, 'html.parser')
head = {'Authorization': 'token {}'.format('PUT_YOUR_TOKEN_HERE')}

def get_top_users(url):
    req = get(url)
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, "html.parser")
        table = soup.find("table").findAll("tr")[1:]
        return [row.find("td").text.split()[0] for row in table]
    else:
        print("Status Code Error")

def get_mean_stars_users(list_users):
    #Initialisation des variables
    dico_mean_stars = {}
    list_stars_mean = []

    dico_mean_stars["name"] = list_users

    for i in range(len(list_users)):
        sum_stars = 0
        mean_stars = 0
        page = "1"
        get_repo = requests.get("https://api.github.com/users/" + list_users[i] + "/repos?page=" + page + "&per_page=100", headers=head)
        get_json = json.loads(get_repo.content)
        for j in range(len(get_json)):
            sum_stars += get_json[j].get("stargazers_count")
        if len(get_json) != 0:
            mean_stars = sum_stars/len(get_json)
        else:
            mean_stars = 0
        list_stars_mean.append(mean_stars)
        dico_mean_stars["mean"] = list_stars_mean

    df_users_stars_mean = pd.DataFrame.from_dict(dico_mean_stars)
    return df_users_stars_mean


list_users = get_top_users(url_256)
df = get_mean_stars_users(list_users)
print(df)


