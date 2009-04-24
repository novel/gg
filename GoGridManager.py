#!/usr/bin/env python

from random import choice
from GoGridClient import GoGridClient
#import paramiko

class GGIp:

    def __init__(self, tokens):
        self.id = tokens[0]
        self.ip = tokens[1]
        self.subnet = tokens[2]
        self.public = (tokens[3] == "true")

    #def __init__(self, id, ip, subnet, public):
    #    self.id = id
    #    self.ip = ip
    #    self.subnet = subnet
    #    self.public = public

    def __str__(self):
        return "ip = %s (id = %s, subnet = %s, public: %s)" % (self.ip, self.id, self.subnet, self.public)

class GGServer:
    
    def __init__(self, tokens):
        self.id = tokens[0]
        self.name = tokens[1]
        self.descr = tokens[2]
        self.ip = GGIp([tokens[3], tokens[4], tokens[5], tokens[6]])
        self.state = tokens[20]

    def __str__(self):
        return "server %s (id = %s, descr = %s, state = %s, ip = %s)" % (self.name, 
                self.id, self.descr, self.state, self.ip.ip)

class GGImage:

    def __init__(self, tokens):
        if len(tokens) == 9:
            self.id = tokens[0]
            self.name = tokens[1]
            self.friendlyName = tokens[2]
            self.descr = tokens[3]
            self.location = tokens[4]
            self.isActive = (tokens[5] == "true")
            self.isPublic = (tokens[6] == "true")
            self.createdTime = tokens[7]
            self.updatedTime = tokens[8]
        else:
            self.id = tokens[0]
            self.name = tokens[1]

    def __str__(self):
        return "image %s (id = %s)" % (self.name, self.id)

class GGPassword:

    def __init__(self, tokens):
        self.id = tokens[0]
        self.server = GGServer(tokens[1:])
        self.username = tokens[30]
        self.password = tokens[31]

    def __str__(self):
        return "%s:%s@%s (id = %s)" % (self.username, self.password, self.server.ip.ip, self.id)

class GoGridManager:

    def __init__(self):
        self.gogrid_client = GoGridClient()


    def find_image_by_name(self, name):
        for image in self.get_image_list():
            if name == image[1]:
                return image

######################
######################

    def get_ips(self, type="all", state=None):       
        param_dict = {}

        if type != "all":
            param_dict["ip.type"] = type

        if state != None:
            param_dict["ip.state"] = state

        data = self.gogrid_client.sendAPIRequest("grid/ip/list", param_dict)

        data = data.splitlines()
        del data[0:2]

        return map(lambda item: GGIp(item.split(",")), data)

    def get_servers(self):
        param_dict = {} 

        data = self.gogrid_client.sendAPIRequest("grid/server/list", param_dict)

        data = data.splitlines()
        del data[0:2]

        return map(lambda item: GGServer(item.split(",")), data)

    def get_images(self):
        """Returns a list of available server images"""
        data = self.gogrid_client.sendAPIRequest("grid/image/list", {}).splitlines()

        del data[0:2]
        return map(lambda item: GGImage(item.split(",")), data)

    def get_passwords(self):
        data = self.gogrid_client.sendAPIRequest("support/password/list", {}).splitlines()

        del data[0:2]
        return map(lambda item: GGPassword(item.split(",")), data)

    def add_server(self, name, image, ram, ip, descr=None):
        param_dict = {"name": name, "image": image, "ram": ram, "ip": ip}

        if descr is not None:
            param_dict["description"] = descr

        response = self.gogrid_client.sendAPIRequest("grid/server/add", param_dict).splitlines()

        del response[0:2]

        return GGServer(response[0].split(","))

    def delete_server(self, id, name):
        if id is not None:
            param_dict = {'id': id}
        else:
            param_dict = {'name': name} 

        # XXX to raise an exception if both fields are None
        
        response = self.gogrid_client.sendAPIRequest("grid/server/delete", param_dict).splitlines()

        del response[0:2]

        return GGServer(response[0].split(","))


    def power_server(self, id, name, action):
        if id is not None:
            param_dict = {"id": id}
        else:
            param_dict = {"name": name}

        param_dict["power"] = action

        response = self.gogrid_client.sendAPIRequest("grid/server/power", param_dict).splitlines()

        del response[0:2]

        return GGServer(response[0].split(","))

    def get_billing(self):
        response = self.gogrid_client.sendAPIRequest("myaccount/billing/get", {}).splitlines()

        del response[0]
        keys = response[0][2:].split(",")
        values = response[1].split(",")

        return dict(zip(keys, values))

######################
######################
    def get_free_public_ips(self):
        """Returns a list of currenty available public ips"""

        data = self.gogrid_client.sendAPIRequest("grid/ip/list", 
                {"format": "csv", "ip.state": "Unassigned",
                    "ip.type": "Public"})

        data = data.splitlines()
        del data[0:2]
            
        return map(lambda item: item.split(","), data)   

    def get_free_public_ip(self):
        ips = self.get_free_public_ips()

        print len(ips)

        return choice(ips)

    def get_server_by_name(self, name):
#        data = self.gogrid_client.sendAPIRequest("grid/server/get",
#                {"name": name, "format": "csv"}).splitlines()
#
#        del data[0:2]
#
#        return map(lambda item: item.split(","), data)[0]
        servers = self.get_server_list()

        for server in servers:
            if server[1] == name:
                return server

    def get_server_by_id(self, id):
        data = self.gogrid_client.sendAPIRequest("grid/server/get",
                {"id": id, "format": "xml"})
        return data

    def get_server_list(self):
        data = self.gogrid_client.sendAPIRequest("grid/server/list", {"format": "csv"}).splitlines()
        del data[0:2]

        return map(lambda item: item.split(","), data)

    def get_password_by_ip(self, ip):
        lines = self.gogrid_client.sendAPIRequest("support/password/list", {'format': 'csv'}).splitlines()

        del lines[0:2]

        for line in lines:
            chunks = line.split(",")
            server_ip = chunks[5]

            if ip == server_ip:
                login = chunks[30]
                password = chunks[31]
                return login, password

    def add_public_server(self, name):
        ip = self.get_free_public_ip()
        image = self.find_image_by_name("centos51_64_apache")
        ram = "4GB"
    
        print "adding server with ip = %s and image id = %s" % (ip[1], image[0])
        data = self.gogrid_client.sendAPIRequest("grid/server/add", 
                {"name": name, "image": image[0], "ram": ram, "ip": ip[1], "format": "csv"}).splitlines()

        del data[0:2]
        return map(lambda item: item.split(","), data)

    #def bootstrap_server(self, ip):
        #print "bootstraping server with ip = %s" % ip

        #login, password = self.get_password_by_ip(ip)

        #print "%s: login = %s, password = %s" % (ip, login, password)

        #t = paramiko.Transport((ip, 22))
        #t.connect(username=login, password=password)

        #commands = [ 'useradd guest', 'echo guest | passwd --stdin guest' ]

        #for command in commands:
            #chan = t.open_session()
            #chan.exec_command(command)
            #chan.close()

        #t.close()
     



