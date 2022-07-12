import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from time import sleep


def extract(page):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",}
    url = f'https://www.longotoyota.com/searchused.aspx?Type=U&Make=Toyota&pt={page}'
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def transform(soup):
    website = 'https://www.longotoyota.com/'
    name = []
    body_style = []
    engine = []
    drive_type = []
    transmission = []
    external_color = []
    internal_color = []
    mileage = []
    price = []
        
    results = soup.find_all('div', class_ = 'row srpVehicle hasVehicleInfo')
    
    for result in results:        
        # name
        try:
            name.append(result.find('span', class_ = 'notranslate').get_text().strip())
        except:
            name.append('')
            
        # body style
        try:
            body_style.append(result.find('li', class_ = 'bodyStyleDisplay').get_text().split('Body Style: ')[-1])
        except:
            body_style.append('')
            
        # engine
        try:
            engine.append(result.find('li', class_ = 'engineDisplay').get_text().split('Engine: ')[-1])
        except:
            engine.append('')
            
        # drive type
        try:
            drive_type.append(result.find('li', class_ = 'driveTrainDisplay').get_text().split('Drive Type: ')[-1])    
        except:
            drive_type.append('')   
        
        # transmission
        try:
            transmission.append(result.find('li', class_ = 'transmissionDisplay').get_text().split('Transmission: ')[-1])    
        except:
            transmission.append('')  
        
        # external color
        try:
            external_color.append(result.find('li', class_ = 'extColor').get_text().split('Ext. Color: ')[-1])
        except:
            external_color.append('')
         
         # internal color
        try:
            internal_color.append(result.find('li', class_ = 'intColor').get_text().split('Int. Color: ')[-1])
        except:
            internal_color.append('')  
        
        # mileage
        try:
            mileage.append(result.find('li', class_ = 'mileageDisplay').get_text().split('Mileage: ')[-1])
        except:
            mileage.append('') 
        
        # price
        try:
            price.append(result.find('span', class_ = 'pull-right primaryPrice').get_text().strip('$'))
        except:
            price.append()
            
        car_info = {
            'Name': name,
            'Body Style':body_style,
            'Engine': engine,
            'Drive Type': drive_type,
            'Transmission': transmission,
            'Ext. Color': external_color,
            'Int. Color': internal_color,
            'Mileage (mi)': mileage,
            'Price ($)': price,
        }
              
    return car_info


list_of_df = []
for page in range(1, 23):
    print(f"Getting page, {page}")
    info = extract(page)
    info_df = pd.DataFrame(transform(info))
    list_of_df.append(info_df)
    sleep(0.1)

result_df = pd.concat(list_of_df, ignore_index=True)
result_df.to_csv('LongoToyotaDatabase.csv')


    