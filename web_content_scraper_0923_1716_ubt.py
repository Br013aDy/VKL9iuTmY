# 代码生成时间: 2025-09-23 17:16:19
from celery import Celery
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Celery configuration
app = Celery('web_content_scraper', broker='pyamqp://guest@localhost//')

# Task to fetch web content
@app.task
def fetch_web_content(url):
    """Fetches and parses the content of a webpage.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        dict: A dictionary containing the title and links found on the webpage.
    """
    try:
        # Send HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        # Handle any errors that occur during the HTTP request
        return {'error': str(e)}
    else:
        # Parse the content of the webpage using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No title found'
        links = [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True) if urlparse(urljoin(url, link.get('href'))).netloc == urlparse(url).netloc]  # Filter out external links
        return {'title': title, 'links': links}

# Example usage
if __name__ == '__main__':
    # Define the URL of the webpage to scrape
    url_to_scrape = 'http://example.com'
    # Call the task to fetch the web content
    result = fetch_web_content.delay(url_to_scrape)
    # Wait for the task to finish and print the result
    print(result.get())
