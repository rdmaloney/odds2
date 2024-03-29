import requests
import pandas as pd
import numpy as np
import sqlite3
from bs4 import BeautifulSoup
import string
import re
import os
import time
from math import *

links = []
alphabets = sorted(set(string.ascii_lowercase))

f1 = []
f2 = []
f1_odds = []
f2_odds = []


def safe_eval(expr):
    try:
        return round(eval(expr), 2)
    except:
        return expr


def scrape_data():
    data = requests.get("https://www.paddypower.com/mixed-martial-arts")
    print(data.text)
    soup = BeautifulSoup(data.text, 'html.parser')
    divs = soup.findAll("div", {"class": "avb-item grid"})
    for div in divs:
        link = div.findAll('tr')[1]
        names = link.findAll('span')
        p1 = names[0].text
        p2 = names[1].text
        buttons_having_odds = div.findAll("div", {"class":"avb-item__box grid grid__cell-2-12"})
        button_odds = button_having_odds.findAll ('span')                                         
        p1_odds = button_odds[0]
        p2_odds = button_odds[1]
        f1.append(p1)
        f2.append(p2)
        f1_odds.append(p1_odds)
        f2_odds.append(p2_odds)

scrape_data()

def create_df():
    df = pd.DataFrame()
    df["Fighter1"] = f1
    df["Fighter1_Odds"] = f1_odds
    df["Fighter2"] = f2
    df["Fighter2_Odds"] = f2_odds

    return df


scrape_data()
df = create_df()

conn = sqlite3.connect('data.sqlite')
df.to_sql('data', conn, if_exists='replace')
print('Db successfully constructed and saved')
conn.close()
