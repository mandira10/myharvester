from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
import re

# MongoDB connection setup
connection_url = "mongodb://134.102.23.199:27017/?directConnection=true"
db_name = "TESTING"
collection_name = "beschas"
client = MongoClient(connection_url)
db = client[db_name]
collection = db[collection_name]
six_months_ago = (datetime.now(timezone.utc) - timedelta(days=5))  # approximately 6 months

def get_tender_ids_evergabe_online():
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://www.evergabe-online.de"},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        unique_tender_data = []
        seen_tender_ids = set()
        
        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    match = re.search(r'id=(\d+)', url)
                    if match:
                        tender_id = match.group(1)
                        if tender_id not in seen_tender_ids:
                            doc['_id'] = str(doc['_id'])
                            unique_tender_data.append({
                                "tender_id": tender_id,
                                "title": title,
                                "url": url,
                                "document": doc
                            })
                            seen_tender_ids.add(tender_id)
        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_tender_ids_evergabe():
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://www.evergabe.de/"},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        unique_tender_data = []
        seen_tender_ids = set()
        
        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    tender_id = None
                    if "suche-ueber-vergabestellen" in url:
                        match = re.search(r'/(\d+)$', url)
                        if match:
                            tender_id = match.group(1)
                    elif "unterlagen" in url:
                        match = re.search(r'/unterlagen/([^/]+)/', url)
                        if match:
                            tender_id = match.group(1)

                    if tender_id and tender_id not in seen_tender_ids:
                        doc['_id'] = str(doc['_id'])
                        unique_tender_data.append({
                            "tender_id": tender_id,
                            "title": title,
                            "url": url,
                            "document": doc
                        })
                        seen_tender_ids.add(tender_id)
        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_tender_ids_bieter_portal_db():
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://bieterportal.noncd.db.de/"},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        unique_tender_data = []
        seen_tender_ids = set()
        
        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    match = re.search(r'deeplink/subproject/([0-9a-f-]+)', url)
                    if match:
                        tender_id = match.group(1)
                        if tender_id not in seen_tender_ids:
                            doc['_id'] = str(doc['_id'])
                            unique_tender_data.append({
                                "tender_id": tender_id,
                                "title": title,
                                "url": url,
                                "document": doc
                            })
                            seen_tender_ids.add(tender_id)
        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_tender_ids_vergabe_autobahn():
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://vergabe.autobahn.de/"},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        unique_tender_data = []
        seen_tender_ids = set()
        
        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    tender_id = None
                    if "TenderingProcedureDetails" in url:
                        match = re.search(r'TenderOID=54321-Tender-([0-9a-zA-Z-]+)', url)
                        if match:
                            tender_id = match.group(1)
                    elif "PublicationControllerServlet" in url:
                        match = re.search(r'TWOID=54321-Tender-([0-9a-zA-Z-]+)', url)
                        if match:
                            tender_id = match.group(1)
                    if tender_id and tender_id not in seen_tender_ids:
                        doc['_id'] = str(doc['_id'])
                        unique_tender_data.append({
                            "tender_id": tender_id,
                            "title": title,
                            "url": url,
                            "document": doc
                        })
                        seen_tender_ids.add(tender_id)
        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    

def get_tender_ids_vergabemarktplatz_brandenburg():
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://vergabemarktplatz.brandenburg.de/"},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        
        unique_tender_data = []
        seen_tender_ids = set()

        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    tender_id_match = re.search(r'/notice/([^/]+)', url)
                    tender_id = tender_id_match.group(1) if tender_id_match else None
                    if tender_id and tender_id not in seen_tender_ids:
                        doc['_id'] = str(doc['_id'])
                        unique_tender_data.append({
                            "tender_id": tender_id,
                            "title": title,
                            "url": url,
                            "document": doc
                        })
                        seen_tender_ids.add(tender_id)

        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
    
