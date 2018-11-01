from django.conf import settings
import sys
from django.template import RequestContext
from django.template import Template
from django.shortcuts import *
from django.template.loader import render_to_string
import random
import re
from sources import Elasticsearch_Source, Elasticsearch_Metric, Elasticsearch_Aggregate

class Base( object ):
    def __init__( self, block_id, conf, width=1, height=1 ):
        self.conf = {
            'title': '',
            'update': 5
        }
        self.block_id = block_id
        self.width = width
        self.height = height
        for k in conf.keys():
            self.conf[ k ] = conf[ k ]

        # set ms value for update to avoid a million conversions in the JS
        self.conf['update_ms'] = self.conf['update'] * 1000

        self.context = self.conf
        self.context[ "block_id" ] = block_id
        self.context[ "settings" ] = settings

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

class Table( Base ):
    def __init__(self, block_id, conf, *args, **kwargs):
        super( Table, self ).__init__(block_id, conf, *args, **kwargs)
    def render( self, request ):
        return render_to_string( "blocks/table.html", self.context, RequestContext( request ) )
    @staticmethod
    def render_support_media( request ):
        return render_to_string( "blocks/table_media.html", RequestContext( request ) )

class Elasticsearch_Table( Table, Elasticsearch_Source ):
    def __init__(self, block_id, conf, *args, **kwargs):
        Table.__init__(self, block_id, conf, *args, **kwargs)
        Elasticsearch_Source.__init__(self, conf, *args, **kwargs)
    def update(self, request):
        return self.query()

class Pie( Base ):
    def __init__(self, block_id, conf, *args, **kwargs):
        super( Pie, self ).__init__(block_id, conf, *args, **kwargs)
    def render( self, request ):
        return render_to_string( "blocks/pie.html", self.context, RequestContext( request ) )
    @staticmethod
    def render_support_media( request ):
        return render_to_string( "blocks/pie_media.html", RequestContext( request ) )

class Arch( Base ):
    def __init__(self, block_id, conf, *args, **kwargs):
        super( Arch, self ).__init__(block_id, conf, *args, **kwargs)
    def render( self, request ):
        return render_to_string( "blocks/arch.html", self.context, RequestContext( request ) )
    @staticmethod
    def render_support_media( request ):
        return render_to_string( "blocks/pie_media.html", RequestContext( request ) )

class Elasticsearch_Pie( Pie, Elasticsearch_Source ):
    def __init__(self, block_id, conf, *args, **kwargs):
        Pie.__init__(self, block_id, conf, *args, **kwargs)
        Elasticsearch_Source.__init__(self, conf, *args, **kwargs)
    def update(self, request):
        return self.query()

class Elasticsearch_Arch( Arch, Elasticsearch_Source ):
    def __init__(self, block_id, conf, *args, **kwargs):
        Arch.__init__(self, block_id, conf, *args, **kwargs)
        Elasticsearch_Source.__init__(self, conf, *args, **kwargs)
    def update(self, request):
        return self.query()

class ES_URL_Table( Elasticsearch_Table ):
    def update(self, request):
        r = Elasticsearch_Table.update(self, request)
        def filter_url(url):
            slug = url.rstrip('/').split('/')[-1]
            slug = re.sub('^[0-9\-]*', '', slug)
            slug = re.sub('[0-9\-]*$', '', slug)
            return slug.replace('-', ' ')
        return [ (filter_url(u),c,) for (u,c) in r ]
        
import time
class Graph( Base ):
    def __init__( self, block_id, conf, *kwargs ):
        super( Graph, self ).__init__( block_id, conf, *kwargs  )
    def update( self, request ):
        if( settings.FAKE ):
            r = { 'vals': [ ( int( time.time() ), int( str( datetime.datetime.now().microsecond * random.random() )[:3] ) * (i+1)/4 + (i*100) ) for i,j in enumerate( self.conf[ "data" ] ) ] }
            return r
    def render( self, request ):
        return render_to_string( "blocks/graph.html", self.context, RequestContext( request ) )
    @staticmethod
    def render_support_media( request ):
        return render_to_string( "blocks/graph_media.html", RequestContext( request ) )

class Elasticsearch_Graph( Graph, Elasticsearch_Metric ):
    def __init__(self, block_id, conf, *args, **kwargs):
        Graph.__init__(self, block_id, conf, *args, **kwargs)
        Elasticsearch_Metric.__init__(self, conf, *args, **kwargs)
    def update(self, request):
        c = self.query()
        r = { 'vals': [[ int( time.time() ), c ],] } # Vals is a list within a list containing time and count
        return r

class Ticker( Base ):
    """Shows a value and optional alarm status"""
    def __init__( self, block_id, conf, *kwargs ):
        super( Ticker, self ).__init__( self, block_id, conf, *kwargs )
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

class Elasticsearch_Ticker( Ticker, Elasticsearch_Metric):
    def __init__(self, block_id, conf, *args, **kwargs):
        # TODO fix Ticker init so it doesn't make a redis store
        Base.__init__( self, block_id, conf, *kwargs )
        Elasticsearch_Metric.__init__(self, conf, *args, **kwargs)
    def update(self, request):
        c = self.query()
        return { 'value': c, 'status': 'OK' }

class Elasticsearch_AggregateTicker( Ticker, Elasticsearch_Aggregate):
    def __init__(self, block_id, conf, *args, **kwargs):
        # TODO fix Ticker init so it doesn't make a redis store
        Base.__init__( self, block_id, conf, *kwargs )
        Elasticsearch_Aggregate.__init__(self, conf, *args, **kwargs)
    def update(self, request):
        c = self.query()
        return { 'value': c, 'status': 'OK' }

class Scratch( Base ):
    def update( self, request ):
        if self.conf.has_key("filename"):
            return file( self.conf[ "filename" ] ).read()
        elif self.conf.has_key("content"):
            return self.conf["content"]
    def render( self, request ):
        self.context[ "content" ] = self.update( request )
        return render_to_string( "blocks/scratch.html", self.context, RequestContext( request ) )

class ClientInfo( Base ):
    def update( self, request ):
	return request.META.get('REMOTE_ADDR')
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
    #print bc_class
    blocks.append( bc_class( bid, bc[ "conf" ] ) )

