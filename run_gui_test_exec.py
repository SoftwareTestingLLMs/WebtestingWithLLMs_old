from selenium import webdriver
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

task = "Your task is to test a web application using python and selenium. Start the python code with <StartCode> and finish the code with a <EndCode> label. Only print the code without further explanations. This is the web application: " + html_source

print(task)

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": task}]
)

response = completion["choices"][0]["message"]["content"]
print(response)

code_string = response
exec(code_string)

# Close the web browser
browser.quit()
