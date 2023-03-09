
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get(
    "https://portal-dev.medi-markt.de/de/termine/rueckruf-vereinbaren/460")


# Fill Form
salutation = browser.find_element(By.XPATH, '//select[@id="salutation"]')
salutation.send_keys('Herr')

name = browser.find_element(By.XPATH, '/html/body/main/div[1]/div/div[1]/div/div[3]/div/form/div/div[2]/div[2]/input')
name.send_keys('Max')

lastname = browser.find_element(By.XPATH, '/html/body/main/div[1]/div/div[1]/div/div[3]/div/form/div/div[2]/div[3]/input')
lastname.send_keys('Mustermann')

phone = browser.find_element(By.XPATH, '/html/body/main/div[1]/div/div[1]/div/div[3]/div/form/div/div[3]/div[1]/input')
phone.send_keys('+49123456789')

street = browser.find_element(By.XPATH, '//input[@id="street"]')
street.send_keys('Teststreet')

hauseNumber = browser.find_element(By.XPATH, '//input[@id="hauseNumber"]')
hauseNumber.send_keys('1')

zipcode = browser.find_element(By.XPATH, '//input[@id="zipcode"]')
zipcode.send_keys('12345')

location = browser.find_element(By.XPATH, '//input[@id="location"]')
location.send_keys('Testcity')

comment = browser.find_element(By.XPATH, '//textarea[@id="comment"]')
comment.send_keys('Test comment')

checkbox = browser.find_element(By.XPATH, '//input[@id="accept_tos"]')
checkbox.click()

# Submit Form
submit_button = browser.find_element(
    By.XPATH, '//button[@id="request_anamnesis_appointment"]')
submit_button.click()
