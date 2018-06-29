# Dashi - A flexible dashboard for serious stuff

Modular and configurable, simply reads data from redis keys or elasticsearch
queries - it's up to you to define what they are.

Uses the brilliant Highcharts.js library http://www.highcharts.com/docs

## Design

Contains a frontend Django app and a backend gateway which marshalls and caches data from
data sources into a presentable form.

  - Gateway uses Celery 'beat' scheduling to perdiocally pull data from
    backends and prepare tabulated data in JSON form which is stored in Redis.
  - Client widgets poll Django reporting endpoints which check Redis for data
    in agreed format

## Widgets

 - Activity graphs (numbers over time)
 - Top-things-tables out of elasticsearch and other places
 - Pie charts of things from elasticsearch and other places
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