def get_tender_ids_dtvp():
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://www.dtvp.de/"},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        
        unique_tender_data = []
        seen_tender_ids = set()
        
        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    tender_id_match = re.search(r'/notice/([^/]+)', url)
                    tender_id = tender_id_match.group(1) if tender_id_match else None
                    if tender_id and tender_id not in seen_tender_ids:
                        doc['_id'] = str(doc['_id'])
                        unique_tender_data.append({
                            "tender_id": tender_id,
                            "title": title,
                            "url": url,
                            "document": doc
                        })
                        seen_tender_ids.add(tender_id)

        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    

def get_tender_ids_vergabe_niedersachsen():
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://vergabe.niedersachsen.de/"},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        
        unique_tender_data = []
        seen_tender_ids = set()
        
        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    tender_id_match = re.search(r'/notice/([^/]+)', url)
                    tender_id = tender_id_match.group(1) if tender_id_match else None
                    if tender_id and tender_id not in seen_tender_ids:
                        doc['_id'] = str(doc['_id'])
                        unique_tender_data.append({
                            "tender_id": tender_id,
                            "title": title,
                            "url": url,
                            "document": doc
                        })
                        seen_tender_ids.add(tender_id)

        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []



def get_tender_ids_vergabe_bremen():
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://vergabe.bremen.de/"},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        unique_tender_data = []
        seen_tender_ids = set()
        
        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    tender_id = None
                    if "TenderingProcedureDetails" in url:
                        match = re.search(r'TenderOID=54321-Tender-([0-9a-zA-Z-]+)', url)
                        if match:
                            tender_id = match.group(1)
                    elif "PublicationControllerServlet" in url:
                        match = re.search(r'TWOID=54321-Tender-([0-9a-zA-Z-]+)', url)
                        if match:
                            tender_id = match.group(1)
                    if tender_id and tender_id not in seen_tender_ids:
                        doc['_id'] = str(doc['_id'])
                        unique_tender_data.append({
                            "tender_id": tender_id,
                            "title": title,
                            "url": url,
                            "document": doc
                        })
                        seen_tender_ids.add(tender_id)
        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    

def get_tender_ids_meinauftrag():
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://www.meinauftrag.rib.de/"},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        
        unique_tender_data = []
        seen_tender_ids = set()

        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    tender_id_match = re.search(r'/tenderId/([^/]+)', url)
                    tender_id = tender_id_match.group(1) if tender_id_match else None
                    if tender_id and tender_id not in seen_tender_ids:
                        doc['_id'] = str(doc['_id'])
                        unique_tender_data.append({
                            "tender_id": tender_id,
                            "title": title,
                            "url": url,
                            "document": doc
                        })
                        seen_tender_ids.add(tender_id)

        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], set()


def get_tender_ids_aumass():
    connection_url = "mongodb://134.102.23.199:27017/?directConnection=true"
    db_name = "TESTING"
    collection_name = "beschas"
    client = MongoClient(connection_url)
    db = client[db_name]
    collection = db[collection_name]
    six_months_ago = (datetime.now(timezone.utc) - timedelta(days=5))
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://plattform.aumass.de/"},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        
        unique_tender_data = []
        seen_tender_ids = set()

        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    tender_id_match = re.search(r'/Veroeffentlichung/([^/]+)', url)
                    tender_id = tender_id_match.group(1) if tender_id_match else None
                    if tender_id and tender_id not in seen_tender_ids:
                        doc['_id'] = str(doc['_id'])
                        unique_tender_data.append({
                            "tender_id": tender_id,
                            "title": title,
                            "url": url,
                            "document": doc
                        })
                        seen_tender_ids.add(tender_id)

        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], set()
    

