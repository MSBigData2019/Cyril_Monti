#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from requests import get
from bs4 import BeautifulSoup
import math
import pandas as pd


# In[ ]:


def get_url(url):
    url = url
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return(soup)


# In[ ]:


def get_links(soup):
    liste_annonce = []
    for annonce in soup.find_all('div', class_="adContainer"):
        for an in annonce.find_all('a'):
            liste_annonce.append(an['href'])
    return liste_annonce


# In[ ]:


def get_all_pages():
    soup = get_url("https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&regions=FR-PAC%2CFR-IDF%2CFR-NAQ")
    nb_annonce_total = int(soup.find('span', class_='numAnn').text.strip())
    nb_annonce_page = 16
    nb_page = math.ceil(nb_annonce_total / nb_annonce_page)
    liste = []
    for page in range(nb_page):
        soup = get_url("https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&options=&page={}&regions=FR-PAC%2CFR-IDF%2CFR-NAQ"
                       .format(page))
        lien = get_links(soup)
        liste.append(lien)
    return liste


# In[ ]:


def flatten(liens):
    liste_lien = []
    for tableau in liens:
        for lien in tableau:
            liste_lien.append(lien)
    return liste_lien


# In[ ]:


def remove_duplicates(l):
    return list(set(l))


# In[ ]:


def get_info(urls):
    modeles = []
    telephones = []
    annees = []
    kilometres = []
    vendeurs = []
    prices = []
    for url in urls:
        soup = get_url("https://www.lacentrale.fr{}".format(url))
        modele = soup.find('div', class_='versionTxt txtGrey7C sizeC mB10 hiddenPhone').text.strip()
        telephone = soup.find('div', class_='phoneNumber1').text.strip()
        annee = soup.find('span', class_='clearPhone lH35').text.strip()
        kilometre = soup.find('span', class_='clearPhone lH40').text.strip()
        vendeur = soup.find('div', class_='bold italic mB10').text[40:58].strip()
        prix = soup.find('strong', class_='sizeD lH35 inlineBlock vMiddle ').text.strip()
        modeles.append(modele)
        telephones.append(telephone)
        annees.append(annee)
        kilometres.append(kilometre)
        vendeurs.append(vendeur)
        prices.append(prix)
    dictionnaire = {"modeles":modeles,
                    "telephones": telephones,
                    "annee":annees,
                    "kilometres":kilometres,
                    "vendeurs":vendeurs,
                    "prix":prices}
    return dictionnaire


# In[ ]:


def get_liens_cote(soup):
    liste_cote = []
    for cote in soup.findAll('div', class_="listingResultLine"):
        for an in cote.findAll('a'):
            liste_cote.append(an['href'])
    return liste_cote


# In[ ]:


def get_all_cote():
    annees = list(range(2012, 2019))
    liens = []
    modeles = []
    prix = []
    annees2 = []
    annee_modele = []
    for annee in annees:
        soup = get_url("https://www.lacentrale.fr/cote-voitures-renault-zoe--{}-.html".format(annee))
        cote = get_liens_cote(soup)
        liens.append(cote)
    liens_f = flatten(liens)
    for lien in liens_f:
        url = "https://www.lacentrale.fr/{}".format(lien)
        soup = get_url(url)
        pri = soup.find('span', class_="jsRefinedQuot").text.strip()
        modele = soup.find('span', class_="sizeC clear txtGrey7C sizeC").text.strip()
        annee = lien[-9:-5]
        modeles.append(modele)
        prix.append(pri)
        annees2.append(annee)
    dictionnaire = {"modeles":modeles,
                    "cote": prix,
                    "annee" : annees2
                   }
    return dictionnaire


# In[ ]:


liens = get_all_pages()
lien_flattened = flatten(liens)
lien_f = remove_duplicates(lien_flattened)


# In[ ]:


informations = get_info(lien_f)
df1 = pd.DataFrame(informations)


# In[ ]:


cotes = get_all_cote()
df2 = pd.DataFrame(cotes)


# In[ ]:


df_final = pd.merge(df1, df2,  how='left', left_on=['modeles','annee'], right_on = ['modeles','annee'])
df_final.prix = df_final.prix.str.extract(r'(\d* \d\d\d)')
df_final.loc[df_final['prix'] > df_final['cote'], 'Good Deal'] = False
df_final.loc[df_final['prix'] < df_final['cote'], 'Good Deal'] = True


# In[ ]:


df_final


# In[ ]:




