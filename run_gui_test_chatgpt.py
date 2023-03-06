from selenium import webdriver
from selenium.webdriver.common.by import By
import openai
import json

# Get openai key from file
with open("openai_key.json", "r") as file:
    openai.api_key = json.load(file)["key"]

# Open the web browser and navigate to the app's URL
browser = webdriver.Chrome()
browser.get('https://sea-lion-app-q6nwz.ondigitalocean.app/sample1')

# Get the HTML source code of the page
html_source = browser.page_source

task = "Your task is to interact with random a gui button element of the web application below using Selenium's WebDriver API. First, give me the corresponding XPath expression of the gui element you want to interact with and then give me corresponding action, for example \"click\". Put the XPath expression and the action in a json dict with the following keys: \"xpath\" and \"action\". This is the html source of the web application: " + html_source

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": task}]
)

response = completion["choices"][0]["message"]["content"]
response_dict = json.loads(response)
print(response_dict)

# Perform the action on the web element using Selenium
xpath = response_dict['xpath']
action = response_dict['action']

element = browser.find_element(By.XPATH, xpath)
if action == 'click':
    element.click()
elif action == 'submit':
    element.submit()
elif action == 'clear':
    element.clear()
else:
    raise ValueError(f"Unknown action {action}")

# Close the web browser
browser.quit()
