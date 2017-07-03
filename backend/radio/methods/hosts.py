""" hosts.py
This module contains operations related to radio listeners host managment.
"""

import redis
import time
import os
import requests
import json

r = redis.StrictRedis(
    os.environ.get("R_REDIS_HOST", "localhost"),
    os.environ.get("R_REDIS_PORT", "6379"),
    db=os.environ.get("R_REDIS_HOSTINFO_DB", "2")
)

R_REDIS_HOSTINFO_TTL = os.environ.get("R_REDIS_HOSTINFO_TTL", 3600)
R_REDIS_LISTENER_TTL = os.environ.get("R_REDIS_LISTENER_TTL", 3600)

# Test redis connection early (at start time)
# and throw an exception if something gets wrong
r.get(None)

def mark_host_as_recently_active(host_ip):
    timestamp = int(time.time())
    key = "%s-%s" % (host_ip, timestamp)
    r.set(key, 1)
    r.expire(key, R_REDIS_HOSTINFO_TTL)

def get_relative_host_activity(host_ip):
    """Get number of tracks offered by the host recently (R_REDIS_HOSTINFO_TTL)"""
    filter = "%s*" % host_ip
    # get all redis keys that match a filter
    host_entries = r.scan_iter(match=filter)
    activity = len([1 for entry in host_entries])
    return activity

def get_most_inactive_hosts(hosts):
    """Get hosts that offered less tracks
    than the others"""
    # hosts = self.__get_unique_hosts()
    stats = []
    for host in hosts:
        stats.append({
            "host": host,
            "activity": get_relative_host_activity(host)
        })
    min_activity = min([
        h['activity'] for h in stats
    ])
    most_inactive_hosts = [
        h['host'] for h in stats if h['activity'] == min_activity
    ]
    return most_inactive_hosts


def add_unique_listener(host):
    key = "listener-%s" % host
    r.set(key, 1)
    r.expire(key, R_REDIS_LISTENER_TTL)
    pass

def get_unique_listeners():
    listeners = r.scan_iter(match="listener-*")
    return len([1 for listener in listeners])


# FIXME
def get_stream_listeners():
    r = requests.get('http://localhost:8765/status-json.xsl')
    text = r.text.replace('"title": -', '"title": null')
    data = json.loads(text)
    print(json.dumps(data, indent=4))
    listeners = data['icestats']['source'][0]['listeners']
    print("Listeners", listeners)
