import argparse

if not os.path.exists('config.json'):
    print('CXTOCNCW config.json not exist')
    sys.exit(1)

common.makedirs('data')

config = common.read_json('config.json')

for instance_data in config['instance_data_list']:
    domain = instance_data['domain']
    bot_client_secret_fn = os.path.join('data','instances',domain,'bot_client.secret')
    if os.path.exist(bot_client_secret_fn)
        continue
    common.makedirs(os.path.join('data','instances',domain)
    Mastodon.create_app(
         'mastodon_instances_connection_monitor_bot',
         api_base_url = 'https://{0}'.format(domain),
         to_file = bot_client_secret_fn
    )
