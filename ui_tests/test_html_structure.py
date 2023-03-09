import unittest
from bs4 import BeautifulSoup
from selenium import webdriver


class TestHTMLStructure(unittest.TestCase):

    def setUp(self):
        # Open the web browser and navigate to the app's URL
        self.browser = webdriver.Chrome()
        self.browser.get(
            'https://sea-lion-app-q6nwz.ondigitalocean.app/sample1')

    def tearDown(self):
        self.browser.quit()

    def test_html_structure(self):
        html_source = self.browser.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        self.assertEqual('My JavaScript Application', soup.title.string)

        input_field = soup.find('input', {'id': 'inputField'})
        self.assertIsNotNone(input_field)

        click_button = soup.find('button', string='Click me!')
        self.assertIsNotNone(click_button)

        clear_button = soup.find('button', string='Clear')
        self.assertIsNotNone(clear_button)


if __name__ == '__main__':
    unittest.main()
