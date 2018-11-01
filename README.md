# Dashi - A flexible dashboard for serious stuff

Modular and configurable, simply reads data from redis keys or elasticsearch
queries - it's up to you to define what they are.

## Widgets

 - Activity graphs (numbers over time)
 - Top-things-tables out of elasticsearch and other places
 - Pie charts of things from elasticsearch and other places
 - Raw HTML (for decoration)
 - Tickers (arbitrary numbers)

## Setup

Install and configure elasticsearch as your data sources.

Install memcached as your query cache.

Pop in a virtualenv and use pip + requirements.txt to set up.

```
pip install -f requirements
```

Install yarn: https://yarnpkg.com/en/docs/install

Install frontend deps:

```
cd dashi/static/
yarn install
```

Set up some configuration files:

`dashi/settings/example-instance.py` to `dashi/settings/instance.py`

`dashi/settings/example-dashboard.py` to `dashi/settings/dashboard.py`

...and customise both.

Some settings you can change:

  - `FAKE` - use fake data instead of connecting to redis, which can help when setting up.

## Running

To run on `localhost:8080` just do a standard a Django dev server:

```
python manage.py runserver --settings=dashi.settings.instance
```

## Hacking

Make new widgets by combining renderers and sources - see
blocks.py:Elaticsearch_Pie for a great exmaple.