def get_tender_ids_staatsanzeiger():
    connection_url = "mongodb://134.102.23.199:27017/?directConnection=true"
    db_name = "TESTING"
    collection_name = "beschas"
    client = MongoClient(connection_url)
    db = client[db_name]
    collection = db[collection_name]
    six_months_ago = (datetime.now(timezone.utc) - timedelta(days=5))
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://www.staatsanzeiger-eservices.de/aJs/EFormsBekVuUrl\\?z_param="},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        
        unique_tender_data = []
        seen_tender_ids = set()

        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    if url.startswith("https://www.staatsanzeiger-eservices.de/aJs/EFormsBekVuUrl?z_param="):
                        tender_id_match = re.search(r'z_param=([^&]+)', url)
                        tender_id = tender_id_match.group(1) if tender_id_match else None
                        if tender_id and tender_id not in seen_tender_ids:
                            doc['_id'] = str(doc['_id'])
                            unique_tender_data.append({
                                "tender_id": tender_id,
                                "title": title,
                                "url": url,
                                "document": doc
                            })
                            seen_tender_ids.add(tender_id)

        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], set()



def get_tender_ids_vergabe_vmstart():
    connection_url = "mongodb://134.102.23.199:27017/?directConnection=true"
    db_name = "TESTING"
    collection_name = "beschas"
    client = MongoClient(connection_url)
    db = client[db_name]
    collection = db[collection_name]
    six_months_ago = (datetime.now(timezone.utc) - timedelta(days=8))
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://vergabe.vmstart.de/"},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        unique_tender_data = []
        seen_tender_ids = set()
        
        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    tender_id = None
                    if "TenderingProcedureDetails" in url:
                        match = re.search(r'TenderOID=54321-Tender-([0-9a-zA-Z-]+)', url)
                        if match:
                            tender_id = match.group(1)
                    elif "PublicationControllerServlet" in url:
                        match = re.search(r'TWOID=54321-Tender-([0-9a-zA-Z-]+)', url)
                        if match:
                            tender_id = match.group(1)
                    if tender_id and tender_id not in seen_tender_ids:
                        doc['_id'] = str(doc['_id'])
                        unique_tender_data.append({
                            "tender_id": tender_id,
                            "title": title,
                            "url": url,
                            "document": doc
                        })
                        seen_tender_ids.add(tender_id)
        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    

def get_tender_ids_vergabe_nrw():
    connection_url = "mongodb://134.102.23.199:27017/?directConnection=true"
    db_name = "TESTING"
    collection_name = "beschas"
    client = MongoClient(connection_url)
    db = client[db_name]
    collection = db[collection_name]
    six_months_ago = (datetime.now(timezone.utc) - timedelta(days=6))
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://www.evergabe.nrw.de/"},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        
        unique_tender_data = []
        seen_tender_ids = set()
        
        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    tender_id_match = re.search(r'/notice/([^/]+)', url)
                    tender_id = tender_id_match.group(1) if tender_id_match else None
                    if tender_id and tender_id not in seen_tender_ids:
                        doc['_id'] = str(doc['_id'])
                        unique_tender_data.append({
                            "tender_id": tender_id,
                            "title": title,
                            "url": url,
                            "document": doc
                        })
                        seen_tender_ids.add(tender_id)

        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    

def get_tender_ids_vmp_rheinland():
    connection_url = "mongodb://134.102.23.199:27017/?directConnection=true"
    db_name = "TESTING"
    collection_name = "beschas"
    client = MongoClient(connection_url)
    db = client[db_name]
    collection = db[collection_name]
    six_months_ago = (datetime.now(timezone.utc) - timedelta(days=6))
    try:
        query = {
            "releases.tender.documents.url": {"$regex": "https://www.vmp-rheinland.de/"},
            "releases.date": {"$gte": six_months_ago.isoformat()}
        }
        
        unique_tender_data = []
        seen_tender_ids = set()
        
        for doc in collection.find(query):
            for release in doc.get('releases', []):
                title = release.get('tender', {}).get('title', "")
                for document in release.get('tender', {}).get('documents', []):
                    url = document.get('url', "")
                    tender_id_match = re.search(r'/notice/([^/]+)', url)
                    tender_id = tender_id_match.group(1) if tender_id_match else None
                    if tender_id and tender_id not in seen_tender_ids:
                        doc['_id'] = str(doc['_id'])
                        unique_tender_data.append({
                            "tender_id": tender_id,
                            "title": title,
                            "url": url,
                            "document": doc
                        })
                        seen_tender_ids.add(tender_id)

        client.close()
        return unique_tender_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    