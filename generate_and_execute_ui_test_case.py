import click
from selenium import webdriver
import openai
import json

# Define the command-line options


@click.command()
@click.option('--url', default='https://sea-lion-app-q6nwz.ondigitalocean.app/sample1', help='The URL of the web application to test.')
def main(url):

    # Get openai key from file
    with open("openai_key.json", "r") as file:
        openai.api_key = json.load(file)["key"]

    # Open the web browser and navigate to the app's URL
    browser = webdriver.Chrome()
    browser.get(url)

    # Get the HTML source code of the page
    html_source = browser.page_source

    # Close the web browser
    browser.quit()

    task = f"Your task is to test a web application using python and selenium with the URL {url}. Start the python code with <StartCode> and finish the code with a <EndCode> label. Use \"browser = webdriver.Chrome()\" to open the web browser. Use only xpath commands like \"browser.find_element(By.XPATH, '//button[text()=\"Click me!\"]')\" to find elements. If there is an alert, the script should switch to the alert and dismiss it before proceeding with the next step. Use assertions to test the correct behavior of the application. Only print the code without further explanations. This is the web application: {html_source}"

    click.echo(task)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": task}]
    )

    response = completion["choices"][0]["message"]["content"]
    click.echo(response)

    # Extract code between <StartCode> and <EndCode> labels
    start_index = response.find("<StartCode>") + len("<StartCode>")
    end_index = response.find("<EndCode>")
    code_string = response[start_index:end_index]

    # Execute the code
    exec(code_string)

    # Close the web browser
    browser.quit()


if __name__ == '__main__':
    main()
