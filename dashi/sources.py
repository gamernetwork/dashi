from elasticsearch import Elasticsearch
import certifi
import logging
from cache_memoize import cache_memoize
import textwrap

# for tidy logging
wrapper = textwrap.TextWrapper( width=40, replace_whitespace=True, initial_indent = '    ', subsequent_indent = '        ')

logger = logging.getLogger('django')

ERR = '#ERR'

class Source(object):
    # should we just make types implied?
    # it doesn't really matter if somebody uses a type incorrectly
    # it's important to be able to iterate and index a val quickly
    # e.g. for each r in d: print r['key'], etc
    """
        {
            keys: { 'a': { label: 'A', type: int},... }
            data: [
                {
                    'a': val,
                    'b': val
                }
            ]
    """
    def __init__( self, conf, *args, **kwargs ):
        pass

from hashlib import md5
import pprint

def sig_gen(*args):
    # suppress 'self' from cache key - see https://github.com/peterbe/django-cache-memoize#args_rewrite
    # the args_rewrite stuff does not actually handle kwargs, just positional
    # if we could use kwargs, I would remove the index names from cache key too
    return ""

def hitme(*args, **kwargs):
    logger.debug( "HIT" )
    logger.debug("\n".join(wrapper.wrap(pprint.pformat(kwargs['body']).strip())))

def missme(*args, **kwargs):
    logger.debug( "MISS" )
    logger.debug("\n".join(wrapper.wrap(pprint.pformat(kwargs['body']).strip())))


class CachedElasticsearch(Elasticsearch):
    """
        Uses a local cache (whatever is configured in Django cache backend settings)
    """
    @cache_memoize(60, args_rewrite=sig_gen, hit_callable=hitme, miss_callable=missme)
    def search(self, *args, **kwargs):
        kwargs.update({'request_cache':True})
        return super(CachedElasticsearch, self).search(*args, **kwargs)

class Redis_Source( Source ):
    def __init__( self, conf, *args, **kwargs ):
        self.datastore = redis.StrictRedis( conf[ "redis_connection" ][ "host" ], conf[ "redis_connection" ][ "port" ], db=0)

class Elasticsearch_Source( Source ):
    def __init__( self, conf, *args, **kwargs ):
        super( Elasticsearch_Source, self ).__init__(conf, *args, **kwargs)
        self.client = CachedElasticsearch([ self.conf['data']['host'], ], verify_certs=False)
    def query(self):
        q = self.conf['data']['query']
        if callable(q):
            q = q()
        logger.debug(q)
        res = self.client.search(
            index = self.conf['data']['index'](),
            body = q
        )
        return [ r.values() for r in res['aggregations'][self.conf['data']['use']]['buckets'] ]

class Elasticsearch_Split( Elasticsearch_Source ):
    """A table with a single key_metric column, for which we calculate proportions
    as a new 'split' key
    """
    def __init__( self, conf, *args, **kwargs ):
        super( Elasticsearch_Split, self ).__init__(conf, *args, **kwargs)

    def query(self):
        data = super( Elasticsearch_Split, self ).query()
        try:
            r = self.conf['data']['key_metric']
            # calc sum
            s = 0
            for d in r['data']:
                s += data[key_metric]
            r['keys']['split'] = { 'label': 'Split', 'type': float }
            # set proportion for each row (0.0-1.0)
            d = [ d.update({'split', d[key_metric] / s}) for d in r['data'] ]
        except Exception as e:
            # probably divide by zero TODO catch sep
            logging.error(e)
            # allow dashboard to tolerate these errors by displaying '#ERR'
            return ERR
            
class Elasticsearch_Metric( Elasticsearch_Source ):
    "A source that returns a single row and value"
    def __init__( self, conf, *args, **kwargs ):
        super( Elasticsearch_Metric, self ).__init__(conf, *args, **kwargs)

    def query(self):
        q = self.conf['data']['query']
        if callable(q):
            q = q()
        logger.debug(q)
        res = self.client.search(
            index = self.conf['data']['index'](),
            body = q
        )
        try:
            return res['hits']['total']

        except Exception as e:
            logging.error(e)
            # allow dashboard to tolerate these errors by displaying '#ERR'
            return ERR
        
class Elasticsearch_Aggregate( Elasticsearch_Source ):
    "A source that returns a single row and value"
    def __init__( self, conf, *args, **kwargs ):
        super( Elasticsearch_Aggregate, self ).__init__(conf, *args, **kwargs)
    def query(self):
        q = self.conf['data']['query']
        if callable(q):
            q = q()
        logger.debug(q)
        res = self.client.search(
            index = self.conf['data']['index'](),
            body = q
        )
        return res['aggregations'][self.conf['data']['use']]['value']
    
