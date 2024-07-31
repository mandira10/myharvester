import os
import requests
from ckan import model
from ckan.model import Session, Package
from ckanext.harvest.model import HarvestJob, HarvestObject, HarvestGatherError, \
                                    HarvestObjectError
from urllib.parse import unquote
from .helpers import *
from .databaseConnection import get_tender_ids_meinauftrag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time
from selenium.webdriver.chrome.options import Options


def fetch_download_urls_meinauftrag(url,tender_download_path):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)
        try:
            cookie_button = driver.find_element(By.ID, "cookieAll")
            cookie_button.click()
            time.sleep(2)
        except NoSuchElementException:
            print("No cookie banner found")
        try:
            toggle_button = driver.find_element(By.ID, "toggleAllFolder")
            toggle_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].scrollIntoView(true);", toggle_button)
            time.sleep(1)
            toggle_button.click()
        except NoSuchElementException:
            print("Nothing to download skipping...")
            return False
        time.sleep(3)
        try:
            download_buttons = driver.find_elements(By.XPATH, "//tbody//button[@class='btn btn-primary btn-sm']")
            download_links = []
        except NoSuchElementException:
            print("Nothing to download skipping...")
            return False
        for button in download_buttons:
            onclick_attr = button.get_attribute("onclick")
            link = onclick_attr.split("'")[1]
            download_links.append(link)
        try:
            for link in download_links:
                response = requests.get(link)
                response.raise_for_status()
                cd = response.headers.get('Content-Disposition')
                if cd:
                    filename = cd.split('filename=')[-1].strip('"').split('"')[0]
                else:
                    filename = unquote(url.split('/')[-1])

                file_path = os.path.join(tender_download_path, filename)

                with open(file_path, 'wb') as f:
                    f.write(response.content)

                if file_path.endswith('.zip'):
                        password = extract_password_from_filename(filename)
                        unzip_file(file_path, tender_download_path, password)
            return True
        except requests.HTTPError as e:
            logging.error('HTTP error fetching %s: %s' % (url, str(e)))
        except requests.RequestException as e:
            logging.error('Error fetching %s: %s' % (url, str(e)))
    finally:
        driver.quit()


def gather_stage_meinauftrag(harvest_job):
        tenders = get_tender_ids_meinauftrag()
        return process_multiple_tenders_giving_publisher(tenders,harvest_job,fetch_download_urls_meinauftrag,"meinauftrag")
