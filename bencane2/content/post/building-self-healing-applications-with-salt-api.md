---
authors:
- Benjamin Cane
categories:
- Python
- Saltstack
date: '2014-12-30T14:50:00'
description: This article will explore creating an application that detects errors
  and corrects them by integrating Saltstack's API
draft: false
header:
  caption: ''
  image: ''
tags:
- saltstack
- self healing applications
- salt-api
- python
- devops
- automation
title: Building Self-Healing Applications with Saltstack
url: /2014/12/30/building-self-healing-applications-with-salt-api

---

Self healing infrastructure is something that has always piqued my interested. The first iteration of self healing infrastructure that I came across was the Solaris Service Management Facility aka "SMF". SMF would restart services if they crashed due to hardware errors or general errors outside of the service itself.

For today's article we are going to explore another way of creating a self healing environment; going beyond restarting failed services. In today's article we are going to take a snippet of code that connects to a database service and give that application not only the ability to reconnect during database failure but also give it the ability to automatically resolve the database issues.

## Starting with a simple connection

For today's article we are going to take a snippet of code [from an existing applicaton](https://github.com/asm-products/cloudroutes-service/blob/develop/src/bridge/bridge.py) and give it self healing super powers. The code we are using is from [Runbook](https://runbook.io) a side project of mine that does all sorts of cool automation for DevOps.

```python
# RethinkDB Server
try:
    rdb_server = r.connect(
        host=config['rethink_host'], port=config['rethink_port'],
        auth_key=config['rethink_authkey'], db=config['rethink_db'])
    print("Connected to RethinkDB")
except (RqlDriverError, socket.error) as e:
    print("Cannot connect to rethinkdb, shutting down")
    print("RethinkDB Error: %s") % e.message
    sys.exit(1)
```

_This code has been altered a bit for simplification._

The code above will attempt to connect to a [RethinkDB](http://rethinkdb.com) instance. If successful it creates a connection object `rdb_server` which can be used later for running queries against the database. If the connection is not successful the application will log an error and exit with an [exit code](http://bencane.com/2014/09/02/understanding-exit-codes-and-how-to-use-them-in-bash-scripts/) of `1`.

To put it simply, if RethinkDB is down or not accepting connections this process stops.

## Let's try again

Before we start adding super powers we need to change how the application handles connection errors. Right now it simply exits the process and unless we have external systems restarting the process it never attempts to reconnect. For a self healing application we should change this behavior to have the application reattempt connections until RethinkDB is online.

```python
# Set initial values
connection_attempts = 0
connected = False

# Retry RethinkDB Connections until successful
while connected == False:
    # RethinkDB Server
    try:
        rdb_server = r.connect(
            host=config['rethink_host'], port=config['rethink_port'],
            auth_key=config['rethink_authkey'], db=config['rethink_db'])
        connected = True
        print("Connected to RethinkDB")
    except (RqlDriverError, socket.error) as e:
        print("Cannot connect to rethinkdb")
        print("RethinkDB Error: %s") % e.message
    connection_attempts = connection_attempts + 1
    print("RethinkDB connection attempts: %d") % connection_attempts
```

If we breakdown the above code we can see that we added two new variables and a while loop. The above code will simply retry connecting to RethinkDB until successful. In some ways this in itself is making the application self healing, as it is gracefully handling an error with an external system and keeps trying to reconnect. These however are not the super powers I was referring to.

## Giving our application superpowers via Saltstack

In an earlier article I covered [implementing salt-api](http://bencane.com/2014/07/17/integrating-saltstack-with-other-services-via-salt-api/) the API for Saltstack. While that article covered utilizing salt-api with third party services such as Runbook or Datadog; that same level of integration could be added to applications themselves. Giving those applications the ability to run infrastructure tasks.

### Using Salt-API and Reactor Formula

For sake of brevity this article will assume that you already have Saltstack and salt-api installed and configured to accept webhook requests as outlined in the [previous article](http://bencane.com/2014/07/17/integrating-saltstack-with-other-services-via-salt-api/). For this article we will also be utilizing a [salt-api and reactor formula](https://github.com/madflojo/salt-api-reactor-formula) that I created for Runbook.

This formula provides several template reactor configurations that can be used to pickup salt-api webhook requests and perform salt actions. Actions such as restarting services, executing shell commands, or even start a highstate. To get started we will first need to download and extract the formula.

```shell
# wget -O /var/tmp/master.zip https://github.com/madflojo/salt-api-reactor-formula/archive/master.zip
# cd /var/tmp/
# unzip master.zip
```

Once extracted we can copy the reactor directory to `/srv/salt/`, this is the default salt directory and may need to be updated for your environment.

```shell
# cp -R salt-api-reactor-formula-master/reactor /srv/salt/
```

We will also need to deploy our reactor config to the `/etc/salt/master.d/` directory as this is what maps the URL endpoint to a specific salt action. Once deployed we will also need to restart the `salt-master` service.

```shell
# cp salt-api-reactor-formula-master/reactor.conf /etc/salt/master.d/
# service salt-master restart
```

#### Examining a reactor configuration

When our application is unable to connect to RethinkDB we want to perform some sort of corrective task. The easiest and safest thing to do in Runbook's environment is to simply run a salt **highstate**. A highstate execution will tell Saltstack to go through all of the defined configurations and make them true on the desired minion server. In our environment that includes ensuring the RethinkDB service is running and configured.

If our application is able to call a highstate execution on the database hosts there is a good chance that the issue may be corrected. Giving our application the ability to resolve any issue that was caused by RethinkDB not matching our desired state.


##### highstate.sls

In order to give our application the ability to run a highstate we will utilize the `reactor/states/highstate.sls` formula. Before going further we should first examine how this formula works.

```yaml+jinja
{% set postdata = data.get('post', {}) %}

{% if postdata.secretkey == "PICKSOMETHINGBETTERPLZKTHX" %}
state_highstate:
  cmd.state.highstate:
    - tgt: '{{ postdata.tgt }}'
    {% if "matcher" in postdata %}
    - expr_form: {{ postdata.matcher }}
    {% endif %}
    {% if "args" in postdata %}
    - arg:
      - {{ postdata.args }}
    {% endif %}
{% endif %}
```

When a `POST` request is made to the `http://saltapiurl/webhooks/states/highstate` address salt-api will take the `POST` data of that request and pass it along salts event system. When processed this reactor configuration will take the `POST` data and assign it to a dictionary named `postdata`. From there salt will check for a key in the `postdata` dictionary named `secretkey` and ensure that the value of that key matches the defined "secretkey" in the template. This section is used to act as an authentication method for webhooks.

Each reactor template has an example secret key defined, it is recommended that you modify this to a unique value for your environment.

After validation salt will look for additional keys in the `postdata` dictionary, for our purpose we will need to understand the `tgt` and `matcher` keys. The `tgt` key is used to specify the "target" for the highstate execution. This target can be a hostname, a grain value, pillar value, subnet or any other target Saltstack accepts. The `matcher` key contains a definition of the `tgt` keys expression, for instance if the `tgt` value was a hostname, the `matcher` value should be `glob` for a hostname glob. If the `tgt` value was a pillar value, the `matcher` value should be `pillar`. You can find all of the valid matcher values in [salt-api's documentation](http://docs.saltstack.com/en/latest/ref/clients/#salt.client.LocalClient.cmd).

### Calling salt-api

Now that we have salt-api configured to accept webhook requests and start highstate executions, we now need to code our application to call those webhooks. Since this is something we may want to do somewhat often in our code we can create a function to perform this webhook request.

#### Highstate Function

```python
def callSaltHighstate(config):
    ''' Call Saltstack to initiate a highstate '''
    import requests
    url = config['salt_url'] + "/states/highstate"
    headers = {
        "Accept:" : "application/json"
    }
    postdata = {
        "tgt" : "db*",
        "matcher" : "glob",
        "secretkey" : config['salt_key']
    }
    try:
        req = requests.post(url=url, headers=headers, data=postdata, verify=False)
        print("Called for help and got response code: %d") % req.status_code
        if req.status_code == 200:
            return True
        else:
            return False
    except (requests.exceptions.RequestException) as e:
        print("Error calling for help: %s") % e.message
        return False
```

The code above is pretty simple, it essentially performs an HTTP `POST` request with `POST` data fields `tgt`, `matcher` and `secretkey`. The `tgt` field contains `db*` which in our field is a hostname glob that matches our database server names. The `matcher` value is `glob` to denote that the `tgt` value is a hostname glob value. The `secretkey` actually contains the value of `config['salt_key']` which is pulled from our configuration file when the main process starts and is passed to the `callSaltHighstate()` function.

Now that the code to call salt-api is defined we can add the `callSaltHighstate()` function into the exception handling for RethinkDB.

#### Adding callSaltHighstate as an action

```python
# Set initial values
connection_attempts = 0
connected = False

# Retry RethinkDB Connections until successful
while connected == False:
    # RethinkDB Server
    try:
        rdb_server = r.connect(
            host=config['rethink_host'], port=config['rethink_port'],
            auth_key=config['rethink_authkey'], db=config['rethink_db'])
        connected = True
        print("Connected to RethinkDB")
    except (RqlDriverError, socket.error) as e:
        print("Cannot connect to rethinkdb")
        print("RethinkDB Error: %s") % e.message
        callSaltHighstate(config)
    connection_attempts = connection_attempts + 1
    print("RethinkDB connection attempts: %d") % connection_attempts
```

As you can see the code above hasn't changed much from the previous example. The biggest change is that after printing the RethinkDB error we experienced we then execute the `callSaltHighstate()` function.

### Leveling up

For a simple example the above code works quite well, however there is a bit of a flaw. With the above code a highstate will be called every time the application attempts to connect to RethinkDB and fails. Since a highstate will take a bit of time to execute this could cause a backlog of highstate executions which could in theory cause even more issues.

To combat this at the end of the while loop you could add a `time.sleep(120)` to cause the application to sleep for 120 seconds between each while loop executions. This would give Saltstack some time to execute the highstate before another is queued. While a sleep would work and is simple, it is not the most elegant method.

Since we can call Saltstack to perform essentially any task Saltstack can perform. Why stop at just a highstate? Below we are going to create another function that calls salt-api, but rather than run a highstate this function will send a webhook request that tells salt-api to restart the RethinkDB service.

#### Restart function

```python
def callSaltRestart(config):
    ''' Call Saltstack to restart a service '''
    import requests
    url = config['salt_url'] + "/services/restart"
    headers = {
        "Accept:" : "application/json"
    }
    postdata = {
        "tgt" : "db*",
        "matcher" : "glob",
        "args" : "rethinkdb",
        "secretkey" : config['salt_key']
    }
    try:
        req = requests.post(url=url, headers=headers, data=postdata, verify=False)
        print("Called for help and got response code: %d") % req.status_code
        if req.status_code == 200:
            return True
        else:
            return False
    except (requests.exceptions.RequestException) as e:
        print("Error calling for help: %s") % e.message
        return False
```

The above code is very similar to the highstate function with the exception that the URL endpoint has changed to `/services/restart` (which utilizes the `reactor/services/restart.sls` template) and there is a new `POST` data key called `args` which contains `rethinkdb` the service in which we want to restart.

Since we are adding the complexity of restarting the RethinkDB service we want to make sure that this call is not made too often. At the moment the best way to do this is to build that logic into the application itself.

#### Extending when to call salt-api

```python
# Set initial values
connection_attempts = 0
first_connect = 0.00
last_restart = 0.00
last_highstate = 0.00
connected = False
called = None

# Retry RethinkDB Connections until successful
while connected == False:
    if first_connect == 0.00:
        first_connect = time.time()
    # RethinkDB Server
    try:
        rdb_server = r.connect(
            host=config['rethink_host'], port=config['rethink_port'],
            auth_key=config['rethink_authkey'], db=config['rethink_db'])
        connected = True
        print("Connected to RethinkDB")
    except (RqlDriverError, socket.error) as e:
        print("Cannot connect to rethinkdb")
        print("RethinkDB Error: %s") % e.message
        timediff = time.time() - first_connect
        if timediff > 300.00:
            last_timediff = time.time() - last_restart
            if last_timediff > 600.00 or last_restart == 0.00:
                if timediff > 600:
                    callSaltRestart(config)
                last_restart = time.time()
            last_timediff = time.time() - last_highstate
            if last_timediff > 300.00 or last_highstate == 0.00:
                callSaltHighstate(config)
                last_highstate = time.time()
    connection_attempts = connection_attempts + 1
    print("RethinkDB connection attempts: %d") % connection_attempts
    time.sleep(60)
```

As you can see with the above code we added quite a bit of logic around when to run and when not to run. With the above code, when our application is unable to connect to RethinkDB it will keep retrying until successful, just as before. However, every 5 minutes if the application is unable to connect to RethinkDB it will call Saltstack via salt-api requesting a highstate be executed on the database servers. Every 10 minutes, if RethinkDB is still not accessible this application will call Saltstack via salt-api requesting a restart of the RethinkDB service on all database servers.

## Improvements

With today's example we are able to correct situations that many applications cannot. Being able to restart the database when you are unable to connect to it is a good example of a self healing environment. However, there are more things that could be done to this application.

This same type of logic could be built into Query exceptions rather than Connection exceptions only. With query exceptions you could also use salt-api to execute database maintenance scripts or call salt-cloud to provision additional servers. Once you give your application the ability to perform infrastructure wide actions you open the door to a wide range of automation capabilities.

_To see the full script from this example you can view it on [this GitHub Gist](https://gist.github.com/madflojo/95fe54b4e42ff01e1ba1)_
