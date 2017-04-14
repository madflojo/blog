Recently there has been a lot of news & talk about how to secure internet traffic to prevent snooping both from service providers and governments. In this article I am going to show one method of anonymizing internet traffic by walking through using **stunnel** to create an SSL tunnel with an instance of **TinyProxy** on the other side.

## How does this help anonymize my internet traffic

**TinyProxy** is an HTTP & HTTPS proxy server. By setting up a TinyProxy instance on a remote server and configuring our HTTP client to use this as a proxy. We can route all of our HTTP & HTTPS traffic through a remote server. This is a useful technique for getting around network restrictions that might be imposed by ISP's or Governments. But by simply routing the HTTP/HTTPS traffic to a remote server we are not adding any protection to the traffic itself. All of the HTTP traffic to TinyProxy would be unencrypted, leaving it open to packet capture and inspection. That is where **stunnel** comes into play.

I've featured it in earlier articles but for those who are new to stunnel, it is a proxy that allows you to create a TLS tunnel between two or more systems. In this article we will use stunnel to create a TLS tunnel between the HTTP client system and TinyProxy.

By using a TLS tunnel between the HTTP client and TinyProxy our HTTP traffic will be encrypted between the local system and the proxy server. This means anyone trying to inspect HTTP traffic will be unable to see the contents of our HTTP traffic. This is also useful for reducing the chances of a [man-in-the-middle attack](https://www.eff.org/deeplinks/2010/08/open-letter-verizon) to HTTPS sites.

I say reducing because one of the caveats of this article is, while routing our HTTP & HTTPS traffic through a TLS tunneled HTTP proxy help obfuscate and anonymize our traffic from the client's perspective. The system running TinyProxy is still susceptible to man-in-the-middle attacks and HTTP traffic snooping. Essentially, with this article, we are not focused on solving the problem, simply moving our problem to a network where no one is looking. This is essentially the same approach as VPN service providers, the advantage of running your own proxy is that you control the proxy.

Now that we understand why we are setting up our HTTP Proxy, let's go ahead and get started with the installation of TinyProxy.

## Installing TinyProxy

The installation of TinyProxy is fairly easy and can be accomplished using the `apt-get` command on Ubuntu systems. Let's go ahead an install TinyProxy on our future proxy server.

```shell
server: $ sudo apt-get install tinyproxy
```

Once the `apt-get` command finishes, we can move to configuring TinyProxy.

### Configuring TinyProxy

By default TinyProxy starts up listening on all interfaces for connections on port `8888`. Since we don't want to leave our proxy open to anyone who happens upon it let's change this by configuring TinyProxy to listen to the `localhost` interface only. We can do this by editing the `/etc/tinyproxy.conf` file.

Find:
```ini
#Listen 192.168.0.1
```

Replace With:
```ini
Listen 127.0.0.1
```

Once complete, we will need to restart the TinyProxy service in order for our change to take effect. We can do this using the `systemctl` command.

```shell
server: $ sudo systemctl restart tinyproxy
```

We can validate that our change is in place by checking whether port `8888` is bound correctly via the `netstat` command.

```shell
server: $ netstat -na
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:8888          0.0.0.0:*               LISTEN
```

It appears TinyProxy is setup correctly. With that done, let's go ahead and setup stunnel.

## Installing stunnel

Just like TinyProxy, the installation of stunnel is as easy as executing the `apt-get` command.

```shell
server: $ sudo apt-get install stunnel
```

Once `apt-get` has finished we can move on to enabling stunnel within the `/etc/default/stunnel4` configuration file.

Find:
```ini
# Change to one to enable stunnel automatic startup
ENABLED=0
```

Replace:
```ini
# Change to one to enable stunnel automatic startup
ENABLED=1
```

By default on Ubuntu, stunnel is installed in a disabled mode. By changing the `ENABLED` flag from `0` to `1` within `/etc/default/stunnel4`, we are enabling stunnel to start. However, our configuration of stunnel does not stop there.

```shell
server: $ sudo systemctl restart stunnel4
```

Our next step with stunnel, will involve defining our TLS tunnel.

### TLS Tunnel Configuration (Server)

By default stunnel will look in `/etc/stunnel` for any files that end in `.conf`. In order to configure our TLS stunnel we will start by creating the file `/etc/stunnel/stunnel.conf`. Once created, we will insert the following content.

```ini
[tinyproxy]
accept = 0.0.0.0:3128
connect = 127.0.0.1:8888
cert = /etc/ssl/cert.pem
key = /etc/ssl/key.pem
```

The contents of this configuration file are fairly straight forward but let's go ahead and break down what each of these items mean. We will start with the `accept` option.

The `accept` option is similar to the `listen` option from TinyProxy. This setting will define what interface and port stunnel will listen on for incoming connections. By setting this to `0.0.0.0:3128` we are telling stunnel to listen on all interfaces on port `3128`.

The `connect` option is used to tell stunnel what IP and port to connect to. In our case this needs to be the IP and port that TinyProxy is listening on; `127.0.0.1:8888`.

An easy way to remember how `accept` and `connect` should be configured is that `accept` is where incoming connections should come from, and `connect` is where they should go to.

Our next two configuration items are closely related, `cert` & `key`. The `cert` option is used to define the location of an SSL certificate that will be used to establish our TLS session. The `key` option is used to define the location of the key used to create the SSL certificate.

We will set these to be located in `/etc/ssl` and in the next step, we will go ahead and create both the key and certificate.

## Creating a self-signed certificate

The first step in creating a self-signed certificate is to create an private key. To do this we will use the following `openssl` command.

```shell
server: $ sudo openssl genrsa -out /etc/ssl/key.pem 4096
```

The above will create a **4096 bit** RSA key. From this key, we will create a public certificate using another `openssl` command. During the execution of the following command there will be a series of questions. These questions are used to populate the key with organization information. Since we will be using this for our own purposes we will not worry too much about the answers to these questions.

```shell
server: $ sudo openssl req -new -x509 -key /etc/ssl/key.pem -out /etc/ssl/cert.pem -days 1826
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:Arizona
Locality Name (eg, city) []:Phoenix
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Example.com
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:proxy.example.com
Email Address []:proxy@example.com
```

Once the questions have been answered the `openssl` command will create our certificate file. After both the certificate and key have been created, we will need to once again restart stunnel in order for the key and certificate to be loaded.

```shell
server: $ sudo systemctl restart stunnel4
```

After restart we have now finished configuring the proxy server. We now need to setup our client.

## Setting up stunnel (client)

Like with the proxy server, our first step in setting up stunnel is installing it with the `apt-get` command.

```shell
client: $ sudo apt-get install stunnel
```

We will also once again need to enabling stunnel within the `/etc/default/stunnel4` configuration file.

Find:
```ini
# Change to one to enable stunnel automatic startup
ENABLED=0
```

Replace:
```ini
# Change to one to enable stunnel automatic startup
ENABLED=1
```

After enabling stunnel we will need to restart the service with the `systemctl` command.

```shell
client: $ sudo systemctl restart stunnel4
```

We can now move to configuring the stunnel client.

### TLS Tunnel Configuration (Client)

The configuration of stunnel in "client-mode" is only a little different than the "server-mode" configuration we set earlier. As with before we will insert the following into the `/etc/stunnel/stunnel.conf` configuration file.

```ini
client = yes

[tinyproxy]
accept = localhost:3128
connect = 192.168.33.10:3128
verify = 4
CAFile = /etc/ssl/cert.pem
```



```
ubuntu@ubuntu-xenial:/etc/ssl$ export http_proxy="http://localhost:3128"
ubuntu@ubuntu-xenial:/etc/ssl$ export https_proxy="https://localhost:3128"
ubuntu@ubuntu-xenial:/etc/ssl$ curl -v http://google.com
* Rebuilt URL to: http://google.com/
*   Trying 127.0.0.1...
* Connected to localhost (127.0.0.1) port 3128 (#0)
> GET http://google.com/ HTTP/1.1
> Host: google.com
> User-Agent: curl/7.47.0
> Accept: */*
> Proxy-Connection: Keep-Alive
>
* HTTP 1.0, assume close after body
< HTTP/1.0 301 Moved Permanently
< Via: 1.1 tinyproxy (tinyproxy/1.8.3)
< Content-Type: text/html; charset=UTF-8
< Date: Wed, 12 Apr 2017 06:52:23 GMT
< X-Frame-Options: SAMEORIGIN
< Expires: Fri, 12 May 2017 06:52:23 GMT
< Server: gws
< Content-Length: 219
< Cache-Control: public, max-age=2592000
< X-XSS-Protection: 1; mode=block
< Location: http://www.google.com/
<
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="http://www.google.com/">here</A>.
</BODY></HTML>
* Closing connection 0
```
