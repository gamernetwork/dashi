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

## Setting up a fake data flow

Set up a local copy of Mormont:
https://github.com/gamernetwork/mormont

Inside the Mormont root directory:

```
docker-compose up -d
```

Ensure that the Mormont API is working by running the following curl command (you should get a success message):

```
curl "http://127.0.0.1:32770/api/measurement/v2/register_pageview?url=www.rockpapershotgun.de/article/red-dead-redemption&section=forum&language=en"
```

Go to Kibana (which is on 127.0.0.1:32768) and add 'analytics-pageview-clicktrack-*' as the index pattern. Select timestamp as time-field name. Now when you go to the discover tab on Kibana you should see a record of your curl request.

Set up a local copy of Mormont-client:
https://github.com/gamernetwork/mormont-client

Inside client/settings/v2/settings.js, for each url in the file, replace 127.0.0.1:8002 with 127.0.0.1:32770. This is where the Mormont API is available.
Run the test-impressions.html file in your browser. When you click 'spam' you should see pageviews automatically registering kibana.

In the dashboard file in Dashi, replace the line in DEFAULT_ES_SOURCE which reads: 
```
'host': 'https://mormont-es-ext.gamer-network.net',
```

with 

```
'host': 'http://127.0.0.1:9200',
```

## Running

To run on `localhost:8080` just do a standard a Django dev server:

```
python manage.py runserver --settings=dashi.settings.instance
```

## Hacking

Make new widgets by combining renderers and sources - see
blocks.py:Elaticsearch_Pie for a great exmaple.
