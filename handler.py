import datetime
import json
import os
import boto3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

s3 = boto3.resource('s3')

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

        # Save a screenshot to the tmp directory
        try:
            now_jst = datetime.datetime.now(
                datetime.timezone(datetime.timedelta(hours=9)))
            filename = f"{now_jst.strftime('%Y%m%d_%H%M%S')}.png"
            filepath = f"/tmp/{filename}.png"
            driver.save_screenshot(filepath)
            # Copy the screenshot file to S3
            bucket_name = "selenium-on-aws-lambda-screenshots"
            s3.meta.client.upload_file(filepath, bucket_name, filename)
        except:
            if "filepath" in locals():
                if os.path.exists(filepath):
                    os.remove(filepath)

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
        if "driver" in locals():
            driver.quit()
