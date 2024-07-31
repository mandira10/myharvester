from ckan.plugins.core import SingletonPlugin, implements
from ckanext.harvest.interfaces import IHarvester
import logging
from ckan import model
from ckan.model import Session, Package
import json
from ckanext.harvest.model import HarvestJob, HarvestObject, HarvestGatherError, \
                                    HarvestObjectError
from .helpers import *
from .vergabeAutobahn import gather_stage_vergabe_autobahn
from .bieterPortal import gather_stage_bieter
from .evergabe import gather_stage_evergabe
from .evergabeOnline import gather_stage_evergabeOnline
from .vergabemarktplatz_brandenburg import gather_stage_vergabeBrandenburg
from .dtvp import gather_stage_dtvp
from .vergabeNiedersachsen import gather_stage_vergabe_niedersachsen
from .vergabeBremen import gather_stage_vergabe_bremen
from .meinauftrag import gather_stage_meinauftrag
from .ausmass import gather_stage_aumass
from .staatsanzeiger import gather_stage_staatsanzeiger
from .vergabeVmstart import gather_stage_vergabe_vmstart
from .vergabeNrw import gather_stage_vergabe_nrw
from .vmpRheinland import gather_stage_vmp_rheinland
from .importHelpers import import_stage_giving_publisher

class MyharvesterPlugin(SingletonPlugin):
    implements(IHarvester)

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)

  
    def info(self):
        return {
            'name': 'myharvester',
            'title': 'My Harvester',
            'description': 'A test harvester for CKAN that handles PDF and ZIP resources'
        }
    
    def get_original_url(self, harvest_object_id):
        obj = HarvestObject.get(harvest_object_id)
        if not obj:
            return None
        original_url = obj.source.url
        return original_url
    


    def gather_stage(self, harvest_job):
        self.log.debug('Gather stage for: %s' % harvest_job.source.url)
        
        if "vergabe.autobahn.de" in harvest_job.source.url:
            return gather_stage_vergabe_autobahn(harvest_job)
        elif "https://bieterportal.noncd.db.de/" in harvest_job.source.url:
            return gather_stage_bieter(harvest_job)
        elif "https://www.evergabe.de/" in harvest_job.source.url:
            return gather_stage_evergabe(harvest_job)
        elif "https://www.evergabe-online.de/" in harvest_job.source.url:
            return gather_stage_evergabeOnline(harvest_job)
        elif "https://vergabemarktplatz.brandenburg.de/" in harvest_job.source.url:
            return gather_stage_vergabeBrandenburg(harvest_job)
        elif "https://www.dtvp.de/" in harvest_job.source.url:
            return gather_stage_dtvp(harvest_job)
        elif "https://vergabe.niedersachsen.de/" in harvest_job.source.url:
            return gather_stage_vergabe_niedersachsen(harvest_job)
        elif "https://vergabe.bremen.de/" in harvest_job.source.url:
            return gather_stage_vergabe_bremen(harvest_job)
        elif "https://www.meinauftrag.rib.de/" in harvest_job.source.url:
            return gather_stage_meinauftrag(harvest_job)
        elif "https://plattform.aumass.de/" in harvest_job.source.url:
            return gather_stage_aumass(harvest_job)
        elif "https://www.staatsanzeiger-eservices.de/" in harvest_job.source.url:
            return gather_stage_staatsanzeiger(harvest_job)
        elif "https://vergabe.vmstart.de/" in harvest_job.source.url:
            return gather_stage_vergabe_vmstart(harvest_job)
        elif "https://www.evergabe.nrw.de/" in harvest_job.source.url:
            return gather_stage_vergabe_nrw(harvest_job)
        elif "https://www.vmp-rheinland.de/" in harvest_job.source.url:
            return gather_stage_vmp_rheinland(harvest_job)

        raise HarvestGatherError()

    def fetch_stage(self, harvest_object):
        self.log.debug('Fetch stage for object: %s' % harvest_object.id)

        if "vergabe.autobahn.de" in self.get_original_url(harvest_object.id):
            return True
        elif "https://bieterportal.noncd.db.de/" in self.get_original_url(harvest_object.id):
            return True
        elif "https://www.evergabe.de/" in self.get_original_url(harvest_object.id):
            return True
        elif "https://www.evergabe-online.de/" in self.get_original_url(harvest_object.id):
            return True
        elif "https://vergabemarktplatz.brandenburg.de/" in self.get_original_url(harvest_object.id):
            return True
        elif "https://www.dtvp.de/" in self.get_original_url(harvest_object.id):
            return True
        elif "https://vergabe.niedersachsen.de/" in self.get_original_url(harvest_object.id):
            return True
        elif "https://vergabe.bremen.de/" in self.get_original_url(harvest_object.id):
            return True
        elif "https://www.meinauftrag.rib.de/" in self.get_original_url(harvest_object.id):
            return True
        elif "https://plattform.aumass.de/" in self.get_original_url(harvest_object.id):
            return True
        elif "https://www.staatsanzeiger-eservices.de/" in self.get_original_url(harvest_object.id):
            return True
        elif "https://vergabe.vmstart.de/" in self.get_original_url(harvest_object.id):
            return True
        elif "https://www.evergabe.nrw.de/" in self.get_original_url(harvest_object.id):
            return True
        elif "https://www.vmp-rheinland.de/" in self.get_original_url(harvest_object.id):
            return True
        
        
        return False
    def import_stage(self, harvest_object):
        self.log.debug('Import stage for object: %s' % harvest_object.id)
        self.log.debug('Harvesting object: %s' % harvest_object)

        if "vergabe.autobahn.de" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"vergabe-autobahn")
        elif "https://bieterportal.noncd.db.de/" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"bieter-portal-db")
        elif "https://www.evergabe.de/" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"evergabe")
        elif "https://www.evergabe-online.de/" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"evergabe-online")
        elif "https://vergabemarktplatz.brandenburg.de/" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"vergabemarktplatz-brandenburg")
        elif "https://www.dtvp.de/" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"dtvp")
        elif "https://vergabe.niedersachsen.de/" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"vergabe-niedersachsen")
        elif "https://vergabe.bremen.de/" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"vergabe-bremen")
        elif "https://www.meinauftrag.rib.de/" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"meinauftrag")
        elif "https://plattform.aumass.de/" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"aumass")
        elif "https://www.staatsanzeiger-eservices.de/" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"staatsanzeiger")
        elif "https://vergabe.vmstart.de/" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"vergabe-vmstart")
        elif "https://www.evergabe.nrw.de/" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"vergabe-nrw")
        elif "https://www.vmp-rheinland.de/" in self.get_original_url(harvest_object.id):
            return import_stage_giving_publisher(harvest_object,"vmp-rheinland")
            
        return False


    def _create_or_update_package(self, data_dict, harvest_object):
        pass

    def _set_config(self, config_str):
        if config_str:
            self.config = json.loads(config_str)
        else:
            self.config = {}
