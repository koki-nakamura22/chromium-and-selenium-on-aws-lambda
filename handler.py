import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def func(event, context):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--single-process")
        chrome_options.binary_location = "/opt/bin/headless-chromium"

        driver = webdriver.Chrome(
            executable_path="/opt/bin/chromedriver",
            chrome_options=chrome_options
        )
        driver.get("https://www.python.org/")
        search_bar = driver.find_element_by_name("q")
        search_bar.clear()
        search_bar.send_keys("getting started with python")
        search_bar.send_keys(Keys.RETURN)

        body = {
            "title": driver.title,
            "currentURL": driver.current_url
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

        return response

    finally:
        if 'driver' in locals():
            driver.quit()
