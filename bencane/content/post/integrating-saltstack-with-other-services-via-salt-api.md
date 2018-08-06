---
authors:
- Benjamin Cane
categories:
- SaltStack
date: '2014-07-17T00:00:00'
description: This article will walk you through using salt-api as an entry point for
  other services to call SaltStack to initiate actions within your infrastructure.
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- saltstack
- salt-api
- saltstack api
title: Using salt-api to integrate SaltStack with other services
url: /2014/07/17/integrating-saltstack-with-other-services-via-salt-api

---

Recently I have been looking for ways to allow external tools and services to perform corrective actions across my infrastructure automatically. As an example, I want to allow a monitoring tool to monitor my nginx availability and if for whatever reason nginx is down I want that monitoring tool/service to do something to fix it.

While I was looking at how to implement this, I remembered that SaltStack has an API and that API can provide exactly the functionality I wanted. The below article will walk you through setting up `salt-api` and configuring it to allow third party services to initiate SaltStack executions.

## Install salt-api

The first step to getting started with `salt-api` is to install it. In this article we will be installing `salt-api` on a single master server, it is possible to run `salt-api` on a multi-master setup however you will need to ensure the configuration is consistent across master servers.

Installation of the `salt-api` package is pretty easy and can be performed with `apt-get` on Debian/Ubuntu or `yum` on Red Hat variants.

    # apt-get install salt-api

## Generate a self signed certificate

By default `salt-api` utilizes HTTPS and while it is possible to disable this, it is generally not a good idea. In this article we will be utilizing HTTPS with a self signed certificate.

