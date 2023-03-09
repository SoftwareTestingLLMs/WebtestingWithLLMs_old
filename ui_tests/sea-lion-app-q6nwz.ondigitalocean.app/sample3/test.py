
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

browser = webdriver.Chrome()
browser.get("https://sea-lion-app-q6nwz.ondigitalocean.app/sample3")

num1_input = browser.find_element(By.XPATH, '//input[@id="num1"]')
operator_select = browser.find_element(By.XPATH, '//select[@id="operator"]')
num2_input = browser.find_element(By.XPATH, '//input[@id="num2"]')
calculate_button = browser.find_element(By.XPATH, '//button[text()="Calculate"]')
result_input = browser.find_element(By.XPATH, '//input[@id="result"]')

# Test addition
num1_input.clear()
num1_input.send_keys("5")
operator_select.click()
browser.find_element(By.XPATH, '//option[text()="+"]').click()
num2_input.clear()
num2_input.send_keys("2")
calculate_button.click()
assert result_input.get_attribute("value") == "7"

# Test subtraction
num1_input.clear()
num1_input.send_keys("10")
operator_select.click()
browser.find_element(By.XPATH, '//option[text()="-"]').click()
num2_input.clear()
num2_input.send_keys("3")
calculate_button.click()
assert result_input.get_attribute("value") == "7"

# Test multiplication
num1_input.clear()
num1_input.send_keys("4")
operator_select.click()
browser.find_element(By.XPATH, '//option[text()="*"]').click()
num2_input.clear()
num2_input.send_keys("5")
calculate_button.click()
assert result_input.get_attribute("value") == "20"

# Test division
num1_input.clear()
num1_input.send_keys("12")
operator_select.click()
browser.find_element(By.XPATH, '//option[text()="/"]').click()
num2_input.clear()
num2_input.send_keys("3")
calculate_button.click()
assert result_input.get_attribute("value") == "4"

# Test division by zero
num1_input.clear()
num1_input.send_keys("5")
operator_select.click()
browser.find_element(By.XPATH, '//option[text()="/"]').click()
num2_input.clear()
num2_input.send_keys("0")
calculate_button.click()
alert = Alert(browser)
assert alert.text == "Cannot divide by zero!"
alert.dismiss()

# Test exponentiation
num1_input.clear()
num1_input.send_keys("2")
operator_select.click()
browser.find_element(By.XPATH, '//option[text()="^"]').click()
num2_input.clear()
num2_input.send_keys("3")
calculate_button.click()
assert result_input.get_attribute("value") == "8"

# Test square root
num1_input.clear()
num1_input.send_keys("49")
operator_select.click()
browser.find_element(By.XPATH, '//option[text()="sqrt"]').click()
num2_input.clear()
calculate_button.click()
assert result_input.get_attribute("value") == "7"

# Test square root of a negative number
num1_input.clear()
num1_input.send_keys("-5")
operator_select.click()
browser.find_element(By.XPATH, '//option[text()="sqrt"]').click()
num2_input.clear()
calculate_button.click()
alert = Alert(browser)
assert alert.text == "Cannot take square root of a negative number!"
alert.dismiss()

# Test invalid operator
num1_input.clear()
num1_input.send_keys("7")
operator_select.click()
browser.find_element(By.XPATH, '//option[text()="invalid"]').click()
num2_input.clear()
calculate_button.click()
alert = Alert(browser)
assert alert.text == "Invalid operator!"
alert.dismiss()

browser.quit()
