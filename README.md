Dashi - A flexible dashboard for serious stuff
==============================================

Modular and configurable, simply reads data from redis keys - it's up to you to define what they are.

Modules
-------

 - Activity graphs (numbers over time)
 - Tickers (arbitrary numbers)
 - Nagios service status summary matrix (overall cluster health)
 - Overall THREAT LEVEL (i.e. is everything cool?)

Deps
----

This is what I've been running with, but YMMV:

```
env/bin/pip freeze -l
Django==1.5.1
django-dajax==0.9.2
django-dajaxice==0.5.5
python-memcached==1.48
redis==2.4.13
```

Setup
-----

Copy

`dashi/settings/example-instance.py` to `dsahi/settings/instance.py`
`dashi/settings/example-dashboard.py` to `dsahi/settings/dashboard.py`

...and customise both (should be fairly self documenting).

Some settings you can change:

  - `FAKE` - use fake data instead of connecting to redis, which can help when setting up.

Running
-------

To run on `localhost:8080` just do a standard a Django dev server:

```
python manage.py runserver
```

No wsgi adapter provided, but that should be fairly easy.

Notes
-----

Uses code taken from Balbec project https://github.com/mkulke/balbec for parsing Nagios status files.
