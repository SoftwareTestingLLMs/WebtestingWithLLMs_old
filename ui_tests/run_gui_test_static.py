import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class TestWebApp(unittest.TestCase):

    def setUp(self):
        # Open the web browser and navigate to the app's URL
        self.browser = webdriver.Chrome()
        self.browser.get('https://sea-lion-app-q6nwz.ondigitalocean.app/sample1')

    def tearDown(self):
        # Close the web browser
        self.browser.quit()

    def test_input_field(self):
        # Find the input field and enter text into it
        input_field = self.browser.find_element(By.ID, 'inputField')
        input_field.send_keys('Hello, world!')

        # Find the "Click me!" button and click it
        click_button = self.browser.find_element(By.XPATH, '//button[string()="Click me!"]')
        click_button.click()

        # Wait for the alert to appear and get its text
        alert = WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        alert_text = alert.text

        # Check if the alert message is displayed with the correct text
        self.assertEqual('You typed: Hello, world!', alert_text)

        # Dismiss the alert
        alert.accept()

        # Find the "Clear" button and click it
        clear_button = self.browser.find_element(By.XPATH, '//button[string()="Clear"]')
        clear_button.click()

        # Check if the input field is cleared
        self.assertEqual('', input_field.get_attribute('value'))

    def test_html_structure(self):
        # Get the HTML source code of the page
        html_source = self.browser.page_source

        # Use BeautifulSoup to parse the HTML source code
        soup = BeautifulSoup(html_source, 'html.parser')

        # Check if the page title is correct
        self.assertEqual('My JavaScript Application', soup.title.string)

        # Check if the page contains an input field
        input_field = soup.find('input', {'id': 'inputField'})
        self.assertIsNotNone(input_field)

        # Check if the page contains a "Click me!" button
        click_button = soup.find('button', string='Click me!')
        self.assertIsNotNone(click_button)

        # Check if the page contains a "Clear" button
        clear_button = soup.find('button', string='Clear')
        self.assertIsNotNone(clear_button)

if __name__ == '__main__':
    unittest.main()
