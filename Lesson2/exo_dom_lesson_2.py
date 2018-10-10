#!/usr/bin/env python
# coding: utf-8

# WEB CRAWLING

# Le but de cet exercice est de crawler les données du site reuters pour plusieurs entreprises.

# On commence par importer les librairies nécessaires.

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from time import time
from time import sleep
from random import randint
from IPython.core.display import clear_output


url = 'https://www.reuters.com/finance/stocks/financial-highlights/'
pages = ['LVMH.PA', 'AIR.PA', 'DANO.PA']
prix = []
percentages = []
quarters_mean =[]
quarters_high =[]
quarters_low =[]
shares = []
dividends_company = []
dividends_industry = []
dividends_sector = []
headers = {"Accept-Language": "en-US, en;q=0.5"}

# Preparing the monitoring of the loop
start_time = time()
requests = 0


for page in pages:
    # Make a get request
    response = get(url + page , headers = headers)
    
    # Pause the loop
    sleep(randint(1,4))

    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)
        
    # Throw a warning for non-200 status codes
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    # Break the loop if the number of requests is greater than expected
    if requests > len(pages):
        warn('Number of requests was greater than expected.')  
        break 

    # Parse the content of the request with BeautifulSoup
    page_html = BeautifulSoup(response.text, 'html.parser')
        
    #Get the price 
    price_container = page_html.find_all('div', class_ = 'sectionQuoteDetail')
    first_price = price_container[0]
    span_container = first_price.find_all('span')
    prix_action = span_container[1].text.strip()
    prix.append(prix_action)
        
    # Get the percentage 
    percentage_container = page_html.find_all('span', class_ = 'valueContentPercent')
    percentage = percentage_container[0].text.strip()
    percentages.append(percentage)
        
    # Get the Quarter 
    quarter_container = page_html.find_all('td', class_ = 'data')
    quarter_mean = quarter_container[1].text
    quarter_high = quarter_container[2].text
    quarter_low = quarter_container[3].text
    quarters_mean.append(quarter_mean)
    quarters_high.append(quarter_high)
    quarters_low.append(quarter_low)
    
    # Get the Shares Owned
    shares_container = page_html.find_all('div', class_ = 'moduleBody')
    shares_IC = shares_container[13]
    share = shares_IC.find('td', class_ = 'data').text.strip()
    shares.append(share)
    
    # Get the dividend
    dividend_container = shares_container[4]
    dividend_container_2 = dividend_container.find_all('td', class_ = 'data')
    dividend_company = dividend_container_2[0].text
    dividend_industry = dividend_container_2[1].text
    dividend_sector = dividend_container_2[2].text
    dividends_company.append(dividend_company)
    dividends_industry.append(dividend_industry)
    dividends_sector.append(dividend_sector)


# On crée un dataframe avec les informations que nous avons récupérés et on affiche notre dataframe

import pandas as pd
company = ['LVMH', 'Airbus', 'Danone']
df = pd.DataFrame({'Company': company,
                   'Quarter mean': quarters_mean,
                   'Quarter high': quarters_high,
                    'Quarter low': quarters_low,
                    'Price': prix,
                    '% Change' : percentages,
                    '% Shares Owned' : shares,
                    'Dividend company' : dividends_company,
                    'Dividend industry' : dividends_industry,
                    'Dividend sector' : dividends_sector})


print(df)


# On peut voir que le résultat n'est pas ce à quoi on s'attendait. Il faut maintenant cleaner notre dataframe
#  pour ne plus voir les parentheses et les % dans les données.

df.loc[:, '% Change'] = df['% Change'].str.extract('(\W\d*.\d\d)', expand=True)
df.loc[:, '% Shares Owned'] = df['% Shares Owned'].str.extract('(\d*.\d.)', expand=True)
print(df)





