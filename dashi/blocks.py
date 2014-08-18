from django.conf import settings
import sys
from django.template import RequestContext
from django.template import Template
from django.shortcuts import *
from django.template.loader import render_to_string
import random
class Base( object ):
    def __init__( self, block_id, conf, width=1, height=1 ):
        self.conf = {
            'title': '',
            'update_ms': 5000
        }
        self.block_id = block_id
        self.width = width
        self.height = height
        for k in conf.keys():
            self.conf[ k ] = conf[ k ]
        self.context = self.conf
        self.context[ "block_id" ] = block_id
        self.context[ "width" ] = width
        self.context[ "height" ] = height
    def render( self, request ):
        return ""
    def update( self, request ):
        return ""

    @staticmethod
    def render_support_media( request ):
        return ""

class Dummy( Base ):
    #def __init__( self, block_id, conf ):
    #    super( self, Dummy ).__init__( self, block_id, conf )
    def render( self, request ):
        return render_to_string( "blocks/dummy.html", self.context, RequestContext( request ) )
        
import time
import redis
class Graph( Base ):
    def __init__( self, block_id, conf, *kwargs ):
        super( Graph, self ).__init__( block_id, conf, *kwargs  )
        self.datastore = redis.StrictRedis( conf[ "redis_connection" ][ "host" ], conf[ "redis_connection" ][ "port" ], db=0)
    def update( self, request ):
        if( settings.FAKE ):
            r = { 'vals': [ ( int( time.time() ), int( str( datetime.datetime.now().microsecond * random.random() )[:3] ) * (i+1)/4 + (i*100) ) for i,j in enumerate( self.conf[ "data" ] ) ] }
            return r
        val = self.datastore.get( self.conf[ "datastore_key" ] )
        return { 'x': val[ "time" ], 'y': val[ "count" ] }
    def render( self, request ):
        return render_to_string( "blocks/graph.html", self.context, RequestContext( request ) )
    @staticmethod
    def render_support_media( request ):
        return render_to_string( "blocks/graph_media.html", RequestContext( request ) )

class Ticker( Base ):
    """Shows a value and optional alarm status"""
    def __init__( self, block_id, conf, *kwargs ):
        super( Ticker, self ).__init__( block_id, conf, *kwargs )
        self.datastore = redis.StrictRedis( conf[ "redis_connection" ][ "host" ], conf[ "redis_connection" ][ "port" ], db=0)
    def update( self, request ):
        #val = self.datastore.get( self.conf[ "datastore_key" ] )
        val = int( str( datetime.datetime.now().microsecond * random.random() )[:3] )
        status = "ok"
        if val > self.conf[ "data" ][ "threshold_error" ]:
            status = "error"
        elif val > self.conf[ "data" ][ "threshold_warning" ]:
            status = "warning"
        #print val
        return { 'value': val, 'status': status }
    def render( self, request ):
        return render_to_string( "blocks/ticker.html", self.context, RequestContext( request ) )
    @staticmethod
    def render_support_media( request ):
        return render_to_string( "blocks/ticker_media.html", RequestContext( request ) )

        

import svn.utility
import datetime
class SVNInfo( Base ):
    def update( self, request ):
        cl = svn.utiliy.get_client(self.conf[ "repos" ])
        info = cl.info['commit#revision']
        return info
    def render( self, request ):
        self.context[ "headrev" ] = self.update( request )
        return render_to_string( "blocks/svninfo.html", self.context, RequestContext( request ) )

import urllib2
import xml.etree.ElementTree as ET
class NagiosLEDs( Base ):
    def get_status( self ):
        usock = urllib2.urlopen("http://icinga.th.eurogamer.net/icinga-web/web/api/host/columns[HOST_NAME%7CHOST_CURRENT_STATE])/order(HOST_NAME;DESC)/authkey=aypeeeye/xml")
	xmldoc = ET.parse(usock)
        status = {}
	for host in xmldoc.findall('result'):
		hostInfo = {
		  "HOST_NAME": "",
		  "HOST_CURRENT_STATE": 0,
		  "HOST_IS_PENDING": 0
		}
		for column in host.findall('column'):
        		hostInfo[column.attrib.get("name")] = column.text
		if hostInfo["HOST_CURRENT_STATE"] == "99":
			hostInfo["HOST_CURRENT_STATE"] = 1
		status[ hostInfo["HOST_NAME"] ] = ( hostInfo["HOST_NAME"], int(hostInfo["HOST_CURRENT_STATE"]), 1, )
        status = [ status[s] for s in status.keys() ]
        return status
    def update( self, request ):
        status = self.get_status()
        ret = "<table><tbody>"
        c = 0
        threat = 0
        for s in status:
            if c % self.conf[ "cols" ] == 0:
                ret += "<tr>"
            threat = max(s[1], threat)
            s_img = "error"
            if s[1] == 0:
                s_img = "ok"
            if (s[1] == 1) or (s[1] == 99):
                s_img = "warning"
            ret += "<td class=\"serverstatus%i\"><img src=\"%simg/server_%s.png\" width=\"8\" height=\"8\" /> %s</td>" % ( s[1], settings.STATIC_URL, s_img, s[0] )
            if (c+1) % self.conf[ "cols" ] == 0:
                ret += "<tr>" 
            c += 1
        if (c+1) % self.conf[ "cols" ] == 0:
            ret += "<td></td><tr>" 
        ret += "</tbody></table>"
        return { 'tablehtml': ret, 'threat': threat }
    def render( self, request ):
        self.context[ "statustable" ] = self.update( request )["tablehtml"]
        return render_to_string( "blocks/nagiosleds.html", self.context, RequestContext( request ) )

class Scratch( Base ):
    def update( self, request ):
        return file( self.conf[ "filename" ] ).read()
    def render( self, request ):
        self.context[ "content" ] = self.update( request )
        return render_to_string( "blocks/scratch.html", self.context, RequestContext( request ) )

# single global instance of blocks - bear in mind threading!
blocks = []
bid = 0
for bc in settings.DASHBOARD_BLOCKS:
    bid += 1
    path = bc[ "module" ]
    dot = path.rindex('.')
    bc_module, bc_classname = path[:dot], path[dot+1:]
    __import__(bc_module)
    mod = sys.modules[bc_module]
    bc_class = getattr(mod, bc_classname)
    print bc_class
    blocks.append( bc_class( bid, bc[ "conf" ], bc[ "width" ], bc[ "height" ] ) )

