# Dashi - A flexible dashboard for serious stuff

Modular and configurable, simply reads data from redis keys or elasticsearch
queries - it's up to you to define what they are.

Uses the brilliant Highcharts.js library http://www.highcharts.com/docs

## Widgets

 - Activity graphs (numbers over time)
 - Top-things-tables out of elasticsearch 
 - Pie charts of things from elasticsearch
 - Raw HTML (for decoration)
 - Tickers (arbitrary numbers)
 - Nagios service status summary matrix (overall cluster health)
 - Overall THREAT LEVEL (i.e. is everything cool?)

## Setup

Install and run redis and/or elasticsearch as your data sources.

Pop in a virtualenv and use pip + requirements.txt to set up.

Install bower and install the frontend deps:

`bower install`

Copy:

`dashi/settings/example-instance.py` to `dashi/settings/instance.py`

`dashi/settings/example-dashboard.py` to `dashi/settings/dashboard.py`

...and customise both.

Some settings you can change:

  - `FAKE` - use fake data instead of connecting to redis, which can help when setting up.

## Running

To run on `localhost:8080` just do a standard a Django dev server:

```
python manage.py runserver
```

No wsgi adapter provided, but that should be fairly easy.

## Hacking

Make new widgets by combining renderers and sources - see
blocks.py:Elaticsearch_Pie for a great exmaple.
