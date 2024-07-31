from hashlib import sha1
import json
import logging
import os
import re
import shutil
import time
import zipfile
import requests
from ckan.model import Session, Package
from ckanext.harvest.model import HarvestJob, HarvestObject, HarvestGatherError, \
                                    HarvestObjectError


def extract_password_from_filename(filename):
    match = re.search(r'Kennwort (\S+)\.zip', filename)
    if match:
        return match.group(1)
    return None

def unzip_file(file_path, extract_to,password=None):
        logging.debug('Unzipping file: %s' % file_path)
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                if password:
                  zip_ref.extractall(extract_to, pwd=password.encode())
                else:  
                  zip_ref.extractall(extract_to)
            os.remove(file_path)
            
            # Recursively unzip any nested zip files and move files to extract_to
            for root, dirs, files in os.walk(extract_to):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.endswith('.zip'):
                        password = extract_password_from_filename(file)
                        unzip_file(file_path, extract_to, password)
                    else:
                        # Move file to extract_to directory if it's not already there
                        if root != extract_to:
                            new_path = os.path.join(extract_to, file)
                            if not os.path.exists(new_path):
                                os.rename(file_path, new_path)
                            else:
                                # If file already exists, handle conflict (e.g., rename or skip)
                                logging.warning('File %s already exists in %s. Skipping.' % (file, extract_to))
                                os.remove(file_path)

            # Remove empty directories
            for root, dirs, files in os.walk(extract_to, topdown=False):
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
        except FileNotFoundError as e:
            logging.error('File not found during unzipping: %s' % str(e))
        except OSError as e:
            logging.error('Error while processing files during unzipping: %s' % str(e))


def ensure_directory_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path


def process_multiple_tenders_giving_publisher(tenders,harvest_job,download_function,publisher_name):
        download_dir = "/srv/app/src_extensions/ckanext-myharvester/ckanext/myharvester/public"
        publisher_path = ensure_directory_exists(os.path.join(download_dir, publisher_name))
        harvest_object_ids = []
        for tender in tenders:
            tender_id = tender["tender_id"]
            contract_name = tender["title"]
            doc = tender["document"]
            print(f"Processing tender ID: {tender_id}")
            print(f"Checking for Offline Tag for ID: {tender_id}")
            if has_offline_tag(tender_id.lower()):
                continue
            tender_download_path = ensure_directory_exists(os.path.join(publisher_path, tender_id))
            print(tender_download_path)
            download_result = True
            if publisher_name == "vergabe_autobahn" or publisher_name == "vergabe_bremen" or publisher_name == "meinauftrag" or publisher_name == "aumass" or publisher_name == "staatsanzeiger" or publisher_name == "vergabe_vmstart":
                download_result = download_function(tender["url"], tender_download_path)
            else:
                download_result = download_function(tender_id, tender_download_path)
            files = os.listdir(tender_download_path)
            if not files:
                print(f"No files found for tender ID: {tender_id}. Deleting folder and skipping.")
                shutil.rmtree(tender_download_path)
                continue
            if not download_result:
                print(f"No files found for tender ID: {tender_id}. Adding Offline Tag to Dataset and skipping.")
                add_offline_tag(tender_id.lower())
                continue
            meta_json_path = os.path.join(tender_download_path, 'Meta.json')
            try:
                with open(meta_json_path, 'w', encoding='utf-8') as file:
                    json.dump(doc, file, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"Error saving document {tender_id} to meta.json: {e}")
            files = os.listdir(tender_download_path)
            for file in files:
                file_path = os.path.join(tender_download_path,file)
                if os.path.isfile(file_path):
                    file_hash = sha1(os.path.basename(file_path).encode('utf-8')).hexdigest()
                    guid = f"{tender_id}-{file_hash}"
                    obj = Session.query(HarvestObject).filter_by(guid=guid).first()
                    if not obj:
                        content = json.dumps({'file_path': file_path, 'contract_name': contract_name})
                        obj = HarvestObject(guid=guid, job=harvest_job, content=content)
                        Session.add(obj)
                        Session.commit()
                    harvest_object_ids.append(obj.id)
        return harvest_object_ids



def move_zip_file_to_public(download_dir):
     
    file_path = max([os.path.join("/srv/app", f) for f in os.listdir("/srv/app")], key=os.path.getctime)
    shutil.move(file_path,download_dir)
    return os.path.join(download_dir, os.path.basename(file_path))


def wait_until_download_finishes():
    dl_wait = True
    while dl_wait:
        time.sleep(5)
        dl_wait = False
        for file_name in os.listdir("/srv/app"):
            if file_name.endswith('.crdownload'):
                dl_wait = True



def has_offline_tag(dataset_id):
    ckan_url = 'http://localhost:5000'
    api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJJS1ZNNGh3X3Ftd1M2SmMxWEJUX3N4UVYtazM3Z3hUZlQxVHFBMmNkQWtBIiwiaWF0IjoxNzIxMTU1MzkxfQ.EOMobIL_5ykmmhhicDS6RxIUOzYGsTlCTNppJfp2Kdk'

    package_show_url = f'{ckan_url}/api/3/action/package_show'
    payload = {'id': dataset_id}
    headers = {'Authorization': api_key, 'Content-Type': 'application/json'}

    try:
        response = requests.post(package_show_url, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 200:
            dataset_info = response.json()
            tags = dataset_info['result']['tags']
            for tag in tags:
                if tag['name'].lower() == 'offline':
                    return True
            return False
        elif response.status_code == 404:
            print(f"Dataset with ID '{dataset_id}' does not exist.")
            return False
        else:
            print("Failed to get dataset info:", response.text)
            return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False
    

def add_offline_tag(dataset_id):
    ckan_url = 'http://localhost:5000'
    api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJJS1ZNNGh3X3Ftd1M2SmMxWEJUX3N4UVYtazM3Z3hUZlQxVHFBMmNkQWtBIiwiaWF0IjoxNzIxMTU1MzkxfQ.EOMobIL_5ykmmhhicDS6RxIUOzYGsTlCTNppJfp2Kdk'

    package_show_url = f'{ckan_url}/api/3/action/package_show'
    package_patch_url = f'{ckan_url}/api/3/action/package_patch'

    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.post(package_show_url, data=json.dumps({'id': dataset_id}), headers=headers)

    if response.status_code != 200:
        print(f"Failed to get dataset info: {response.text}")
        return False

    dataset_info = response.json()
    tags = dataset_info['result']['tags']
    tags.append({'name': 'Offline'})

    payload = {
        'id': dataset_id,
        'tags': tags
    }

    response = requests.post(package_patch_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print(f"The 'Offline' tag has been added to the dataset {dataset_id}.")
        return True
    else:
        print(f"Failed to add 'Offline' tag: {response.text}")
        return False