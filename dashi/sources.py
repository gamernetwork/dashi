from elasticsearch import Elasticsearch
import certifi
import logging
import redis

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

class Redis_Source( Source ):
    def __init__( self, conf, *args, **kwargs ):
        self.datastore = redis.StrictRedis( conf[ "redis_connection" ][ "host" ], conf[ "redis_connection" ][ "port" ], db=0)

class Elasticsearch_Source( Source ):
    def __init__( self, conf, *args, **kwargs ):
        super( Elasticsearch_Source, self ).__init__(conf, *args, **kwargs)
        self.client = Elasticsearch([ self.conf['data']['host'], ], verify_certs=False)
    def query(self):
        logger.debug(self.conf['data']['query'])
        res = self.client.search(
            index = self.conf['data']['index'](),
            body = self.conf['data']['query']
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
        logger.debug(self.conf['data']['query'])
        res = self.client.search(
            index = self.conf['data']['index'](),
            body = self.conf['data']['query']
        )
        try:
            return res['hits']['total']

        except Exception as e:
            logging.error(e)
            # allow dashboard to tolerate these errors by displaying '#ERR'
            return ERR
        
    
