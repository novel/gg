#!/usr/bin/env python


"""
GoGridManager is a Python module which implements an interface to the GoGrid API.
It uses CSV mode and therefore doesn't need external libs (that would be needed if it used
json) and the code is compact (it would be hard to keep it as small as now if it used xml).
The module has been tested with CPython 2.5 and CPython 2.6 and works fine. Jython should
work too, but it wasn't tested as frequently as CPython.

@note: Small comment on the datatypes. As you probably know already, GoGrid server
can be identified by either numeric id of it's name. Actually, __actually__, it is possible to
have to servers with the same name, however numeric id is always unique. But in most of cases if
you are sure that you don't use same names for your servers, it might be more convenient to search
servers by name. You will notice that some methods accepts both id and name, however type for id is
string. Don't get confused: type is string to avoid non-needed type conversion, as id is stored as
string in CSV, like all other fields as well.

@author: Roman Bogorodskiy
@contact: bogorodskiy@gmail.com
"""

from random import choice
from GoGridClient import GoGridClient

class GGIp:
    """
    Class representing IP addresses. In GoGrid API, IP address can be generally used in a two ways:

        1. As an address attached to the server

        2. As an item of the address pool

    IP addresses are of two types:

        1. Private

        2. Public

    Private addresses are used for connecting to cloud storage (as it's not available from the world)
    and for internal connections between GoGrid servers and ServePath servers for example. You cannot
    create GoGrid servers with the private IP.

    Public IPs are just IPs assigned to the servers when they're getting created.
    
    @author: Roman Bogorodskiy
    @contact: bogorodskiy@gmail.com
    """

    def __init__(self, tokens):
        """
        Constructor.

        @type tokens: string
        @param tokens: comma-separated list of items as recieved from GoGrid API response

        @note: you most likely don't want to construct GGIp objects yourself, normally they will
        be returned by various methods from L{GoGridManager<GoGridManager>}.
        """

        self.id = tokens[0]
        """
        @ivar: internal id of the IP address
        @type: string
        """
        self.ip = tokens[1]
        """
        @ivar: actuall IP address in dot-decimal notation (192.168.0.1 for example)
        @type: string
        """
        self.subnet = tokens[2]
        """
        @ivar: subnet given IP address belongs to
        @type: string
        """
        self.public = (tokens[3] == "true")
        """
        @ivar: true if the address is public, false in case if it's from private network
        @type: boolean
        """

    #def __init__(self, id, ip, subnet, public):
    #    self.id = id
    #    self.ip = ip
    #    self.subnet = subnet
    #    self.public = public

    def __str__(self):
        return "ip = %s (id = %s, subnet = %s, public: %s)" % (self.ip, self.id, self.subnet, self.public)

class GGServer:
    """
    Class representing GoGrid server instance.
    """

    def __init__(self, tokens):
        """
        Constructor.

        @type tokens: string
        @param tokens: comma-separated list of items as recieved from GoGrid API response
        
        @note: you most likely don't want to construct GGServer objects yourself, normally they will
        be returned by various methods from L{GoGridManager<GoGridManager>}.
        """
        self.id = tokens[0]
        """
        @ivar: id of the server
        @type: string
        """
        self.name = tokens[1]
        """
        @ivar: name of the server
        @type: string
        """
        self.descr = tokens[2]
        """
        @ivar: user's description of the server, might be blank
        @type: string
        """
        self.ip = GGIp([tokens[3], tokens[4], tokens[5], tokens[6]])
        """
        @ivar: address information for the server
        @type: L{GGIp<GGIp>}
        """
        self.state = tokens[20]
        """
        @ivar: name of the current server state. 

        You can get a list of possible values using gg-lookup tool::

            gg-lookup server.state

        @type: string
        """ 

    def __str__(self):
        return "server %s (id = %s, descr = %s, state = %s, ip = %s)" % (self.name, 
                self.id, self.descr, self.state, self.ip.ip)

class GGImage:
    """
    Class representing GoGrid images. Images are generally various OS temples, e.g. centos5x with Apache, centos5x
    with PostgreSQL, etc
    """

    def __init__(self, tokens):
        """
        Constructor.

        @type tokens: string
        @param tokens: comma-separated list of items as recieved from GoGrid API response

        @note: you most likely don't want to construct GGImage objects yourself, normally they will
        be returned by various methods from L{GoGridManager<GoGridManager>}.
        """
        if len(tokens) == 9:
            self.id = tokens[0]
            """
            @ivar: internal id of the image
            @type: string
            """
            self.name = tokens[1]
            """
            @ivar: name of the image
            @type: string
            """
            self.friendlyName = tokens[2]
            """
            @ivar: friendly name of the image
            @type: string
            """
            self.descr = tokens[3]
            """
            @ivar: long descriptive name of the image
            @type: string
            """
            self.location = tokens[4]
            """
            @ivar: location of the image
            @type: string
            """
            self.isActive = (tokens[5] == "true")
            """
            @ivar: true if image is active, false otherwise
            @type: boolean
            """
            self.isPublic = (tokens[6] == "true")
            """
            @ivar: true if image is active, false otherwise
            @type: boolean
            """
            self.createdTime = tokens[7]
            """
            @ivar: creation time of an image
            @type: string
            """
            self.updatedTime = tokens[8]
            """
            @ivar: update time of an image
            @type: string
            """
        else:
            self.id = tokens[0]
            self.name = tokens[1]

    def __str__(self):
        return "image %s (id = %s)" % (self.name, self.id)

