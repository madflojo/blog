---
aliases: ["/post/how-to-structure-a-golang-cli-project/"]
title: "How to Structure a Go Command-Line Project"
date: 2020-12-29T00:01:00-07:00
draft: false
subtitle: "A detailed example of a Go project structure, specifically for command-line tools."
summary: "Best practices around structuring Go command-line applications where packages go, parse command-line arguments, and optimize for testing."
authors: ["Benjamin Cane"]
tags: ["golang",]
categories: ["Software Engineering"]
featured: true
aliases: ["/post/how-to-structure-a-golang-cli-project/"]
url: /2020/12/29/how-to-structure-a-golang-cli-project
---

I was recently restructuring one of my early [Go side projects](https://github.com/madflojo/efs2). As I was changing the project layout, I was reminded there are many recommendations out there but no set standard for structuring Golang projects.

In other programming languages such as Java, there is a typical project layout that most programmers follow inherently. In Python, the framework used (i.e., Django or Flask) will define how the project is structured. However, Go is still at a point where the community hasn't settled on a defacto standard.

There are, however, some strong recommendations, but as I was going through those recommendations, I found they didn't wholly work for my project. 

This article will discuss how I ultimately structured my project (which isn't too different from general recommendations) and standard best practices.

## Make your code modular with well-designed packages

The first best practice to mention is any code within your application that can be re-used should be a package. How to structure packages and best practices around packages could be an article in itself. I have a talk that discusses this very topic. Rather than repeating that talk here, I'd suggest looking at the [slides](https://go-pkg-structure.dev/) for that talk.

I will say, though, that breaking code out into packages holds more benefits than just re-use. From a project structure perspective, it helps to group code with a common purpose together. It makes it easier for others to find and contribute, an important attribute, especially for Open Source projects. Packages also often make code easier to test. By isolating functionality into a package, we can then test that functionality with fewer dependencies.

When I start a new project or start restructuring an existing project, I will usually first write down the different packages I need. Sometimes, I even go ahead and create the base package structure before writing any other code and refactor/add code as I go.

## Split Entry-Point code from Application code 

Another best practice that I've seen across most project layout recommendations is to separate application code from entry-point code. What I mean by entry-point code is the `main` package and `main()` function.

With Go, like other languages, the entry-point for an application is the `main()` function. When an application starts, this is the first function executed, and it is very tempting to put all of the core application functionality within this function. Rather than dumping all of the runtime code into the `main` package, the better practice is to create an `app` package.

There are several advantages to placing core application logic within its own package. My personal favorite is how it makes testing easier. A common pattern would be to create both `Start()` and `Stop()` or `Shutdown()` functions for this `app` package. When creating tests, having the ability to start and stop the core application functionality makes it a lot easier to write tests that execute against the core logic.

Below is an example structure for an `app` package.

```golang
package app

import (
	"fmt"
)

var ErrShutdown = fmt.Errorf("application was shutdown gracefully")

func Start(...) error {
	// Application runtime code goes here
}

func Shutdown() {
	// Shutdown contexts, listeners, and such
}
```

The above is an excellent recommendation when creating a command-line project that is both a server and a command-line interface (CLI) client. By having the application code in a shared package, both the server and the CLI client can share this core `app` package.

However, this recommendation isn't as relevant to simple command-line utilities. These utilities tend to start, perform an action, and stop. But even for these types of applications, I like following the `app` package recommendation. It makes it easier to group runtime logic, which lowers others' barriers to understand the codebase.

### So what does go into the main package?

With all of our application core in the `app` package, it makes sense to wonder what we would put in the `main` package. The answer is simple, very little.

In general, I restrict the `main` package to the code that interacts with users of the resulting binary. For example, if I am working on a project that has both a CLI client and a server, I will often put command-line argument parsing in the `main` package. The reason is both the server and the CLI client binaries will have different `main` packages (more on this later). By parsing arguments in the `main` package, I can easily create unique options for a CLI client that don't apply to the server, and vice versa.

Anything that the command-line utility's user interacts with is something I tend to put into the `main` package. A few examples of this would include:

- Command-line argument parsing
- User input (if it's simple and not part of the core application logic)
- Config file parsing
- Exit codes
- Signal Traps

The below code snippet is an example of the `main()` function from my side project; from this example, we can see just how little goes into this package.

```golang
// main runs the command-line parsing and validations. This function will also start the application logic execution.
func main() {
	// Parse command-line arguments
	var opts options
	args, err := flags.ParseArgs(&opts, os.Args[1:])
	if err != nil {
		os.Exit(1)
	}

	// Convert to internal config
	cfg := config.New()
	cfg.Verbose = opts.Verbose
	// more taking command line options and putting them into a config struct.

	if opts.Pass {
		// ask the user for a password
	}

	// Run the App
	err = app.Run(cfg)
	if err != nil {
		// do stuff
		os.Exit(1)
	}
}
```

## A recommended directory structure

One of the most common project structure recommendations is one that uses the following directory structure.

- `internal/app` - Place the core application logic in this `app` package.
- `internal/pkg/` - Place any internal-only packages here (not `app` though).
- `pkg/` - Place any externally shareable packages here.
- `cmd/<app_name>` - Place the `main` package here under a directory with application name

A big part of this recommendation is splitting the application core into `internal/app` and the entry-point code into a `cmd/<app_name>` directory.  As discussed earlier, this layout is excellent for projects with multiple binaries to build (i.e., server and CLI client). A `cmd/<app_name>` directory could contain a `main` package for creating a CLI client, and a `cmd/<app_name>-server` directory could contain a different `main` package unique for creating a server. But both of these can leverage the shared `internal/app` package.

Overall this is a pretty good structure, but I found it doesn't exactly work for my side project. So what did I do differently?

### I put packages in a different location.

The first thing I do a bit different than the recommendation above is where I put packages. I am not a fan of application projects (it's different for stand-alone packages) with many sub-directory layers. In my opinion, having a lot of sub-directories makes it very difficult to find where functionality belongs. 

For substantial projects with a lot of code, having a structure like this may be necessary, but I feel it's overkill for small to medium projects.

Instead, I like to place all of my packages at the top-level directory of the project. For example, if I have a Parser package, it would be located within `parser/`, an SSH package within `ssh/`, and of course, the `app` package is within the `app/` directory.

This practice makes it very easy to find packages and functionality as they are all in the top-level directory. Again, this only works for projects with a limited number of packages. If the project grows into many packages, it may be cleaner to place them into a `pkg/` directory.

### I ignored the Internal vs. Pkg directory approach.

Another recommendation that I'm not a fan of is splitting packages into `internal/` vs. `pkg/` directories. The main reason is that this recommendation is for in-app packages, and when dealing with in-app packages, I don't see a clear line between internal and external packages.  In the name of internal-only packages, I've seen many developers skip best practices because "no one else is going to use it...".

I also don't accept that developers will maintain packages within `pkg/` like a stand-alone package. In reality, these packages' interfaces are very likely to change as they are packages within an application. If they were genuinely stand-alone, they would be an independent project. 

For me, it makes more sense to put all of my in-app packages in the same general location. Either at the top-level of the project or within a `pkg/` directory.

### I didn't use the `cmd/` directory.

While I am a fan of using the `cmd/` directory, I had a problem with this recommendation for my side-project. 

My project is a simple command-line utility that will always be just a CLI tool. One of the things I want to do is make it easy for my users to install this utility. The easiest and fastest way is to let users install via the `go get` command, as shown below.

```console
$ go get -u github.com/madflojo/efs2
```

When users install my command-line tool via the command above, I want them to reference the repository URL only. The problem with the above recommendation is that my users would have to add `/cmd/<app_name>` to the URL like the below example.

```console
$ go get -u github.com/madflojo/efs2/cmd/efs2
```

This URL format isn't the end of the world, but it's a bit messy; users must know my project structure to install my application. I want my layout to make it easier for people to install, not harder.

Rather than placing my minimal main package in the `cmd/` directory. I put my `main.go` file in the top-level directory of my project. This change allows my users to run the `go get` command with the primary project path while still allowing me to follow the practice of keeping this code minimal with the core application functionality in an `app` package.

## Summary

With the above patterns and practices, the result has my side-project using the following structure. 

```golang
$ tree -L 2
.
├── CONTRIBUTING.md
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── app
│   ├── app.go
│   └── app_test.go
├── config
│   ├── config.go
│   └── config_test.go
├── dev-compose.yml
├── go.mod
├── go.sum
├── main.go
├── parser
│   ├── parser.go
│   └── parser_test.go
├── ssh
│   ├── ssh.go
│   └── ssh_test.go
└── vendor
    ├── github.com
    ├── golang.org
    └── modules.txt

7 directories, 18 files
```

Overall I am happy with it. New contributors can quickly identify which packages perform different functions. This visibility is there when someone looks at the directory names and when using the [Go Reference documentation](https://pkg.go.dev/github.com/madflojo/efs2).

I've also found that breaking out my application core into a package has helped me improve my code coverage. While it may be uncommon, I've yet to see any downfalls to putting my minimal `main` package in the top-level directory.

As some read this article, I expect they may not like some of the changes I've made over the recommended standards. But this is what I've found works for me, it may work for others, or it may not. 
