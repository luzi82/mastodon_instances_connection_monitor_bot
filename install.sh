#!/bin/bash

pip3 install --user --upgrade beautifulsoup4 mastodon.py
sudo cp res/crond /etc/cron.d/mastodon_instances_connection_monitor_bot
