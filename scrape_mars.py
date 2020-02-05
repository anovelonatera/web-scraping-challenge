# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pymongo

import time
import pandas as pd


def init_browser():
    # Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():   
    # Dictionary to return
    mars_data = { }
    
    browser = init_browser()
    # Links to scrape
    nasa_mars = 'https://mars.nasa.gov/news'
    jpl_mars_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    mars_fact_url = 'https://space-facts.com/mars/'
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_usgs_link='https://astrogeology.usgs.gov'


    # ** 1. ** Visit NASA Mars news page. Latest News: Title and Paragaph ----------------------------------------
    browser.visit(nasa_mars)
    # Create BS4 Object
    html = browser.html
    soup = bs(html, 'html.parser')

    slides = soup.find('li', class_='slide')
    # GET latest news title.
    nasa_title = slides.find('div', class_='content_title')
    latest_title = nasa_title.text
    # GET latest news paragraph
    description = slides.find('div', class_='rollover_description_inner')
    latest_description = description.text

    #print(latest_title)
    #print(latest_description)
    # =====================================================================================================


    # ** 2. ** Visit Mars Space Images page. Title and Paragaph intro ----------------------------------------
    browser.visit(jpl_mars_image)
    base_jpl_url = 'https://www.jpl.nasa.gov'
    # Create BS4 Object
    html = browser.html
    soup = bs(html, 'html.parser')

    url = soup.find('div', class_='carousel_container')
    featured_image_url = url.find('a')['data-fancybox-href']
    featured_image_url = base_jpl_url + featured_image_url
    #print (featured_image_url)
    # =====================================================================================================


    # ** 3. ** Visit Mars Weather Twiter account. Latest weather Tweet ----------------------------------------
    browser.visit(mars_weather_url)
    # Create BS4 Object
    html = browser.html
    soup = bs(html, 'html.parser')
    
    # GET latest Tweet
    tweet_container = soup.find('div', class_='js-tweet-text-container')
    tweet_container_text = tweet_container.p.text.strip()
    latest_tweet = tweet_container_text.replace(tweet_container.a.text,'')
    latest_tweet = latest_tweet.replace('\n',' ').encode('utf-8').strip()
    #print (latest_tweet)
    # =====================================================================================================

    # 4. Visit Mars Facts page. Table of characteristics -------------------------------------------------
    browser.visit(mars_fact_url)
    # Create BS4 Object
    html = browser.html
    soup = bs(html, 'html.parser')

    table = soup.find_all('tr')
    # Get the elements of the Website Table in 2 lists
    mars_facts = []
    mars_facts_values = []
    for row in table:
        fact_name = row.find('td', class_='column-1').text.strip()
        fact_value = row.find('td', class_='column-2').text.strip()

        mars_facts.append(fact_name)
        mars_facts_values.append(fact_value)
    
    # Create Mars Facts DataFrame
    data = {'Description':mars_facts, 'Value':mars_facts_values}
    mars_facts_df = pd.DataFrame(data)
    # Set index to Description
    mars_facts_df = mars_facts_df.set_index('Description')

    # To HTML
    html_facts = mars_facts_df.to_html()




    # 5. Visit Mars Hemispheres page. High Resolution Images: Title & URL -------------------------------------------------
    browser.visit(mars_hemispheres_url)
    # Parse HTML
    html = browser.html
    soup = bs(html, 'html.parser')

    hem_links = soup.find_all('div', class_='item')

    # List to save the image data.
    hemisphere_image_urls = []

    for link in hem_links:
        title = link.find('h3').text
        # Get the link to the hemisphere
        hemisphere_url = link.find('a')['href']
        #print(title)
        key_word = title.split(' ')
    
        try:
        
            browser.click_link_by_partial_text(key_word[0])
        
            # Reload html and soup for the new window
            html = browser.html
            soup = bs(html, 'html.parser')
        
            # Extract the image URL
            image = soup.find('div', class_='downloads')        
        
            image_url = image.find('a')['href']
        
            # Save data to a Dictionary
            hemispheres_dict = {
                'Title':title,
                'Img_URL':image_url
            } 
            # Append new dictionary to list
            hemisphere_image_urls.append(hemispheres_dict)
        
        except:
            print('Cant click')
    # =====================================================================================================
    
    #print (hemisphere_image_urls)


    mars_data['Latest_News'] = latest_title
    mars_data['Description'] = latest_description
    mars_data['Featured_Image'] = featured_image_url
    mars_data['Latest_Tweet'] = latest_tweet
    mars_data['Facts_Table'] = html_facts
    mars_data['Hemispheres'] = hemisphere_image_urls


    #mars_data = {
    #    'Latest_News':latest_title,
    #    'Description':latest_description,
    #    'Featured_Image':featured_image_url,
    #    'Latest_Tweet':latest_tweet,
        # Table,
    #    'Hemispheres':hemisphere_image_urls
    #}
    
    # Close-End Browser
    browser.quit()
    
    return mars_data

# Init browser and call scrape.
#browser = init_browser()
#scrape(browser)