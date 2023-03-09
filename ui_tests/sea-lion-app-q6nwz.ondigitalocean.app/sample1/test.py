from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

browser = webdriver.Chrome()
browser.get("https://sea-lion-app-q6nwz.ondigitalocean.app/sample1")

# Test input field
input_field = browser.find_element(By.XPATH, '//input[@id="inputField"]')
assert input_field.is_displayed() == True
assert input_field.is_enabled() == True
input_field.send_keys("Testing 123")
assert input_field.get_attribute("value") == "Testing 123"

# Test button - click
button_click = browser.find_element(By.XPATH, '//button[text()="Click me!"]')
assert button_click.is_displayed() == True
assert button_click.is_enabled() == True
button_click.click()
Alert(browser).dismiss()

# Test button - clear
button_clear = browser.find_element(By.XPATH, '//button[text()="Clear"]')
assert button_clear.is_displayed() == True
assert button_clear.is_enabled() == True
button_clear.click()
assert input_field.get_attribute("value") == ""
