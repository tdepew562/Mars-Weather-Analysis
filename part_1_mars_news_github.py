#Part 1: Scrape Titles and Preview Text from Mars News

from splinter import Browser
from bs4 import BeautifulSoup as soup
import json
import os

# Initialize the browser (make sure the Chrome WebDriver is in your PATH)
browser = Browser('chrome')

# Visit the Mars news site
url = 'https://static.bc-edx.com/data/web/mars_news/index.html'
browser.visit(url)

# Get the HTML content of the website
html = browser.html

# Create a Beautiful Soup object
mars_news_soup = soup(html, 'html.parser')

# Initialize an empty list to store the scraping results
scraped_data = []

# Extract titles and preview text
articles = mars_news_soup.find_all('div', class_='list_text')
for article in articles:
    # Extract title
    title = article.find('div', class_='content_title').text.strip()
    
    # Extract preview text
    preview = article.find('div', class_='article_teaser_body').text.strip()
    
    # Create a dictionary to store title and preview text
    article_dict = {'title': title, 'preview': preview}
    
    # Append the dictionary to the list of scraping results
    scraped_data.append(article_dict)

# Print the list of scraping results
for article in scraped_data:
    print(article)

# Define the path to the resources folder
resources_folder = "resources"

# Create the resources folder if it doesn't exist
if not os.path.exists(resources_folder):
    os.makedirs(resources_folder)

# Define the path to the JSON file within the resources folder
output_file = os.path.join(resources_folder, "mars_news_data.json")

# Store the scraped data in the JSON file within the resources folder
with open(output_file, "w") as f:
    json.dump(scraped_data, f)

print(f"Scraped data has been stored in {output_file}")

# Quit the browser
browser.quit()