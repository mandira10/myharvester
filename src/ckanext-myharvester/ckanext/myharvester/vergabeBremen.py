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
from .databaseConnection import get_tender_ids_vergabe_bremen
 
def download_tender_files_vergabe_bremen(url, download_dir):
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
        wait = WebDriverWait(driver, 10)
        
        if "PublicationControllerServlet" in url:
            # Click the link to go to the next page
            link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.hiddenForLoggedInUser.noPrint.color-main")))
            link.click()
            # Now, wait for the new page to load
            wait.until(EC.url_contains("TenderingProcedureDetails"))
        
        # Common steps for downloading files
        download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn-modal.zipFileContents")))
        download_button.click()
        modal = wait.until(EC.visibility_of_element_located((By.ID, 'detailModal')))
        select_all_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Alles auswählen']")))
        select_all_button.click()
        confirm_download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Auswahl herunterladen']")))
        confirm_download_button.click()
        wait_until_download_finishes()
        file_path = move_zip_file_to_public(download_dir)
        unzip_file(file_path, download_dir)
        return True
    except TimeoutException:
        print("Nothing to download")
        return False
    finally:
        driver.quit()
    
def gather_stage_vergabe_bremen(harvest_job):
        tender_ids = get_tender_ids_vergabe_bremen()
        return process_multiple_tenders_giving_publisher(tender_ids,harvest_job,download_tender_files_vergabe_bremen,"vergabe_bremen")

