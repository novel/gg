#!/usr/bin/env python

import sys
import time
from random import choice
from GoGridManager import GoGridManager

manager = GoGridManager()

NUM_SERVERS = 4
RUNS = 3

def check_ips():
    ips = manager.get_ips(type="Public", state="Unassigned")

    if len(ips) < NUM_SERVERS * 1.5:
        print "Not enough free IP addresses (%s required)." % (NUM_SERVERS * 1.5)
        sys.exit(1)

def server_status(name):
    servers = manager.get_servers()

    for server in servers:
        if name == server.name:
            return server.state

if __name__ == "__main__":
#    check_ips()

    servers = {}
    times = []

    for i in range(NUM_SERVERS):
        name = "bench_%s" % (i,)
        ip = choice(manager.get_ips(type='Public', state='Unassigned')).ip      
        server = manager.add_server(name, '62', '2GB', ip)
        timestamp = int(time.time())

         #print server.name
        servers[server.name] = timestamp

    while True:
        for k,v in servers.iteritems():
            if "Started" == server_status(k):
                # server has started, print bootstrapping time, remove and create a new one
                delta = int(time.time()) - servers[k]
                print delta
                times.append(delta)
                manager.delete_server(None, k)
                
                # sleep just to make sure
                time.sleep(10)

                ip = choice(manager.get_ips(type='Public', state='Unassigned')).ip      
                server = manager.add_server(k, '62', '2GB', ip)
                timestamp = int(time.time())

                servers[k] = timestamp
        
        time.sleep(20)

