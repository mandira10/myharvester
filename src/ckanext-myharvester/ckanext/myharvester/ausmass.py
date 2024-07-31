from .helpers import *
from ckan.plugins.core import SingletonPlugin, implements
from ckanext.harvest.interfaces import IHarvester
from ckan import model
from ckan.model import Session, Package
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from ckanext.harvest.model import HarvestJob, HarvestObject, HarvestGatherError, \
                                    HarvestObjectError
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from .databaseConnection import get_tender_ids_aumass
 
def download_tender_files_aumass(url, download_dir):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {
        "download.default_directory": download_dir,
        "savefile.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)

    file_path = None
    try:
        driver.get(url)
        
        try:
            cookies_accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='cc-btn cc-dismiss' and text()='Ich stimme zu.']"))
            )
            cookies_accept_button.click()
            print("Cookies accepted")
        except TimeoutException:
            print("No cookies warning found or it did not appear in time")
        
        wait = WebDriverWait(driver, 10)
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn-download') and contains(text(), 'DOWNLOAD')]")))
        
        download_button.click()
        
        try:
            modal = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog'))
            )
            print("Registration modal appeared")

            ohne_registrierung_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='freierDownloadLinkArea']/a[contains(text(), 'Ohne Registrierung herunterladen')]"))
            )
            ohne_registrierung_button.click()
            print("Clicked 'Ohne Registrierung herunterladen'")

        except TimeoutException:
            print("Registration modal did not appear")

        wait_until_download_finishes()
        file_path = move_zip_file_to_public(download_dir)
        unzip_file(file_path, download_dir)
        return True

    except NoSuchElementException:
        print("Nothing to download")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        driver.quit()
    
def gather_stage_aumass(harvest_job):
        tender_ids = get_tender_ids_aumass()
        return process_multiple_tenders_giving_publisher(tender_ids,harvest_job,download_tender_files_aumass,"aumass")

