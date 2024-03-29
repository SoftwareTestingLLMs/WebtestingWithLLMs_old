import click
import os
from selenium import webdriver
import openai
import json
from tools.common import clean_html, generate_directory_path


@click.command()
@click.option('--url', default='https://sea-lion-app-q6nwz.ondigitalocean.app/sample1', help='The URL of the web application to test.')
@click.option('--base_dir', default='ui_tests', help='The base directory where the ui tests should be saved.')
def main(url, base_dir):
    # Get OpenAI API key from file
    with open("openai_key.json", "r") as file:
        openai.api_key = json.load(file)["key"]

    # Open the web browser and navigate to the app's URL
    browser = webdriver.Chrome()
    browser.get(url)

    # Get the HTML source code of the page
    html_source_cleaned = clean_html(browser.page_source)

    # Close the web browser
    browser.quit()

    task = (f"Your task is to test a web application using python and selenium with the URL {url}. Start the python "
            f"code with <StartCode> and finish the code with a <EndCode> label. Use \"browser = webdriver.Chrome()\" "
            f"to open the web browser. Use only xpath commands "
            f"like \"browser.find_element(By.XPATH, '//button[text()=\"Click me!\"]')\" to find elements. If there is "
            f"an alert, the script should switch to the alert and dismiss it before proceeding with the next step. "
            f"Use assertions to test the correct behavior of the application. Only print the code without further "
            f"explanations. This is the web application: {html_source_cleaned}")

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

    # Generate the directory path
    directory_path = generate_directory_path(url, base_dir)

    # Save the generated test to file
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    with open(os.path.join(directory_path, "test.py"), "w") as file:
        file.write(code_string)

    # Execute the code
    exec(code_string)

    # Close the web browser
    browser.quit()


if __name__ == '__main__':
    main()
