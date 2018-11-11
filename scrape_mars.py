from bs4 import BeautifulSoup as bs
import pandas as pd
import pymongo
from pprint import pprint
import requests
from splinter import Browser
import lxml


def scrape():

    mars_all = {}

    #MARS NEWS
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #Prepare empty list for headlines and paragraphs
    news_info=[]

    html = browser.html
    soup = bs(html, 'lxml')
    news_title = soup.find("div", class_='content_title').find('a').text
    news_paragraph = soup.find("div", class_='article_teaser_body').text

    news_info.append({"Headline": news_title,
                    "Paragraph": news_paragraph})

    mars_all['news_title'] = news_title
    mars_all['news_paragraph'] = news_paragraph


    #MARS IMAGE
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')

    #Define the base image URL of high-res image
    base_imgurl = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/'

    #Locate the image, strip into components, and get only the 8-digit image name
    image_name = soup.find('div', class_='img').find('img')['src']
    image_name = image_name.split("/")[-1:][0][0:8]

    #Concatenate the image URL components
    featured_image_url = base_imgurl + image_name + '_hires.jpg'

    mars_all['featured_image_url'] = featured_image_url 

    #MARS TWEET
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')

    mars_weather = soup.find('div', class_='js-tweet-text-container').find('p').text

    mars_all['mars_weather'] = mars_weather

    #MARS FACTS
    url = 'http://space-facts.com/mars/'
    tables = pd.read_html(url)

    #Specify column titles for fact table
    mars_facts = tables[0]
    mars_facts.columns = ['Statistic', 'Detail']

    #Convert DataFrame to HTML
    mars_facts = mars_facts.to_html()

    mars_all['mars_facts'] = mars_facts

    #MARS HEMISPHERES
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)

    #Prepare empty list to store dictionary of image links and titles
    mars_hemispheres = []

    #Loop through 4 hemispheres
    for i in range(4):

        browser.find_by_css("a.product-item h3")[i].click()

        #Get the current HTML page structure
        html = browser.html
        soup = bs(html, 'lxml')
        
        #Identified from the enhanced image, this is the base URL...
        base_url = 'https://astrogeology.usgs.gov'

        #Each hemisphere image location found here...store it in a variable
        hemisphere_image = soup.find_all('img', class_='wide-image')[0]['src']
        image_link = base_url + hemisphere_image
        
        #Store the title in a variable...need to remove ' Enhanced'
        hemisphere_title = soup.find('h2', class_='title').text.replace(' Enhanced', '')
        
        #Append image and title to a dictionary and append to list
        mars_hemispheres.append({'Hemisphere': hemisphere_title,
                                'ImageURL': image_link})
        
        mars_all['hemispheres'] = mars_hemispheres
        
        #Back to previous page to loop through other hemispheres.
        browser.click_link_by_text('Back')

    return(mars_all)