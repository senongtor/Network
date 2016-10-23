## Synopsis

This is a simple http **proxy**. 

## How to use it

Because Firefox defaults to using HTTP/1.1 and your proxy speaks HTTP/1.0, there are a couple of minor changes that need to be made to Firefox's configuration. Fortunately, Firefox is smart enough to know when it is connecting through a proxy, and has a few special configuration keys that can be used to tweak the browser's behavior.1. Type'about:config'inthetitlebar.2. In the search/filter bar, type 'network.http.proxy'3. You should see two keys: network.http.proxy.pipelining,and network.http.proxy.version.4. Set version to 1.0. Make sure that pipelining is set to false.
5. Manually set up proxy with host name localhost and port number with any portnumber you want to test on.
6. In your terminal where this script is at, do python minimal proxy.py -portnumber.
7. The portnumber of 5 and 6 needs to be matched.

## Motivation

A toy proxy for understanding how proxy actually works.


## Blocking

'www.baidu.com','www.cnn.com','www.nyu.edu','www.aol.com','www.dmv.org',
'www.stackoverflow.com','www.bbc.co.uk','www.youku.com','www.ticketmaster.com','www.columbia.edu' are blocked. These are set arbitrarily for test

## Filtering

Filtering words are: 'research’,’porn’. These are set arbitrarily for test

