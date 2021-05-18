---
title: "Using Viper With Consul to Configure Go Applications"
date: 2021-05-18T08:00:00-07:00
aliases: ["/post/using-viper-with-consul-to-configure-go-apps/"]
draft: false
subtitle: "Learn how to use Consul with the popular Go configuration package Viper"
summary: "Viper is a powerful configuration library which also supports pulling configuration from Consul. However, using Consul is not straightforward. This article explains how to use Viper with Consul"
authors: ["Benjamin Cane"]
tags: ["golang", "consul"]
categories: ["Software Engineering"]
featured: true
url: /2021/05/18/using-viper-with-consul-to-configure-go-apps
---

Recently I wanted to revamp one of my side projects [go-quick](https://github.com/madflojo/go-quick). This project is a boilerplate web application meant to be a starting point for Go apps. Previously, I wrote a custom config package within the project to pull configuration from Environment Variables as per the [12 Factor Apps manifest](https://12factor.net/). But, I wanted to expand how users can configure my project. 

Enter [HashiCorp Consul](https://www.consul.io/). Consul is open source and solves many of the platform painpoints of running modern applications. One of those is dynamic configuration via its distributed key-value store.  With Consul, applications can boot up using Consul as the remote source of their configuration. These applications can also periodically pull and update their configuration parameters from Consul.

This dynamic update happens without a restart, something not possible with the traditional Environment Variable-based configuration. But this article isn't about Consul; this article is about Viper.

## Why Viper

The goal of my boilerplate project is to provide an easy-to-use starter Go application. While many would be happy to have a Consul-backed configuration baked in, not everyone uses Consul. Many users, especially those just starting in Go, will most likely choose a more straightforward configuration method. Like Environment Variables.

Since I need to support configuring the application in multiple ways (Environment Variables, Consul, maybe even a JSON file), I needed a much more robust configuration library, like [spf13/viper](https://github.com/spf13/viper).

Viper is a Go package that aims to be a complete configuration library. It allows users to use multiple sources for configuration and even use them together. This capability is what I want; as such, I decided to replace my custom configuration package with Viper. But in doing so, I found out that using Viper with Consul wasn't as straightforward as I thought.

This article will show how my project uses Viper and what you need to do to make Viper work with Consul. 

## Getting Started

Before we jump into the Viper configuration, it will help to go through how my project is structured. Much like my [command-line application structure](https://bencane.com/2020/12/29/how-to-structure-a-golang-cli-project/) article outlines, the main application code exists within an `app` package. This `app` package has both a `Run()` and a `Stop()` function for starting and stopping the application.

```golang
package app

import (
	// imports go here
	"github.com/madflojo/go-quick/config"
)

// Common errors returned by this app.
var (
	ErrShutdown = fmt.Errorf("application shutdown gracefully")
)

// cfg is used across the app package to contain configuration.
var cfg config.Config

// Run starts the primary application. It handles starting background services,
// populating package globals & structures, and clean up tasks.
func Run(c config.Config) error {

	// Apply config provided by main
	cfg = c

	// Application logic goes here
}

// Stop is used to gracefully shutdown the server.
func Stop() {
	// Stop logic goes here
}
```

However, unlike my command-line example, I tend to create a `cmd/<application-name>` directory for the `main` package for an application service. I make this structure because, unlike a command-line application. I do not expect anyone to try and use `go get` to install my application service, and I find it a little cleaner for application services.

The below `tree` command shows my project structure before starting with Viper.

```console
$ tree -L 2
.
├── CONTRIBUTING.md
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── app
│   ├── app.go
│   ├── app_test.go
│   └── server.go
├── cmd
│   └── go-quick
├── config
│   ├── config.go
│   └── config_test.go
├── dev-compose.yml
├── doc.go
├── docker-compose.yml
├── docker-entrypoint.sh
├── go.mod
├── go.sum
└── secret.txt

5 directories, 19 files
```

Now that we've explored the application structure, the first thing we need to do is replace the `go-quick/config` package with Viper. Since the current package pulls configurations from Environment Variables, we will initially set up Viper to do the same thing. Once that's working, we will move on to more complex aspects.

To start within the `app` package, we will change `cfg` from a `config.Config` type to `*viper.Viper`.

```golang
package app

import (
  // imports go here
  "github.com/spf13/viper"
)

// Common errors returned by this app.
var (
  ErrShutdown = fmt.Errorf("application shutdown gracefully")
)

// cfg is used across the app package to contain configuration.
var cfg *viper.Viper

// Run starts the primary application. It handles starting background services,
// populating package globals & structures, and clean up tasks.
func Run(c *viper.Viper) error {

  // Apply config provided by main
  cfg = c

  // Application logic goes here
}

// Stop is used to gracefully shutdown the server.
func Stop() {
  // Stop logic goes here
}
```

With this change, references further in the application code to the `cfg` variable will also need to change. References such as `cfg.ListenerAddr()` will need to change to `cfg.GetString("listener_addr")`. But we will address that later. We will now adjust how we initialize Viper and pass it to the `Run()` function.

## Loading Config from Env

First, we need to initialize Viper creating a `*viper.Viper` object within the `main` package. Once we've done that, we can add the code required to tell Viper to load configuration from the environment and use the `ReadInConfig()` function to have Viper find and load configuration from Files and Environment.

```golang
package main

import (
  "github.com/madflojo/go-quick/app"
  "github.com/sirupsen/logrus"
  "github.com/spf13/viper"
)

func main() {
  // Initiate a simple logger
  log := logrus.New()

  // Setup Config
  cfg := viper.New()

  // Load Config
  cfg.SetEnvPrefix("app")
  cfg.AllowEmptyEnv(true)
  cfg.AutomaticEnv()
  err := cfg.ReadInConfig()
  if err != nil {
    log.Warnf("Error when Fetching Configuration - %s", err)
  }

  // Run application
  err = app.Run(cfg)
  if err != nil && err != app.ErrShutdown {
    log.Fatalf("Service stopped - %s", err)
  }
  log.Infof("Service shutdown - %s", err)
}
```

In the above, we created a `*viper.Viper` object using the `New()` function. We also told Viper to allow empty environment variables by calling `AllowEmptyEnv()` with a `true` parameter. But an important item to be mindful of is the use of `SetEnvPrefix()` with the `app` value.

By default, when Viper loads configuration from the environment, it will take all environmental variables and make them available as config. This option can be helpful for some situations, but I elected to change this behavior for my project.

Using the `SetEnvPrefix()` function, we set Viper up to only load environment variables with an `APP_` prefixed. With this setup, an item such as `APP_DEBUG` will convert to `debug`. 

I prefer to use the prefix method because it allows me to have finer control over what environment variables become configuration. But either way works; this is more of a preference vs. a practice argument.

## Loading Config from File

While not my favorite method of managing config, many people still use configuration files for their applications. Since I want my project to be usable in many environments, it also makes sense to set it up to support configuration files. 

Luckily, doing this with Viper is pretty simple; all it takes is calling the `AddConfigPath()` function.

```golang
  // Load Config
  cfg.AddConfigPath("./conf")
  cfg.SetEnvPrefix("app")
  cfg.AllowEmptyEnv(true)
  cfg.AutomaticEnv()
  err := cfg.ReadInConfig()
  if err != nil {
    switch err.(type) {
    case viper.ConfigFileNotFoundError:
      log.Warnf("No Config file found, loaded config from Environment - Default path ./conf")
    default:
      log.Fatalf("Error when Fetching Configuration - %s", err)
    }
  }
```

In the above, I used the `AddConfigPath()` function to tell Viper by default to look through a `./conf` directory for any config files. Viper's notable in that users can create this directory and place any config file they want, JSON, YAML, TOML, or even Java Properties files. Viper figures it out.

However, when adding file support to Viper, I found when no config files exist, the `ReadInConfig()` function will return an error with the `viper.ConfigFileNotFoundError` type. This error can throw off error checking, especially if you apply the philosophy of shutting down the application when it cannot load config.

To handle this better, I added a simple switch statement that checks the error type allowing me to take the error and log a warning if the file is not found, but exit if there is a fundamental configuration error.

## Loading Config from Consul

Using Viper to load configuration from Files and Environment Variables is reasonably straightforward. But adding Consul is where things are a bit more confusing, especially if you've used Consul in the past.

When I first attempted to use Viper with Consul, it took me quite a bit of time to figure out what I was doing wrong. The problem ended up being that I wasn't loading the configuration into Consul the way Viper expects it.

Traditionally with Consul, when you add configuration items, they are each counted as a unique key. Consul supports a key path with many subkeys allowing users to manage each configuration key and value independently. For example, a "debug" config parameter would have a key of `go-quick/config/debug`, and its value would be `true`. A "trace" would be `go-quick/config/trace`, and its value would be `false`. 

With Viper, it expects one key, `go-quick/config`, and the value of that key is a JSON, YAML, or another supported format. Rather than having each parameter be a unique key, you must load a string that Viper can parse and understand. 

To explain this easier, let's look at the Consulator config file I use with my project. 

```yaml
go-quick:
  config: '{"from_consul": true, "debug": false, "trace": false}'
```

[Consulator](https://github.com/lewispeckover/consulator) is a handy utility that will read a YAML file (in this case) and load the contents of that YAML file as keys into Consul. In this example, we can see that the key `go-quick/config` is populated with a string that happens to be a JSON. 

Viper will read this JSON, parse it and then apply the values within it. What this means is we can access the `from_consul` value as `cfg.GetBool("from_consul")`.

Once we load the configuration into Consul, the way Viper expects, adding Consul support is pretty straightforward.

```golang
	// Load Config
	cfg.AddConfigPath("./conf")
	cfg.SetEnvPrefix("app")
	cfg.AllowEmptyEnv(true)
	cfg.AutomaticEnv()
	err := cfg.ReadInConfig()
	if err != nil {
		switch err.(type) {
		case viper.ConfigFileNotFoundError:
			log.Warnf("No Config file found, loaded config from Environment - Default path ./conf")
		default:
			log.Fatalf("Error when Fetching Configuration - %s", err)
		}
	}

	// Load Config from Consul
	if cfg.GetBool("use_consul") {
		cfg.AddRemoteProvider("consul", cfg.GetString("consul_addr"), cfg.GetString("consul_keys_prefix"))
		cfg.SetConfigType("json")
		err = cfg.ReadRemoteConfig()
		if err != nil {
			log.Fatalf("Error when Fetching Configuration from Consul - %s", err)
		}
	}
```

To configure Viper to use pull from Consul, we need to use the `AddRemoteProvider()` function, providing it with the Consul address and a key path, both of which I pull from Environment Variables in my example. Before this function works, however, we much first use a blank import to add the Remote Provider functionality to Viper.

```golang
package main

import (
	"github.com/madflojo/go-quick/app"
	"github.com/sirupsen/logrus"
	"github.com/spf13/viper"
	// Add remote provider support to Viper
	_ "github.com/spf13/viper/remote"
)
```

With the Consul address and key path loaded, we also need to use the `SetConfigType()` function to tell Viper which type of format to expect from Consul. Since our example used a string of JSON text, we will set this to `json`.

Once everything is ready, we can call the `ReadRemoteConfig()` function to tell Viper to read and load the configuration from Consul. If Viper found any issues pulling the structure from Consul, it would be returned as an error here.

### Watching Consul for Updates

One of the critical benefits of Consul is the ability to change configuration dynamically. However, by default, Viper doesn't reload configuration changes from Consul. We can, however, add this capability by setting up a scheduled task to reload the configuration.

```golang
	// Setup Scheduler
	scheduler = tasks.New()
	defer scheduler.Stop()

	// Config Reload
	if cfg.GetInt("config_watch_interval") > 0 {
		_, err := scheduler.Add(&tasks.Task{
			Interval: time.Duration(cfg.GetInt("config_watch_interval")) * time.Second,
			TaskFunc: func() error {
				// Reload config using Viper's Watch capabilities
				err := cfg.WatchRemoteConfig()
				if err != nil {
					return err
				}
				return nil
			},
		})
		if err != nil {
			log.Errorf("Error scheduling Config watcher - %s", err)
		}
	}
```

In the example above, I used the [madflojo/tasks](https://github.com/madflojo/tasks) package to create a scheduled task that will call the `WatchRemoteConfig()` function when executed. This function will pull the latest configuration from Consul and update the internal Viper configuration values.

With this recurring task scheduled, we now have a dynamically updated configuration backed by Consul.

### Other Parameters of Consul

In the example above, Viper asks for the Consul address and the Key Path. However, users who know Consul well may notice that there is no specification for a Consul Token. The good news is while Viper itself doesn't ask for these parameters; underneath the covers, Viper uses the Consul API package. That means we can use standard environment variables such as `CONSUL_HTTP_TOKEN` to authenticate with Consul.

To see the list of available environment variables for Consul API, we can reference its [Go Documentation](https://pkg.go.dev/github.com/hashicorp/consul/api#pkg-constants). 

## Summary

This article covered how to add Viper to an existing application and use Viper to load configuration from multiple sources, including Consul. While this article focused on Consul, readers can easily use the examples to connect to other Remote Providers like etcd.

