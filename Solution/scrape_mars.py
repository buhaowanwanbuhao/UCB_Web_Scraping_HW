# return one library to collect all scrape data
# modules
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time


# Defining function to scrape data
def get_scraped_data():
    # Creating a library that holds all the Mars' Data
    library = {}
    # Use splinter to navigate the JPL's Featured Space Image and scrape the current Featured Mars Image url (https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
    # Executing Chromedriver
    path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **path, headless=False)
    
    # scraping latest News and Paragragh from NASA Mars News Site(https://mars.nasa.gov/news/).
    # scraped page url
    url_one = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    #Visiting the page
    browser.visit(url_one)
    # assigning html data
    html = browser.html
    # Creating a Beautiful Soup object
    soup_one = bs(html, "html5lib")
    # Extracting text from class="content_title" and clean up the text use strip
    title_of_news = soup_one.find_all('div', class_='content_title')[0].find('a').text.strip()
    # Extracting paragraph from the class="rollover_description_inner" and clean up the text use strip
    news_para = soup_one.find_all('div', class_='rollover_description_inner')[0].text.strip()
    # adding data into Library
    library['news_title'] = title_of_news
    library['news_p'] = news_para


    
    # scraped page url
    url_two = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #Visiting the page
    browser.visit(url_two)
    # assigning html data
    html = browser.html
    # Creating a Beautiful Soup object
    soup_two = bs(html, "html5lib")
    #incomplete path of the url
    incomplete_address = soup_two.find_all('a', class_='fancybox')[0].get('data-fancybox-href').strip()
    #full address
    image_url = "https://www.jpl.nasa.gov" + incomplete_address
    # adding data into Library
    library['featured_image_url'] = image_url


    
    # Use splinter to scrape the latest Mars weather tweet from the Mars Weather twitter account  (https://twitter.com/marswxreport?lang=en)
    # URL of page to be scraped
    url_three = 'https://twitter.com/marswxreport?lang=en'
    #Visiting page
    browser.visit(url_three)
    # assigning html data
    html = browser.html
    # Creating a Beautiful Soup object
    soup_three = bs(html, "html5lib")
    #latest Mars weather tweet
    weather = soup_three.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text
    # Put infos into Library
    library['mars_weather'] = weather


    
    # Use Pandas to scrape the table from Mars Facts webpage and convert the data to a HTML table string
    # scraped page url
    url_four = 'https://space-facts.com/mars/'
    # getting the url table
    table = pd.read_html(url_four)
    # Converting list into dataframe
    dataframe = table[0]
    # modifying column name
    dataframe.columns=['description','value']
    #Setting index to column, description
    dataframe.set_index('description', inplace=True)
    # saving dataframe as html file
    facts=dataframe.to_html(justify='left')
    # adding data into Library
    library['mars_facts'] = facts


    # scraped page url
    url_five = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #Visiting page
    browser.visit(url_five)
    # assigning html data
    html = browser.html
    # Creating a Beautiful Soup object
    soup_five = bs(html,"html5lib")
    # list to store:
    images_of_hemisphere = []
    # creating empty dictionary
    dictionary = {}
    # getting all the titles
    findings = soup_five.find_all('h3')
    # Loop through each finding
    for finding in findings:
        # Get text info from finding
        item_alpha = finding.text
        time.sleep(1)    
        browser.click_link_by_partial_text(item_alpha)
        time.sleep(1)
        # assigning html data
        html_alpha = browser.html
        # Creating a Beautiful Soup object
        soup_alpha = bs(html_alpha,"html5lib")
        time.sleep(1)
        # image link
        link_alpha = soup_alpha.find_all('div', class_="downloads")[0].find_all('a')[0].get("href")
            # Pass title to dictionary
        time.sleep(1)
        dictionary["title"]=item_alpha
        # Pass url to dictionary
        dictionary["img_url"]=link_alpha
        # Append dictionary to the list
        images_of_hemisphere.append(dictionary)
        # Cleaning up dictionary
        dictionary = {}
        browser.click_link_by_partial_text('Back')
        time.sleep(1)
    # adding data into Library
    library['hemisphere_image_urls']=images_of_hemisphere
    
    # Return Library
    return library

