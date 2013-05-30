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

        

import pysvn
import datetime
class SVNInfo( Base ):
    def get_login( realm, username, may_save ):
        return True, username, "7329", True
    def update( self, request ):
        return str( datetime.datetime.now().microsecond )[:5]
        cl = pysvn.Client()
        cl.callback_get_login = self.get_login
        info = cl.info2( self.conf[ "repos" ] )[0]
        return info[ "rev" ].number
    def render( self, request ):
        self.context[ "headrev" ] = self.update( request )
        return render_to_string( "blocks/svninfo.html", self.context, RequestContext( request ) )

from balbec.filebackend import FileBackend
class NagiosLEDs( Base ):
    def get_status( self ):
        fb = FileBackend( self.conf[ "object_cache" ], self.conf[ "status_file" ] )
        status = {}
        for hostgroup in fb.getHostgroups( self.conf[ "hostgroups" ] ):
            hosts = fb.getHosts( hostgroup )
            for host in hosts:
                status[ host.hostname ] = ( host.hostname, host.result.status, host.result.output, )
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
            if s[1] == 1:
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

