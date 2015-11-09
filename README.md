# Dashi - A flexible dashboard for serious stuff

Modular and configurable, simply reads data from redis keys - it's up to you to define what they are.

## Modules

 - Activity graphs (numbers over time) - uses Highcharts.js http://www.highcharts.com/docs
 - Tickers (arbitrary numbers)
 - Nagios service status summary matrix (overall cluster health)
 - Overall THREAT LEVEL (i.e. is everything cool?)

## Setup

Pop in a virtualenv and use pip + requirements.txt to set up.

Copy:

`dashi/settings/example-instance.py` to `dsahi/settings/instance.py`

`dashi/settings/example-dashboard.py` to `dsahi/settings/dashboard.py`

...and customise both (should be fairly self documenting).

Some settings you can change:

  - `FAKE` - use fake data instead of connecting to redis, which can help when setting up.

## Running

To run on `localhost:8080` just do a standard a Django dev server:

```
python manage.py runserver
```

No wsgi adapter provided, but that should be fairly easy.
