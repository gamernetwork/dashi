from elasticsearch import Elasticsearch
import certifi
import logging
import redis

logger = logging.getLogger('django')

class Source(object):
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
            index = self.conf['data']['index'],
            body = self.conf['data']['query']
        )
        return [ r.values() for r in res['aggregations'][self.conf['data']['use']]['buckets'] ]

class Elasticsearch_Metric( Elasticsearch_Source ):
    def __init__( self, conf, *args, **kwargs ):
        super( Elasticsearch_Metric, self ).__init__(conf, *args, **kwargs)

    def query(self):
        q = {
          "query": {
            "filtered": {
              "query": {
                "query_string": {
                  "query": self.conf['data']['series'][0]['query'],
                  "analyze_wildcard": True
                }
              },
              "filter": {
                "bool": {
                  "must": [
                    {
                      "range": {
                        "timestamp": {
                          "gte": "now-" + self.conf['data']['window'],
                          "lte": "now",
                        }
                      }
                    }
                  ],
                  "must_not": []
                }
              }
            }
          },
          "aggs": {}
        }
            
        res = self.client.search(
            index = self.conf['data']['index'],
            body = q
        )
        return res['hits']['total']
        
    
