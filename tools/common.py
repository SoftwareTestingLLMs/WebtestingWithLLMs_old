from bs4 import BeautifulSoup, Comment
from urllib.parse import urlparse
import os


def clean_html(html):
    # Parse the HTML code with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # div_element = soup.find('div', {'class': 'col-sm-12 col-md-12 col-lg-7 col-xl-7'})

    # Remove scripts
    for script in soup.findAll('script'):
        script.extract()

    # Return the cleaned HTML code
    return str(soup)


def generate_directory_path(url, base_dir):
    # Extract the directory name from the URL
    url_parts = urlparse(url)
    directory = url_parts.netloc + url_parts.path

    # Construct the full directory path
    return os.path.join(base_dir, directory.lstrip("/"))
