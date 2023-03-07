from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Open the web browser and navigate to the app's URL
browser = webdriver.Chrome()
browser.get('https://sea-lion-app-q6nwz.ondigitalocean.app/sample1')

# Get the HTML source code of the page
html_source = browser.page_source

# Use BeautifulSoup to parse the HTML source code
soup = BeautifulSoup(html_source, 'html.parser')

# Find the input field and enter text into it
input_field = browser.find_element(By.ID, 'inputField')
input_field.send_keys('Hello, world!')

# Find the "Click me!" button and click it
click_button = browser.find_element(By.XPATH, '//button[text()="Click me!"]')
click_button.click()

# Check if the alert message is displayed with the correct text
alert = browser.switch_to.alert
assert 'You typed: Hello, world!' == alert.text
alert.accept()

# Find the "Clear" button and click it
clear_button = browser.find_element(By.XPATH, '//button[text()="Clear"]')
clear_button.click()

# Check if the input field is cleared
assert '' == input_field.get_attribute('value')

# Print the HTML structure of the page
print(soup.prettify())

# Close the web browser
browser.quit()