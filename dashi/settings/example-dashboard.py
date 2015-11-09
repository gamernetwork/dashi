DASHBOARD_UNIT_SIZE = 200

DASHBOARD_BLOCKS = (
#    { 'id': 3, 'module': 'dashi.blocks.Dummy', 'conf': { 'title': 'Nothing', 'width' : 1, 'height' : 1, } },
#    { 'id': 1, 'module': 'dashi.blocks.Scratch', 'width' : 2, 'height' : 2, 'conf': { 'title': 'Contacts', 'update_ms' : 30000, 'filename': 'scratch/contacts.txt' } },
    { 'id': 5, 'module': 'dashi.blocks.Graph', 'width' : 4, 'height' : 2, 
        'conf': { 'title': 'Realtime Traffic', 'update_ms' : 1000, 'redis_connection': { 'host': 'localhost', 'port': 6379, },
            'range': 100,
            'threshold_error' : 2000, 'threshold_warning' : 1000, 
            'data': [
                { 'label' : 'PV/sec', 'memcache_key': 'pageviews/sec' },
                { 'label' : 'BW (mbit)', 'memcache_key': 'bandwidth/sec' },
                { 'label' : 'Monkeys', 'memcache_key': 'monkeys/sec' },
            ]
        }
    },
    { 'id': 9, 'module': 'dashi.blocks.Graph', 'width' : 4, 'height' : 2, 
        'conf': { 'title': 'Appserver Load', 'update_ms' : 1000, 'redis_connection': { 'host': 'localhost', 'port': 6379, },
            'range': 50,
            'threshold_error' : 2000, 'threshold_warning' : 1000, 
            'data': [
                { 'label' : 'bodie', 'memcache_key': 'loadavg/avon' },
                { 'label' : 'bunk', 'memcache_key': 'loadavg/bunk' },
                { 'label' : 'bunny', 'memcache_key': 'loadavg/bunny' },
                { 'label' : 'prez', 'memcache_key': 'loadavg/prez' },
                { 'label' : 'weebey', 'memcache_key': 'loadavg/weebey' },
            ]
        }
    },
    { 'id': 10, 'module': 'dashi.blocks.Graph', 'width' : 4, 'height' : 2, 
        'conf': { 'title': 'Appserver Connections', 'update_ms' : 1000, 'redis_connection': { 'host': 'localhost', 'port': 6379, },
            'range': 20,
            'threshold_error' : 2000, 'threshold_warning' : 1000, 
            'data': [
                { 'label' : 'bodie', 'memcache_key': 'conn/avon' },
                { 'label' : 'bunk', 'memcache_key': 'conn/bunk' },
                { 'label' : 'bunny', 'memcache_key': 'conn/bunny' },
                { 'label' : 'prez', 'memcache_key': 'conn/prez' },
                { 'label' : 'weebey', 'memcache_key': 'conn/weebey' },
            ]
        }
    },
    { 'id': 7, 'module': 'dashi.blocks.Ticker',
        'width' : 1, 'height' : 1,
        'conf': { 'title': 'PHP Warnings', 'update_ms' : 10000, 'redis_connection': { 'host': 'localhost', 'port': 6379, },
            'data': { 'memcache_key': 'php_warnings/sec', 'unit' : '/sec', 'threshold_error' : 700, 'threshold_warning' : 400, 'low_threshold_error' : 0, 'low_threshold_warning' : 0 },
        }
    },
    { 'id': 8, 'module': 'dashi.blocks.Ticker',
        'width' : 1, 'height' : 1,
        'conf': { 'title': 'PHP Errors', 'update_ms' : 10000, 'redis_connection': { 'host': 'localhost', 'port': 6379, },
            'data': { 'memcache_key': 'php_errors/sec', 'unit' : '/sec', 'threshold_error' : 700, 'threshold_warning' : 400, 'low_threshold_error' : 0, 'low_threshold_warning' : 0 },
        }
    },
        
)

DASHBOARD_COLOURS = {
    'error' : 'red',
    'warning' : 'orange',
    'ok' : 'green',
    'default' : 'white',
    'label' : 'white',
    'title' : '#c0c0c0',
}

