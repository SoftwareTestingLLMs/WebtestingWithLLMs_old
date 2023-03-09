import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestInputField(unittest.TestCase):

    def setUp(self):
        # Open the web browser and navigate to the app's URL
        self.browser = webdriver.Chrome()
        self.browser.get(
            'https://sea-lion-app-q6nwz.ondigitalocean.app/sample1')

    def tearDown(self):
        self.browser.quit()

    def test_input_field(self):
        input_field = self.browser.find_element(By.ID, 'inputField')
        input_field.send_keys('Hello, world!')

        click_button = self.browser.find_element(
            By.XPATH, '//button[string()="Click me!"]')
        click_button.click()

        alert = WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        alert_text = alert.text

        self.assertEqual('You typed: Hello, world!', alert_text)

        alert.accept()

        clear_button = self.browser.find_element(
            By.XPATH, '//button[string()="Clear"]')
        clear_button.click()

        self.assertEqual('', input_field.get_attribute('value'))


if __name__ == '__main__':
    unittest.main()
