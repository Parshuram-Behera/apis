from appwrite.client import Client
import os
import logging
import yt_dlp
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_download_urls(video_url):
    try:
        # Configure Selenium to use headless Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(video_url)

        # Wait for the page to load and handle potential CAPTCHAs
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(10)  # Adjust sleep time as needed

        # Parse the page source with BeautifulSoup
        page_source = driver.page_source
        driver.quit()
        soup = BeautifulSoup(page_source, 'html.parser')

        # Example parsing logic (YouTube's page structure can be complex)
        video_urls = []
        for script in soup.find_all('script'):
            if 'var ytInitialPlayerResponse' in script.text:
                start_index = script.text.find('var ytInitialPlayerResponse =') + len('var ytInitialPlayerResponse = ')
                end_index = script.text.find(';', start_index)
                json_text = script.text[start_index:end_index].strip()

                import json
                player_response = json.loads(json_text)
                formats = player_response.get('streamingData', {}).get('formats', [])

                # Extract URLs from formats
                for fmt in formats:
                    url = fmt.get('url')
                    resolution = fmt.get('height', 'unknown')
                    if url:
                        video_urls.append(f'Resolution: {resolution}p, URL: {url}')

                break

        if not video_urls:
            logging.warning("No video URLs found")
            return ["No video URLs found"]

        return video_urls

    except Exception as e:
        logging.error(f"Error processing URL {video_url}: {e}")
        raise e


def main(context):
    if context.req.method == "GET":
        value = context.req.query.get("value")

        if value:
            try:
                download_urls = get_download_urls(value)
                result_string = '\n'.join(download_urls)
                return context.res.send(result_string)
            except Exception as e:
                return context.res.send(f"Error processing URL: {str(e)}")
        else:
            return context.res.send("Value parameter is missing in GET REQUEST")

    return context.res.json({
        "message": "Hello Parshuram Behera"
    })