Depending on your intended usage of `salt-api` you may want to [Generate a certificate that is signed by a certificate authority](https://www.openssl.org/docs/HOWTO/certificates.txt), if you are using `salt-api` internally only a self signed certificate should be acceptable.

### Generate the key

The first step in creating any SSL certificate is to generate a key, the below command will generate a `4096` bit key.

    # openssl genrsa -out /etc/ssl/private/key.pem 4096

### Sign the key and generate a certificate

After we have generated the key we can generate the certificate with the following command.

    # openssl req -new -x509 -key /etc/ssl/private/key.pem -out /etc/ssl/private/cert.pem -days 1826

The `-days` option allows you to specify how many days this certificate is valid, the above command should generate a certificate that is valid for 5 years.

## Create the rest_cherrypy configuration

Now that we have installed `salt-api` and generated an SSL certificate we can start configuring the `salt-api` service. In this article we will be placing the `salt-api` configuration into `/etc/salt/master.d/salt-api.conf` you can also put this configuration directly in the `/etc/salt/master` configuration file; however, I prefer putting the configuration in `master.d` as I believe it allows for easier upkeep and better organization.

    # vi /etc/salt/master.d/salt-api.conf

### Basic salt-api configuration

**Insert**

    rest_cherrypy:
      port: 8080
      host: 10.0.0.2
      ssl_crt: /etc/ssl/private/cert.pem
      ssl_key: /etc/ssl/private/key.pem

The above configuration enables a very basic `salt-api` instance, which utilizes SaltStack's [external authentication system](http://docs.saltstack.com/en/latest/topics/eauth/index.html). This system requires requests to authenticate with user names and passwords or tokens; in reality not every system can or should utilize those methods of authentication. 

### Webhook salt-api configuration

Most systems and tools however do support utilizing a pre-shared API key for authentication. In this article we are going to use a pre-shared API key to authenticate our systems with `salt-api`. To do this we will add the `webhook_url` and `webhook_disable_auth` parameters.

**Insert**

    rest_cherrypy:
      port: 8080
      host: <your hosts ip>
      ssl_crt: /etc/ssl/private/cert.pem
      ssl_key: /etc/ssl/private/key.pem
      webhook_disable_auth: True
      webhook_url: /hook

The `webhook_url` configuration parameter tells `salt-api` to listen for requests to the specified URI. The `webhook_disable_auth` configuration allows you to disable the external authentication requirement for the webhook URI. At this point in our configuration there is no authentication on that webhook URI, and any request sent to that webhook URI will be posted to SaltStack's event bus.

## Actioning webhook requests with Salt's Reactor system

SaltStack's event system is a internal notification system for SaltStack, it allows external processes to listen for SaltStack events and potentially action them. A few examples of events that are published to this event system are Jobs, Authentication requests by minions, as well as salt-cloud related events. A common consumer of these events is the SaltStack Reactor system, the Reactor system allows you to listen for events and perform specified actions when those events are seen.

### Reactor configuration

We will be utilizing the Reactor system to listen for webhook events and execute specific commands when we see them. Reactor definitions need to be included in the master configuration, for this article we will define our configuration within the `master.d` directory.

    # vi /etc/salt/master.d/reactor.conf

**Insert**

    reactor:
      - 'salt/netapi/hook/restart':
        - /salt/reactor/restart.sls

The above command will listen for events that are tagged with `salt/netapi/hook/restart` which would mean any API requests targeting `https://example.com:8080/hook/restart`. When those events occur it will execute the items within `/salt/reactor/restart.sls`.

### Defining what happens

Within the `restart.sls` file, we will need to define what we want to happen when the `/hook/restart` URI is requested.

    # vi /salt/reactor/services/restart.sls

#### Simply restarting a service

To perform our simplest use case of restarting nginx when we get a request to `/hook/restart` you could add the following.

**Insert**

    restart_services:
      cmd.service.restart:
        - tgt: 'somehost'
        - arg:
          - nginx

This configuration is extremely specific and doesn't leave much chance for someone to exploit it for malicious purposes. This configuration is also extremely limited.

#### Restarting the specified services on the specified servers

When a `salt-api`'s webhook URL is called the `POST` data being sent with that request is included in the event message. In the below configuration we will be using that `POST` data to allow request to the webhook URL to specify both the target servers and the service to be restarted.

**Insert**

    {% set postdata = data.get('post', {}) %}
    
    restart_services:
      cmd.service.restart:
        - tgt: '{{ postdata.tgt }}'
        - arg:
          - {{ postdata.service }}

In the above configuration we are taking the `POST` data sent to the URL and assigning it to the `postdata` object. We can then use that object to provide the `tgt` and `arg` values. This allows the same URL and webhook call to be used to restart any service on any or all minion nodes.

Since we disabled external authentication on the webhook URL there is currently no authentication with the above configuration. This means that anyone who knows our URL could send a well formatted request and restart any service on any minion they want.

#### Using a secret key to authenticate

To secure our webhook URL a little better we can add a few lines to our reactor configuration that requires that requests to this reactor include a valid secret key before executing.

**Insert**

    {% set postdata = data.get('post', {}) %}
    
    {% if postdata.secretkey == "replacethiswithsomethingbetter" %}
    restart_services:
      cmd.service.restart:
        - tgt: '{{ postdata.tgt }}'
        - arg:
          - {{ postdata.service }}
    {% endif %}

The above configuration requires that the requesting service include a `POST` key of `secretkey` and the value of that key must be `replacethiswithsomethingbetter`. If the requester does not, the Reactor will simply perform no steps. 
The secret key in this configuration should be treated like any other API key, it should be validated before performing any action and if you have more than one system/user making requests you should ensure that only the correct users have the ability to execute the commands specified in the reactor `SLS` file.

### Restarting salt-master and Starting salt-api

Before testing our new `salt-api` actions we will need to restart the `salt-master` service and start the `salt-api` service.

    # service salt-master restart
    # service salt-api start

## Testing our configuration with curl

Once the two above services have finished restarting we can test our configuration with the following `curl` command.

    # curl -H "Accept: application/json" -d tgt='*' -d service="nginx" -d secretkey="replacethiswithsomethingbetter" -k https://salt-api-hostname:8080/hook/services/restart

If the configuration is correct you should expect to see a message stating success.

**Example**

    # curl -H "Accept: application/json" -d tgt='*' -d service="nginx" -d secretkey="replacethiswithsomethingbetter" -k https://10.0.0.2:8080/hook/services/restart
    {"success": true}

At this point you can now integrate any third party tool or service that can send webhook requests with your SaltStack implementation. You can also use `salt-api` to have home grown tools initiate SaltStack executions.

## Additional Considerations

### Other netapi modules

In this article we implemented `salt-api` with the cherrypy netapi module, this is one of [three options](http://docs.saltstack.com/en/latest/ref/netapi/all/index.html#all-netapi-modules) that SaltStack gives you. If you are more familiar with other application servers such as wsgi than I would suggest looking through the documentation to find the appropriate module for your environment.

### Restricting salt-api

While in this article we added a secret key for authentication and SSL certificates for encrypted HTTPS traffic; there are additional options that can be used to restrict the `salt-api` service further. If you are implementing the `salt-api` service into a non-trusted network, it is a good idea to use tools such as `iptables` to restrict which hosts / IP's are able to utilize the `salt-api` service.

In addition when implementing `salt-api` it is a good idea to think carefully as to what you allow systems to request. A simple example of this would be the `cmd.run` module within SaltStack. If you allowed a server to perform dynamic `cmd.run` requests via `salt-api, if a malicious user was able to bypass the implemented restrictions that user would then be able to theoretically run any arbitrary command on your systems.

It is always best to only allow specific commands through the API system and avoid allowing potentially dangerous commands such as `cmd.run`.
