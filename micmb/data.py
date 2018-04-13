from . import common
import os

class Data:

    def __init__(self, config):
        self.config = config
        self.fn = os.path.join('data','data.json')
        if os.path.exists(self.fn):
            self.j = common.read_json(self.fn)
        else:
            self.j = {}

    def set_refreshtime(self,domain,timestamp):
        if 'domain_data_dict' not in self.j:
            self.j['domain_data_dict'] = {}
        if domain not in self.j['domain_data_dict']:
            self.j['domain_data_dict'][domain] = {}
        self.j['domain_data_dict'][domain]['refreshtime'] = timestamp
        self._save()

    def get_refreshtime(self,domain):
        try:
            return self.j['domain_data_dict'][domain]['refreshtime']
        except:
            return 0

    def set_username(self,domain,name):
        if 'domain_data_dict' not in self.j:
            self.j['domain_data_dict'] = {}
        if domain not in self.j['domain_data_dict']:
            self.j['domain_data_dict'][domain] = {}
        self.j['domain_data_dict'][domain]['username'] = name
        self._save()

    def get_username(self,domain):
        try:
            return self.j['domain_data_dict'][domain]['username']
        except:
            return None

    def set_id(self,domain,id):
        if 'domain_data_dict' not in self.j:
            self.j['domain_data_dict'] = {}
        if domain not in self.j['domain_data_dict']:
            self.j['domain_data_dict'][domain] = {}
        self.j['domain_data_dict'][domain]['id'] = id
        self._save()

    def get_id(self,domain):
        try:
            return self.j['domain_data_dict'][domain]['id']
        except:
            return None

    def set_seen_data(self, read_domain, write_domain, read_timestamp, write_timestamp):
        if 'seen_data_dict' not in self.j:
            self.j['seen_data_dict'] = {}
        key = '{1}>{0}'.format(read_domain, write_domain)
        print(key)
        self.j['seen_data_dict'][key] = {
            'read_timestamp': read_timestamp,
            'write_timestamp': write_timestamp
        }
        self._save()

    def get_seen_data(self, read_domain, write_domain):
        key = '{0},{1}'.format(read_domain, write_domain)
        try:
            return self.j['seen_data_dict'][key]
        except:
            return None

    def set_lastrun(self, timestamp):
        self.j['lastrun'] = timestamp
        self._save()

    def get_lastrun(self):
        try:
            return self.j['lastrun']
        except:
            return 0
    
    def _save(self):
        common.write_json(self.fn, self.j)
