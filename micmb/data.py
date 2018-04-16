from . import common
import os
import dateutil.parser
import datetime

class Data:

    def __init__(self, config, timestamp):
        self.config = config
        self.timestamp = timestamp
        self.fn = os.path.join('data','data.json')
        if os.path.exists(self.fn):
            self.j = common.read_json(self.fn)
        else:
            self.j = {}

    def add_domain_try_write_time(self,domain,timestamp):
        if 'domain_data_dict' not in self.j:
            self.j['domain_data_dict'] = {}
        if domain not in self.j['domain_data_dict']:
            self.j['domain_data_dict'][domain] = {}
        if 'try_write_time_list' not in self.j['domain_data_dict'][domain]:
            self.j['domain_data_dict'][domain]['try_write_time_list'] = []
        self.j['domain_data_dict'][domain]['try_write_time_list'].append(timestamp)
        timeout = self.timestamp - self.config['timeout']
        self.j['domain_data_dict'][domain]['try_write_time_list'] = list(filter(
                lambda i:i>=timeout,
                self.j['domain_data_dict'][domain]['try_write_time_list']
        ))
        self._save()

    def get_min_domain_try_write_time(self,domain):
        try:
            timeout = self.timestamp - self.config['timeout']
            return min(filter(
                lambda i:i>=timeout,
                self.j['domain_data_dict'][domain]['try_write_time_list']
            ))
        except:
            return 0

    def get_max_domain_try_write_time(self,domain):
        try:
            timeout = self.timestamp - self.config['timeout']
            return max(filter(
                lambda i:i>=timeout,
                self.j['domain_data_dict'][domain]['try_write_time_list']
            ))
        except:
            return 0

    def add_domain_success_write_time(self,domain,timestamp):
        if 'domain_data_dict' not in self.j:
            self.j['domain_data_dict'] = {}
        if domain not in self.j['domain_data_dict']:
            self.j['domain_data_dict'][domain] = {}
        if 'success_write_time_list' not in self.j['domain_data_dict'][domain]:
            self.j['domain_data_dict'][domain]['success_write_time_list'] = []
        self.j['domain_data_dict'][domain]['success_write_time_list'].append(timestamp)
        timeout = self.timestamp - self.config['timeout']
        self.j['domain_data_dict'][domain]['success_write_time_list'] = list(filter(
                lambda i:i>=timeout,
                self.j['domain_data_dict'][domain]['success_write_time_list']
        ))
        self._save()

    def get_min_domain_success_write_time(self,domain):
        try:
            timeout = self.timestamp - self.config['timeout']
            return min(filter(
                lambda i:i>=timeout,
                self.j['domain_data_dict'][domain]['success_write_time_list']
            ))
        except:
            return 0

    def set_domain_try_read_time(self,domain,timestamp):
        if 'domain_data_dict' not in self.j:
            self.j['domain_data_dict'] = {}
        if domain not in self.j['domain_data_dict']:
            self.j['domain_data_dict'][domain] = {}
        self.j['domain_data_dict'][domain]['try_read_time'] = timestamp
        self._save()

    def get_domain_try_read_time(self,domain):
        try:
            return self.j['domain_data_dict'][domain]['try_read_time']
        except:
            return 0

    def set_domain_success_read_time(self,domain,timestamp):
        if 'domain_data_dict' not in self.j:
            self.j['domain_data_dict'] = {}
        if domain not in self.j['domain_data_dict']:
            self.j['domain_data_dict'][domain] = {}
        self.j['domain_data_dict'][domain]['success_read_time'] = timestamp
        self._save()

    def get_domain_success_read_time(self,domain):
        try:
            return self.j['domain_data_dict'][domain]['success_read_time']
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

    def set_domain2_follow_time(self,write_domain,read_domain,timestamp):
        key = '{0}>{1}'.format(write_domain,read_domain)
        if 'domain2_data_dict' not in self.j:
            self.j['domain2_data_dict'] = {}
        if key not in self.j['domain2_data_dict']:
            self.j['domain2_data_dict'][key] = {}
        self.j['domain2_data_dict'][key]['follow_time'] = timestamp
        self._save()

    def get_domain2_follow_time(self,write_domain,read_domain):
        try:
            key = '{0}>{1}'.format(write_domain,read_domain)
            return self.j['domain2_data_dict'][key]['follow_time']
        except:
            return None

    def set_domain2_msg_time(self,write_domain,read_domain,timestamp):
        key = '{0}>{1}'.format(write_domain,read_domain)
        if 'domain2_data_dict' not in self.j:
            self.j['domain2_data_dict'] = {}
        if key not in self.j['domain2_data_dict']:
            self.j['domain2_data_dict'][key] = {}
        self.j['domain2_data_dict'][key]['msg_time'] = timestamp
        self._save()

    def get_domain2_msg_time(self,write_domain,read_domain):
        try:
            key = '{0}>{1}'.format(write_domain,read_domain)
            return self.j['domain2_data_dict'][key]['msg_time']
        except:
            return 0

    def set_domain2_state(self,write_domain,read_domain,timestamp):
        key = '{0}>{1}'.format(write_domain,read_domain)
        if 'domain2_data_dict' not in self.j:
            self.j['domain2_data_dict'] = {}
        if key not in self.j['domain2_data_dict']:
            self.j['domain2_data_dict'][key] = {}
        self.j['domain2_data_dict'][key]['state'] = timestamp
        self._save()

    def get_domain2_state(self,write_domain,read_domain):
        try:
            key = '{0}>{1}'.format(write_domain,read_domain)
            return self.j['domain2_data_dict'][key]['state']
        except:
            return 'unknown'

    def set_lastrun(self, timestamp):
        self.j['lastrun'] = timestamp
        self._save()

    def get_lastrun(self):
        try:
            return self.j['lastrun']
        except:
            return 0

    def set_next_heartbeat(self, t):
        self.j['next_heartbeat'] = str(t)
        self._save()
    
    def get_next_heartbeat(self):
        try:
            return dateutil.parser.parse(self.j['next_heartbeat'])
        except:
            return datetime.datetime.fromtimestamp(0)
    
    def _save(self):
        common.write_json(self.fn, self.j)
