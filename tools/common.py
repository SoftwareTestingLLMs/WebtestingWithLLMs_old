from bs4 import BeautifulSoup, Comment
from urllib.parse import urlparse
import os


def clean_html(html):
    # Parse the HTML code with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # div_element = soup.find('div', {'class': 'col-sm-12 col-md-12 col-lg-7 col-xl-7'})

    # Remove comments
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Remove scripts
    for script in soup.findAll('script'):
        script.extract()

    # Remove meta tags
    for meta in soup.findAll('meta'):
        if 'X-UA-Compatible' in meta.get('http-equiv', '') or 'viewport' in meta.get('name', ''):
            meta.extract()

    # Remove non-UI elements
    for element in soup.select('body, [cbcookie], script, [nonce], [translations], link[rel="icon"]'):
        element.extract()


    # Return the cleaned HTML code
    return str(soup)


def generate_directory_path(url, base_dir):
    # Extract the directory name from the URL
    url_parts = urlparse(url)
    directory = url_parts.netloc + url_parts.path

    # Construct the full directory path
    return os.path.join(base_dir, directory.lstrip("/"))
