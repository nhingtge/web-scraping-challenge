from bs4 import BeautifulSoup
from splinter import Browser
import time
import pandas as pd
import pymongo
import requestd


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # article
    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find('div', class_='article_teaser_body').text

    # image url
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(1)
    browser.links.find_by_partial_text('more info').click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    feat_img_url = soup.find('figure', class_='lede').a['href']
    feat_image_url = f'https://www.jpl.nasa.gov{feat_img_url}'

    # facts string
    facts_url = 'https://space-facts.com/mars/'

    facts = pd.read_html(facts_url)[0]
    facts_string = facts.to_html()

    # hemisphere images
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)

    hemi_image_urls = []

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find('div', class_='result-list')
    hemispheres = results.find_all('div', class_='item')

    for hemisphere in hemispheres:
        title = hemisphere.find('h3').text
    
        partial_link = hemisphere.find('a')['href']
        image_link = 'https://astrogeology.usgs.gov/' + partial_link    
    
        browser.visit(image_link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        image = soup.find('div', class_='downloads')
        image_url = image.find('a')['href']
    
        hemi_image_urls.append({'title': title, 'img_url': image_url})

    # store in dictionary
    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'feat_image_url': feat_image_url,
        'facts_string': facts_string,
        'hemi_image_urls': hemi_image_urls
    }

    browser.quit()
    return mars_data