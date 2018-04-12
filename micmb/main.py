import argparse
from . import common
import copy
import os
from mastodon import Mastodon

def instance_data_more(instance_data):
    domain = instance_data['domain']
    bot_client_secret_fn = os.path.join('data','instances',domain,'bot_client.secret')
    user_secret_file = os.path.join('data','instances',domain,'user.secret')
    api_base_url = 'https://{0}'.format(domain)

    ret = copy.copy(instance_data)
    ret['bot_client_secret_fn'] = bot_client_secret_fn
    ret['user_secret_file'] = user_secret_file
    ret['api_base_url'] = api_base_url
    
    return ret

if not os.path.exists('config.json'):
    print('CXTOCNCW config.json not exist')
    sys.exit(1)

common.makedirs('data')

config = common.read_json('config.json')

# create bot_client.secret
for instance_data in config['instance_data_list']:
    instance_data = instance_data_more(instance_data)
    domain = instance_data['domain']
    bot_client_secret_fn = instance_data['bot_client_secret_fn']
    api_base_url = instance_data['api_base_url']
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
    instance_data = instance_data_more(instance_data)
    domain = instance_data['domain']
    username = instance_data['username']
    password = instance_data['password']
    user_secret_file = os.path.join('data','instances',domain,'user.secret')
    bot_client_secret_fn = os.path.join('data','instances',domain,'bot_client.secret')
    api_base_url = instance_data['api_base_url']
    
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
