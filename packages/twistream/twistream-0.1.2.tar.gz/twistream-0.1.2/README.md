# Twistream: Twitter Stream API data collection

[![CircleCI](https://circleci.com/gh/guillermo-carrasco/twistream.svg?style=svg)](https://circleci.com/gh/circleci/circleci-docs)
[![PyPI version](https://badge.fury.io/py/twistream.svg)](https://badge.fury.io/py/twistream)

Twistream helps you automatically collect and store data from Twitter Stream API.

## Installation

Latest stable release:

    pip install twistream

From source:

    git clone https://github.com/guillermo-carrasco/twistream.git
    cd twistream
    pip install .

### Setting up

#### Twitter credentials
You need your twitter credentials in order to be able to use Twitter API. For that,
create an application [here](https://apps.twitter.com). Once created, save the credentials to configure
twistream

#### Create a configuration file

You can use the command `twistream init` to help you create a correctly formatted configuration file
for your collections.

Once created, you will have a file that will luke like this:

```
~> cat ~/.twistream/twistream.yml      

twitter:                  
  consumer_key: your_consumer_key                   
  consumer_secret: your_consumer_secret             
  access_token_key: your_access_token_key             
  access_token_secret: your_access_token_secret       
      

backend: backend_name                  

backend_params:
    username: db_username
    password: db_password
```

## Usage

__**Remember that `--help` is always an available option**__

Once created a configuration file, start collecting tweets!

```
twistream collect --tracks tracks,to,follow
```

Refer to the [twitter documentation][streaming-docs] to know what tracks are, in short: 

> A comma-separated list of phrases which will be used to determine what Tweets will be delivered 
> on the stream. A phrase may be one or more terms separated by spaces, and a phrase will match 
> if all of the terms in the phrase are present in the Tweet, regardless of order and ignoring case.
> By this model, you can think of commas as logical ORs, while spaces are equivalent to 
> logical ANDs (e.g. ‘the twitter’ is the AND twitter, and ‘the,twitter’ is the OR twitter).

If what you want is to follow hashtags, don't forget to include the `#` character.

### Supported backends
Right now twistream only supports sqlite, the `backend` and `backend_params` sections in your
configuration file should look like this:

```
backend: sqlite

backend_params:
    db: /path/to/your/db
```

[streaming-docs]: https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters