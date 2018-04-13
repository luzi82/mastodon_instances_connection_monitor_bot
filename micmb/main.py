import argparse
from . import common
import copy
import os
from mastodon import Mastodon
import time
from bs4 import BeautifulSoup
from .data import Data
import math
import json
import hashlib

if not os.path.exists('config.json'):
    print('CXTOCNCW config.json not exist')
    sys.exit(1)

timestamp = int(time.time())

common.makedirs('data')

config = common.read_json('config.json')

def sign(j):
    if 'sign' in j:
        del j['sign']
    jc = json.dumps(j, sort_keys=True)
    jc = config['secret'] + jc
    md5 = hashlib.new('md5')
    md5.update(jc.encode('utf8'))
    md5 = md5.hexdigest()
    j['sign'] = md5

def verify(j):
    if j is None:
        return False
    if 'sign' not in j:
        return False
    jj = copy.copy(j)
    del jj['sign']
    jc = json.dumps(jj, sort_keys=True)
    jc = config['secret'] + jc
    md5 = hashlib.new('md5')
    md5.update(jc.encode('utf8'))
    md5 = md5.hexdigest()
    return md5 == j['sign']

# create bot_client.secret
for instance_data in config['instance_data_list']:
    domain = instance_data['domain']
    bot_client_secret_fn = os.path.join('data','instances',domain,'bot_client.secret')
    api_base_url = 'https://{0}'.format(domain)
    if os.path.exists(bot_client_secret_fn):
        continue
    common.makedirs(os.path.dirname(bot_client_secret_fn))
    Mastodon.create_app(
        'mastodon_instances_connection_monitor_bot',
        api_base_url = api_base_url,
        to_file = bot_client_secret_fn
    )

# login
for instance_data in config['instance_data_list']:
    domain = instance_data['domain']
    username = instance_data['username']
    password = instance_data['password']
    bot_client_secret_fn = os.path.join('data','instances',domain,'bot_client.secret')
    user_secret_file = os.path.join('data','instances',domain,'user.secret')
    api_base_url = 'https://{0}'.format(domain)
    
    if os.path.exists(user_secret_file):
        continue

    mastodon = Mastodon(
        client_id = bot_client_secret_fn,
        api_base_url = api_base_url
    )
    mastodon.log_in(
        username,
        password,
        to_file = user_secret_file
    )

data = Data(config)
data.set_lastrun(timestamp)

# username, id
for instance_data in config['instance_data_list']:
    domain = instance_data['domain']
    if (data.get_username(domain) is not None) and (data.get_id(domain) is not None):
        continue

    bot_client_secret_fn = os.path.join('data','instances',domain,'bot_client.secret')
    user_secret_file = os.path.join('data','instances',domain,'user.secret')
    api_base_url = 'https://{0}'.format(domain)
    mastodon = Mastodon(
        client_id = bot_client_secret_fn,
        access_token = user_secret_file,
        api_base_url = api_base_url
    )
    
    avc = mastodon.account_verify_credentials()
    username = avc['username']
    username = '@{0}@{1}'.format(username, domain)
    data.set_username(domain, username)
    data.set_id(domain, avc['id'])

# refresh

refresh_instance_count_max = (len(config['instance_data_list'])+1)*60/config['refresh_min_period']
refresh_instance_count_max = math.ceil(refresh_instance_count_max)
print('refresh_instance_count_max={0}'.format(refresh_instance_count_max))

refreshtime_domain_tuple_list = []
for instance_data in config['instance_data_list']:
    domain = instance_data['domain']
    refreshtime = data.get_refreshtime(domain)
    refreshtime_domain_tuple_list.append((refreshtime, domain))

refreshtime_domain_tuple_list = filter(lambda x:x[0]<timestamp-config['refresh_min_period'],refreshtime_domain_tuple_list)
refreshtime_domain_tuple_list = sorted(refreshtime_domain_tuple_list)
refreshtime_domain_tuple_list = refreshtime_domain_tuple_list[:refresh_instance_count_max]

# mark refresh
for refreshtime_domain_tuple in refreshtime_domain_tuple_list:
    domain = refreshtime_domain_tuple[1]
    data.set_refreshtime(domain, timestamp)

# check follow
for refreshtime_domain_tuple in refreshtime_domain_tuple_list:
    domain = refreshtime_domain_tuple[1]
    bot_client_secret_fn = os.path.join('data','instances',domain,'bot_client.secret')
    user_secret_file = os.path.join('data','instances',domain,'user.secret')
    api_base_url = 'https://{0}'.format(domain)
    mastodon = Mastodon(
        client_id = bot_client_secret_fn,
        access_token = user_secret_file,
        api_base_url = api_base_url
    )
    
    user_id = data.get_id(domain)
    
    follower_list = []
    max_id = None
    while(True):
        _follower_list = mastodon.account_following(user_id, max_id=max_id)
        if len(_follower_list) <= 0:
            break
        follower_list += _follower_list
        if '_pagination_next' not in _follower_list[-1]:
            break
        max_id = _follower_list[-1]['_pagination_next']

    follower_list = [i['acct'] for i in follower_list]
    follower_list = ['@{0}'.format(i) if '@' in i else '@{0}@{1}'.format(i,domain) for i in follower_list]
    add_follower_list = config['instance_data_list']
    add_follower_list = [i['domain'] for i in add_follower_list]
    add_follower_list = [data.get_username(i) for i in add_follower_list]
    add_follower_list = set(add_follower_list) - set(follower_list)
    add_follower_list.remove(data.get_username(domain))
    
    for acct in add_follower_list:
        print('{0} follow {1}'.format(domain, acct))
        mastodon.follows(acct[1:])

# check read
for refreshtime_domain_tuple in refreshtime_domain_tuple_list:
    domain = refreshtime_domain_tuple[1]
    bot_client_secret_fn = os.path.join('data','instances',domain,'bot_client.secret')
    user_secret_file = os.path.join('data','instances',domain,'user.secret')
    api_base_url = 'https://{0}'.format(domain)
    
    mastodon = Mastodon(
        client_id = bot_client_secret_fn,
        access_token = user_secret_file,
        api_base_url = api_base_url
    )
    
    status_list = []
    max_id = None
    while(True):
        _status_list = mastodon.timeline_home(max_id=max_id)
        if len(_status_list) <= 0:
            break
        __status_list = filter(lambda i:i['created_at'].timestamp() >= timestamp-config['timeout'], _status_list)
        __status_list = list(__status_list)
        if len(__status_list) <= 0:
            break
        status_list += __status_list
        if _status_list[-1]['created_at'].timestamp() < timestamp-config['timeout']:
            break
        max_id = _status_list[-1]['id']

    for status in status_list:
        content = status['content']
        try:
            _content = BeautifulSoup(content,'html5lib').text
            print(_content)
            j = json.loads(_content)
            if not verify(j):
                continue
            if j['timestamp'] < timestamp-config['timeout']:
                continue

            seen_data = data.get_seen_data(
                read_domain=domain,
                write_domain=j['domain']
            )
            if seen_data is not None and seen_data['write_timestamp'] > j['timestamp']:
                continue
            data.set_seen_data(
                read_domain=domain,
                write_domain=j['domain'],
                read_timestamp=timestamp,
                write_timestamp=j['timestamp']
            )
        except:
            print('content err: {0}'.format(content))

# do write

for refreshtime_domain_tuple in refreshtime_domain_tuple_list:
    domain = refreshtime_domain_tuple[1]
    bot_client_secret_fn = os.path.join('data','instances',domain,'bot_client.secret')
    user_secret_file = os.path.join('data','instances',domain,'user.secret')
    api_base_url = 'https://{0}'.format(domain)
    
    mastodon = Mastodon(
        client_id = bot_client_secret_fn,
        access_token = user_secret_file,
        api_base_url = api_base_url
    )

    j = {
        'domain':domain,
        'timestamp':timestamp
    }
    sign(j)
    content = json.dumps(j, sort_keys=True)
    mastodon.status_post(content, visibility='unlisted')
    print('{0} {1}'.format(domain,content))