class GGPassword:
    "Class representing password instance."

    def __init__(self, tokens):
        self.id = tokens[0]
        """
        @ivar: internal numeric id of the password object
        @type: string
        """
        self.server = GGServer(tokens[2:])
        """
        @ivar: points to the corresponding L{GGServer<GGServer>} object
        @type: L{GGServer<GGServer>}
        """
        self.username = tokens[31]
        """
        @ivar: username
        @type: string
        """
        self.password = tokens[32]
        """
        @ivar: password
        @type: string
        """

    def __str__(self):
        return "%s:%s@%s (id = %s)" % (self.username, self.password, self.server.ip.ip, self.id)

class GoGridManager:
    """
    The main class to accessing GoGrid API methods.
    """

    def __init__(self, key='', secret=''):
        """Constructor.

        key and secret params are optional. If you will specify both of them, GoGridManager
        will use these credentials to use GoGrid API. If at least one of the params will be
        missing, it will try to use configuration file. Configuration file is located
        at ~/.ggrc and contains only one line of the format: "api_key:secret". You can get more
        details on obtaining GoGrid API key at the GoGrid wiki.
        """
        self.gogrid_client = GoGridClient(key, secret)

    def find_image_by_name(self, name):
        """@deprecated: not elegant, use filter on the get_images()"""
        for image in self.get_image_list():
            if name == image[1]:
                return image

######################
######################

    def get_ips(self, type="all", state=None):
        """
        Returns a list of IPs available for the current account.

        @type type: string
        @param type: A type of the IP address. Can be "Public", "Private" and "All" which means both private and public are OK
        @type state: string
        @param state: A state of the IP, can be one of "Assigned" or "Unassigned". By default returns all IPs
        @rtype: list
        @return: a list of L{GGIp<GGIp>} objects matching the query
        """

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
        """
        Returns a list of servers currently deployed

        @rtype: list
        @return: a list of L{GGServer<GGServer>} objects representing currently running servers
        """

        param_dict = {} 

        data = self.gogrid_client.sendAPIRequest("grid/server/list", param_dict)

        data = data.splitlines()
        del data[0:2]

        return map(lambda item: GGServer(item.split(",")), data)

    def get_images(self):
        """
        Returns a list of available server images (i.e. Operating System templates)
        
        @rtype: list
        @return: a list of L{GGImage<GGImage>} objects representing currently available OS templates
        """
        data = self.gogrid_client.sendAPIRequest("grid/image/list", {}).splitlines()

        del data[0:2]
        return map(lambda item: GGImage(item.split(",")), data)

    def get_passwords(self):
        """
        Returns a list of passwords for the currently running servers

        @rtype: list
        @return: a list of L{GGPassword<GGPassword>} objects containing passwords for the currently running servers
        """
        data = self.gogrid_client.sendAPIRequest("support/password/list", {}).splitlines()

        del data[0:2]
        return map(lambda item: GGPassword(item.split(",")), data)

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

        param_dict = {"name": name, "image": image, "ram": ram, "ip": ip}

        if descr is not None:
            param_dict["description"] = descr

        response = self.gogrid_client.sendAPIRequest("grid/server/add", param_dict).splitlines()

        del response[0:2]

        return GGServer(response[0].split(","))

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
        if id is not None:
            param_dict = {'id': id}
        else:
            param_dict = {'name': name} 

        # XXX to raise an exception if both fields are None
        
        response = self.gogrid_client.sendAPIRequest("grid/server/delete", param_dict).splitlines()

        del response[0:2]

        return GGServer(response[0].split(","))


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
        if id is not None:
            param_dict = {"id": id}
        else:
            param_dict = {"name": name}

        param_dict["power"] = action

        response = self.gogrid_client.sendAPIRequest("grid/server/power", param_dict).splitlines()

        del response[0:2]

        return GGServer(response[0].split(","))

    def get_billing(self):
        """
        A method that returns account billing information

        @rtype: dict
        @return: dict with various billing information
        """
        response = self.gogrid_client.sendAPIRequest("myaccount/billing/get", {}).splitlines()

        del response[0]
        keys = response[0][2:].split(",")
        values = response[1].split(",")

        return dict(zip(keys, values))

######################
######################
    def get_free_public_ips(self):
        """
        Returns a list of currenty available public ips
        """

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
