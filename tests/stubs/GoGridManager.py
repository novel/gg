#!/usr/bin/env python

from random import choice
from GoGridClient import GoGridClient

class GGIp:

    def __init__(self, tokens):
        self.id = tokens[0]
        self.ip = tokens[1]
        self.subnet = tokens[2]
        self.public = (tokens[3] == "true")

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
        self.server = GGServer(tokens[2:])
        self.username = tokens[31]
        self.password = tokens[32]

    def __str__(self):
        return "%s:%s@%s (id = %s)" % (self.username, self.password, self.server.ip.ip, self.id)

class GoGridManager:

    def __init__(self, key='', secret=''):
        #self.gogrid_client = GoGridClient(key, secret)
        pass

######################
######################

    def get_ips(self, type="all", state=None):
        return []

    def get_servers(self):
        return []

    def get_images(self):
        return []

    def get_passwords(self):
        return []

    def add_server(self, name, image, ram, ip, descr=None):
        """
        A method to add a new server.

        @type name: string
        @param name: desired name of the newely created server
        @type image: string
        @param image: image to be used for the server. You can use either symbolic name or numeric image id, but even
        if you specify image by id, it should still be string
        @type ram: string
        @param ram: desired amount of RAM for the server
        @type ip: string
        @param ip: IP address to be assigned to the server. Remember that you have to specify public IP address, private address will not work here
        @type descr: string
        @param descr: optional literal description of the server, may be omitted
        @rtype: L{GGServer<GGServer>}
        @return: a L{GGServer<GGServer>} object representing newely created server
        """

        return None

    def delete_server(self, id, name):
        """
        A method to remove server. It can delete server both by id and name and access both
        these parameters. Be sure to specify at least one of them. If you specify _both_, id
        will be preferred.

        @type id: integer
        @param id: numeric id of the server to remove
        @type name: string
        @param name: literal name of the server to remove
        @rtype: L{GGServer<GGServer>}
        @return: a L{GGServer<GGServer>} object corresponding to the deleted server
        """
        
        return None


    def power_server(self, id, name, action):
        """A method to start/stop/reboot server.

        You can identify server by either id or name. So you have to specify at least one of these params.
        If you specify both, id would be prefered.

        @param id: numeric id of the server
        @type id: string
        @param name: liternal name of the server
        @type name: string
        @param action: name of the operation to perform on the server. Possible operations are:

            1. "on" - power server on
            2. "off" - turns server off (not gracefully)
            3. "restart" - reboots server
        @type action: string
        
        @rtype: L{GGServer<GGServer>}
        @return: a L{GGServer<GGServer>} object representing a server operation was pefrormed on
        """

        return None

    def get_billing(self):
        """
        A method that returns account billing information

        @rtype: dict
        @return: dict with various billing information
        """

        return None
