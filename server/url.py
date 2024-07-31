import requests
from bs4 import BeautifulSoup

# Specify the URL
url = 'https://legacy.reactjs.org/docs/faq-structure.html'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Get the HTML content from the response
    html_content = response.text

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Print the HTML code
    print(soup.prettify())
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
