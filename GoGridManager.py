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

from GoGridClient import GoGridClient
from random import choice
import xml.dom.minidom

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

    def __init__(self):
        """
        Constructor.

        @type tokens: string
        @param tokens: comma-separated list of items as recieved from GoGrid API response

        @note: you most likely don't want to construct GGIp objects yourself, normally they will
        be returned by various methods from L{GoGridManager<GoGridManager>}.
        """

        self.id = ''
        """
        @ivar: internal id of the IP address
        @type: string
        """
        self.ip = ''
        """
        @ivar: actuall IP address in dot-decimal notation (192.168.0.1 for example)
        @type: string
        """
        self.subnet = ''
        """
        @ivar: subnet given IP address belongs to
        @type: string
        """
        self.public = ''
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

    def __init__(self):
        """
        Constructor.

        @type tokens: string
        @param tokens: comma-separated list of items as recieved from GoGrid API response
        
        @note: you most likely don't want to construct GGServer objects yourself, normally they will
        be returned by various methods from L{GoGridManager<GoGridManager>}.
        """

        self.id = ''
        """
        @ivar: id of the server
        @type: string
        """
        self.name = ''
        """
        @ivar: name of the server
        @type: string
        """
        self.descr = ''
        """
        @ivar: user's description of the server, might be blank
        @type: string
        """
        self.ip = GGIp()
        """
        @ivar: address information for the server
        @type: L{GGIp<GGIp>}
        """
        self.state = ''
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

    def __init__(self):
        """
        Constructor.

        @type tokens: string
        @param tokens: comma-separated list of items as recieved from GoGrid API response

        @note: you most likely don't want to construct GGImage objects yourself, normally they will
        be returned by various methods from L{GoGridManager<GoGridManager>}.
        """

        pass
#        if len(tokens) == 11:
#            self.id = tokens[2]
#            """
#            @ivar: internal id of the image
#            @type: string
#            """
#            self.name = tokens[3]
#            """
#            @ivar: name of the image
#            @type: string
#            """
#            self.friendlyName = tokens[4]
#            """
#            @ivar: friendly name of the image
#            @type: string
#            """
#            self.descr = tokens[5]
#            """
#            @ivar: long descriptive name of the image
#            @type: string
#            """
#            self.location = tokens[6]
#            """
#            @ivar: location of the image
#            @type: string
#            """
#            self.isActive = (tokens[7] == "true")
#            """
#            @ivar: true if image is active, false otherwise
#            @type: boolean
#            """
#            self.isPublic = (tokens[8] == "true")
#            """
#            @ivar: true if image is active, false otherwise
#            @type: boolean
#            """
#            self.createdTime = tokens[9]
#            """
#            @ivar: creation time of an image
#            @type: string
#            """
#            self.updatedTime = tokens[10]
#            """
#            @ivar: update time of an image
#            @type: string
#            """
#        else:
#            self.id = tokens[0]
#            self.name = tokens[1]

    def __str__(self):
        return "image %s (id = %s)" % (self.friendlyName, self.id)

class GGPassword:
    "Class representing password instance."

#    def __init__(self, tokens):
#        self.id = tokens[0]
#        """
#        @ivar: internal numeric id of the password object
#        @type: string
#        """
#        self.server = GGServer(tokens[1:])
#        """
#        @ivar: points to the corresponding L{GGServer<GGServer>} object
#        @type: L{GGServer<GGServer>}
#        """
#        self.username = tokens[31]
#        """
#        @ivar: username
#        @type: string
#        """
#        self.password = tokens[32]
#        """
#        @ivar: password
#        @type: string
#        """

    def __str__(self):
        return "%s:%s@%s (id = %s)" % (self.username, self.password, self.server.ip.ip, self.id)

class GGJob:
    hist = []
    
    def __init__(self):
        pass

class GGJobHistory:
    id = ''
    state = ''
    note = ''
    updatedon = ''

