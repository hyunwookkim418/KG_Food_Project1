import os
from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time

post_urls = [
    "https://www.instagram.com/p/CMf-caUAQht/",
    "https://www.instagram.com/p/ClhLem0s01f/",
    "https://www.instagram.com/p/CpgInkDyUlj/",
    "https://www.instagram.com/p/CtKfI6mOsN0/",
    "https://www.instagram.com/p/CbqAcdSsdaN/",
    "https://www.instagram.com/p/CsC0YWKhDhv/",
    "https://www.instagram.com/p/CMSj-QLhd0R/",
    "https://www.instagram.com/p/Co_8qxeNBIB/",
    "https://www.instagram.com/p/ChZiarYM4Nj/",
    "https://www.instagram.com/p/CtvD_5YMRHu/"
]

# Create the directory for saving images if it doesn't exist
if not os.path.exists('.img'):
    os.makedirs('.img')

# Iterate over the post URLs
for post_url in post_urls:
    driver = webdriver.Chrome()
    driver.get(post_url)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    insta = soup.select('._aagv')
    
    n = 1
    for i in insta:
        profile_link = i.a['href'] if i.a else ''
        if profile_link.startswith('/'):
            profile_link = profile_link[1:]
        print('https://www.instagram.com/' + profile_link)

        imgurl = i.select_one('._aagv img')['src'] if i.select_one('._aagv img') else ''
        
        # Extract the post ID from the URL
        post_id = post_url.split('/')[-2]
        
        with urlopen(imgurl) as f:
            folder_name = post_id
            if not os.path.exists(f'.img/{folder_name}'):
                os.makedirs(f'.img/{folder_name}')
            
            with open(f'.img/{folder_name}/{folder_name}_{n}.jpg', 'wb') as h:
                img = f.read()
                h.write(img)
        
        n += 1
        print(imgurl)
        print()

    driver.close()
