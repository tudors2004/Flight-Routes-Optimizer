import pandas as pd
from bs4 import BeautifulSoup
import requests

response = requests.get("https://en.wikipedia.org/wiki/List_of_international_airports_by_country")
soup = BeautifulSoup(response.text, 'html.parser')
h = soup.find_all("h4") # the headers which contain the country names
t = soup.find_all("table", class_="wikitable") # the tables that contain the city, airport name and IATA code
airports=[]
for header,table in zip(h,t):
    country = header.text.strip() # remove whitespace
    df=pd.read_html(str(table))[0] # convert the table to pandas df
    df = df.iloc[:, :3] # keep only the first 3 columns
    df.columns = ["Airport Name", "City", "IATA Code"]
    df["Country"] = country
    airports.append(df)
df_airports = pd.concat(airports, ignore_index=True) # concatenate all the df
df_airports.to_csv("static/airports.csv", index=False)