class GoGridManager:
    """
    The main class to accessing GoGrid API methods.
    """

    def __init__(self, key='', secret='', account="default"):
        """Constructor.

        key and secret params are optional. If you will specify both of them, GoGridManager
        will use these credentials to use GoGrid API. If at least one of the params will be
        missing, it will try to use configuration file. Configuration file is located
        at ~/.ggrc and contains only one line of the format: "api_key:secret". You can get more
        details on obtaining GoGrid API key at the GoGrid wiki.
        """
        self.gogrid_client = GoGridClient(key, secret, account=account)

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

        doc = xml.dom.minidom.parseString(data)

        ips = []
        object_nodes = doc.getElementsByTagName("object")

        for obj in object_nodes:
            if "ip" == obj.getAttribute("name"):
                ips.append(self._parse_ip_object(obj))

        return ips

    def get_servers(self):
        """
        Returns a list of servers currently deployed

        @rtype: list
        @return: a list of L{GGServer<GGServer>} objects representing currently running servers
        """

        param_dict = {} 

        data = self.gogrid_client.sendAPIRequest("grid/server/list", param_dict)

        doc = xml.dom.minidom.parseString(data)

        servers = []
        object_nodes = doc.getElementsByTagName("object")

        for obj in object_nodes:
            if "server" == obj.getAttribute("name"):
                servers.append(self._parse_server_object(obj))

        return servers

    def get_images(self):
        """
        Returns a list of available server images (i.e. Operating System templates)
        
        @rtype: list
        @return: a list of L{GGImage<GGImage>} objects representing currently available OS templates
        """
        data = self.gogrid_client.sendAPIRequest("grid/image/list", {})

        doc = xml.dom.minidom.parseString(data)
   
        images = []
        object_nodes = doc.getElementsByTagName("object")

        for obj in object_nodes:
            if "serverimage" != obj.getAttribute("name"):
                continue

            images.append(self._parse_serverimage_object(obj))

        return images

    def get_passwords(self):
        """
        Returns a list of passwords for the currently running servers

        @rtype: list
        @return: a list of L{GGPassword<GGPassword>} objects containing passwords for the currently running servers
        """
        data = self.gogrid_client.sendAPIRequest("support/password/list", {})

        doc = xml.dom.minidom.parseString(data)

        passwords = []
        object_nodes = doc.getElementsByTagName("object")

        for obj in object_nodes:
            if "password" == obj.getAttribute("name"):
                passwords.append(self._parse_password_object(obj))

        return passwords

    def get_job(self, id):
        """Returns information about single job."""

        data = self.gogrid_client.sendAPIRequest("grid/job/get", {"id": id})

        doc = xml.dom.minidom.parseString(data)

        return self._parse_job_object(doc.getElementsByTagName("object")[0])

    def get_jobs(self, num_items=20):
        """Returns a list of jobs"""

        data = self.gogrid_client.sendAPIRequest("grid/job/list", 
            {"num_items": num_items})

        doc = xml.dom.minidom.parseString(data)

        jobs = []
        object_nodes = doc.getElementsByTagName("object")

        for obj in object_nodes:
            if "job" == obj.getAttribute("name"):
                jobs.append(self._parse_job_object(obj))

        return jobs

    def save_image(self, name, server, descr=None):
        """
        A method to save sendbox image to cloud storage
        to be able to use it as a server image.

        @type name: string
        @param name: the friendly name of the  server image to be saved 
        @type server: instace to be used as an image. You can provide either
         symbolic name or numeric server id
        @type descr: string
        @param descr: optional literal description of the image
        """

        param_dict = {"friendlyName": name, "server": server}

        if descr is not None:
            param_dict["description"] = descr

        response = self.gogrid_client.sendAPIRequest("grid/image/save", param_dict)

        doc = xml.dom.minidom.parseString(response)

        return self._parse_serverimage_object(doc.getElementsByTagName("object")[0])

    def add_server(self, name, image, ram, ip, descr=None, sandbox=False):
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
        
        if sandbox:
            param_dict['isSandbox'] = "true"


        response = self.gogrid_client.sendAPIRequest("grid/server/add", param_dict)

        doc = xml.dom.minidom.parseString(response)
        
        return self._parse_server_object(doc.getElementsByTagName("object")[0])

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
        
        response = self.gogrid_client.sendAPIRequest("grid/server/delete", param_dict)

        doc = xml.dom.minidom.parseString(response)
        
        return self._parse_server_object(doc.getElementsByTagName("object")[0])

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

        response = self.gogrid_client.sendAPIRequest("grid/server/power", param_dict)

        doc = xml.dom.minidom.parseString(response)
        
        return self._parse_server_object(doc.getElementsByTagName("object")[0])

    def get_billing(self):
        """
        A method that returns account billing information

        @rtype: dict
        @return: dict with various billing information
        """
        response = self.gogrid_client.sendAPIRequest("myaccount/billing/get", {})

        doc = xml.dom.minidom.parseString(response)

        fields = ["startDate", "endDate", 
                "memoryAllotment", "memoryInUse", "memoryAccrued",
                "memoryOverage", "memoryOverageCharge",
                "transferAllotment", "transferAccrued",
                "transferOverage", "transferOverageCharge"]
        result = {}

        for node in doc.getElementsByTagName("object")[0].childNodes:
            if node.ELEMENT_NODE == node.nodeType:
                if "attribute" == node.nodeName:
                    name = node.getAttribute("name")
                    
                    if name in fields:
                        result[name] = self._get_text(node)

        return result

    def _get_text(self, object):
        text = []
        for child in object.childNodes:
            if child.TEXT_NODE == child.nodeType:
                text.append(child.data)

        return ''.join(text)

    def _parse_serverimage_object(self, object):
        image = GGImage()

        mappings = {'id': 'id',
                'name': 'name',
                'friendlyName': 'friendlyName',
                'description': 'descr',
                'location': 'location',
                'createdTime': 'createdTime',
                'updatedTime': 'updatedTime'}
        boolean_mappings = {'isActive': 'isActive',
                'isPublic': 'isPublic'}

        for child in object.childNodes:
            if child.ELEMENT_NODE == child.nodeType:
                if "attribute" == child.nodeName:
                    name, value = child.getAttribute("name"), self._get_text(child)

                    if name in mappings:
                        setattr(image, mappings[name], value)
                    elif name in boolean_mappings:
                        setattr(image, boolean_mappings[name], value == "true")

        return image

    def _parse_ip_object(self, object):
        ip = GGIp()

        fields = ['id', 'ip', 'subnet']
        boolean_fields = ['public']

        for child in object.childNodes:
            if child.ELEMENT_NODE == child.nodeType:
                if "attribute" == child.nodeName:
                    name, value = child.getAttribute("name"), self._get_text(child)

                    if name in fields:
                        setattr(ip, name, value)
                    elif name in boolean_fields:
                        setattr(ip, name, value == "true")

        return ip

    def _parse_server_object(self, object):
        server = GGServer()

        mappings = {'id': 'id',
                'name': 'name',
                'description': 'desc'}
        boolean_mappings = {'isSandbox': 'isSandbox'}

        for child in object.childNodes:
            if child.ELEMENT_NODE == child.nodeType:
                if "attribute" == child.nodeName:
                    name = child.getAttribute("name")

                    if name in mappings:
                        setattr(server, mappings[name], self._get_text(child))
                    elif name in boolean_mappings:
                        setattr(server, boolean_mappings[name], 
                                "true" == self._get_text(child))
                    elif "ip" == name:
                        server.ip = self._parse_ip_object(child.childNodes[0])
                    elif "image" == name:
                        server.image = self._parse_serverimage_object(child.childNodes[0])
                    elif "state" == name:
                         for grandchild in child.childNodes[0].childNodes:
                             if "attribute" == grandchild.nodeName:
                                 if "name" == grandchild.getAttribute("name"):
                                     server.state = self._get_text(grandchild)
                    
        return server

    def _parse_password_object(self, object):
        password = GGPassword()

        mappings = {'id': 'id',
                'username': 'username',
                'password': 'password'}


        for child in object.childNodes:
            if child.ELEMENT_NODE == child.nodeType:
                name = child.getAttribute("name")

                if name in mappings:
                    setattr(password, mappings[name], self._get_text(child))
                elif "server" == name:
                    password.server = self._parse_server_object(child.childNodes[0])

        if not hasattr(password, 'server'):
            password.server = GGServer()

        return password

    def _parse_job_object(self, object):
        job = GGJob()

        fields = ["id", "owner", "attempts"]
        hist_mappings = {"name": "state",
                "note": "note",
                "description": "descr",
                "updatedon": "updatedon"}

        for child in object.childNodes:
            if child.ELEMENT_NODE == child.nodeType:
                if "attribute" == child.nodeName:
                    name = child.getAttribute("name")
                    
                    if name in fields:
                        setattr(job, name, self._get_text(child))
                    elif "command" == name:
                        for grandchild in child.childNodes[0].childNodes:
                            if "attribute" == grandchild.nodeName:
                                if "description" == grandchild.getAttribute("name"):
                                    job.descr = self._get_text(grandchild)
                    elif "history" == name:
                        job_history_objects = child.getElementsByTagName("object")

                        for job_history_obj in job_history_objects:
                            if "job_history" != job_history_obj.getAttribute("name"):
                                continue

                            gg_job_history = GGJobHistory()

                            if "job_history" == job_history_obj.getAttribute("name"):
                                for job_history_child in job_history_obj.childNodes:
                                    if job_history_child.ELEMENT_NODE == job_history_child.nodeType:
                                        name = job_history_child.getAttribute("name")

                                        if name in hist_mappings:
                                            setattr(gg_job_history, hist_mappings[name], 
                                                    self._get_text(job_history_child))
                                        elif "state" == name:
                                            # deeper and deeper
                                            for state_attr in job_history_child.childNodes[0].childNodes:
                                                if "attribute" == state_attr.nodeName:
                                                    #print state_attrs.getAttribute("name")
                                                    name = state_attr.getAttribute("name")
                                                    if name in hist_mappings:
                                                        setattr(gg_job_history, 
                                                                hist_mappings[name],
                                                                self._get_text(state_attr))

                            job.hist.append(gg_job_history)

        return job
