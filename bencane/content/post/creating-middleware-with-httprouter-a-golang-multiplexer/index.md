---
title: "Creating Middleware with httprouter"
date: 2021-08-08T00:40:06-07:00
draft: false
subtitle: "Using a Golang HTTP Multiplexer to create HTTP middleware."
summary: "Learn how to use the httprouter Go mux to route your custom handlers HTTP requests and create common functions for all handlers, even those pesky ones like PProf."
authors: ["Benjamin Cane"]
tags: ["golang",]
categories: ["Software Engineering"]
featured: true
aliases: ["/post/creating-middleware-with-httprouter-a-golang-multiplexer"]
url: /2021/09/08/creating-middleware-with-httprouter-a-golang-multiplexer
---

When working with HTTP-based services in Go, many developers (including myself) like to use HTTP Multiplexers (mux). Multiplexers, also sometimes referred to as Request Routers, offer a suite of features and capabilities. The simplest form allows users to register a specific handler 
function with specific URL patterns and methods.

One of the more advanced features is using HTTP Multiplexers to create "HTTP middleware." This capability allows users to create a standard function or set of executed functions before requests route to the User-defined handlers. Developers can use these common functions to perform many tasks, from creating a standard logger to handling authentication.

Today's article will explore using the httprouter HTTP Multiplexer to create a simple HTTP middleware. 

## Why httprouter

There are many Multiplexers available, with popular ones being [Gorilla Mux](https://github.com/gorilla/mux), [httprouter](https://github.com/julienschmidt/httprouter), and [Bone](https://github.com/go-zoo/bone). For this article, I will explore httprouter, one I often use because I like how simple and efficient it is. But also because there is a version available for both `net/http` and `fasthttp`. I use both of these HTTP packages throughout my various projects. And having one HTTP Multiplexer to use regardless of which I'm using helps keep things simple.

## Getting Started with httprouter

Before jumping into creating an HTTP middleware function, we should first start with the basics of using httprouter. We can look at the most basic HTTP service that prints "Hello World" to kick us off.

```golang
package main

import (
        "fmt"
        "log"
        "net/http"
)

// handler is a basic HTTP handler that prints hello world.
func handler(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hello World")
}

func main() {
        // Register our handler function
        http.HandleFunc("/hello", handler)

        // Start HTTP Listener
        err := http.ListenAndServe(":8080", nil)
        if err != nil {
                log.Printf("HTTP Server stopped - %s", err)
        }
}
```

The above code only uses the standard `net/http` and the default mux with the standard library. One of the nice things about Go is that the standard library is all you need if you build elementary HTTP-based services.

But for this article, we want to do something more advanced; we want to have a standard HTTP middleware executed before our HTTP handler.

To get started, let's add httprouter into the mix.

```golang
package main

import (
        "fmt"
        "github.com/julienschmidt/httprouter"
        "log"
        "net/http"
)

// handler is a basic HTTP handler that prints hello world.
func handler(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
        fmt.Fprintf(w, "Hello World")
}

func main() {
        // Create Router
        router := httprouter.New()
        router.GET("/hello", handler)

        // Start HTTP Listener
        err := http.ListenAndServe(":8080", router)
        if err != nil {
                log.Printf("HTTP Server stopped - %s", err)
        }
}
```

As we can see from the code example above, we made a few changes to our code. The first to call out is rather than using `http.HandleFunc()` to register our `handler` function, we created an `httprouter.Router` and used this to register our `handler` function for the `/hello` end-point.

A keen eye may also notice that with httprouter, we can register our functions under different HTTP Methods. This feature is one of the excellent features of httprouter over the default standard library. With httprouter, users can register different functions for different HTTP Methods. In our example, it doesn't make sense to serve the `/hello` route under any method other than a GET.

In addition to the changes in how we register our `handler` function, it is worth calling out that the signature of our `handler` function has also changed. Now, in addition to the standard `http.ResponseWriter` and the `http.Request` types, our function also receives an `httprouter.Params` type.

With httprouter, one of the more advanced features is the ability to parameterize the URI. For example, instead of registering `/hello`, we could register `/hello/:name`. We could ask users to put their names within the URI, such as `/hello/ben`. We could then access that parameter using the `httprouter.Params` provided to our handler.

```golang
// handler is a basic HTTP handler that prints hello world.
func handler(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
        fmt.Fprintf(w, "Hello %s", ps.ByName("name"))
}
```

We now have a fully working HTTP service using httprouter; we can start creating our middleware function from here.

### Creating our HTTP Middleware

For this article, we will create a basic logger middleware. This middleware aims to create a consistent log of HTTP requests regardless of what HTTP handler executes. That means before our `handler()` function executes, we want our middleware to run first.

We will achieve this by creating a wrapper function and then including this wrapper function with our `handler()` registration call.

```golang
package main

import (
        "fmt"
        "github.com/julienschmidt/httprouter"
        "log"
        "net/http"
)

// handler is a basic HTTP handler that prints hello world.
func handler(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
        fmt.Fprintf(w, "Hello %s", ps.ByName("name"))
}

// middleware is used to intercept incoming HTTP calls and apply general functions upon them.
func middleware(n httprouter.Handle) httprouter.Handle {
        return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
                log.Printf("HTTP request sent to %s from %s", r.URL.Path, r.RemoteAddr)

                // call registered handler
                n(w, r, ps)
        }
}

func main() {
        // Create Router
        router := httprouter.New()
        router.GET("/hello/:name", middleware(handler))

        // Start HTTP Listener
        err := http.ListenAndServe(":8080", router)
        if err != nil {
                log.Printf("HTTP Server stopped - %s", err)
        }
}
```

In the above, we can see our wrapper function `middleware()` is now being registered along with the `handler()` function. The name of this technique is chaining; by wrapping the `handler()` function with the `middleware()` function, we are chaining the two functions together. The `middleware()` function executes first, and at the end, the `middleware()` function itself calls our `handler()` function.

At this point, we have a working HTTP middleware powered by httprouter. For every custom handler we have, we can use this HTTP middleware to keep a consistent log. But what about non-custom handlers? What about things like [PProf](https://pkg.go.dev/net/http/pprof) that has their handlers built with the standard HTTP signature?

### Registering non-Custom Handlers with the HTTP middleware

A common practice for libraries such as PProf is to provide HTTP handlers as part of the package interface. The `net/http/pprof` package has several functions that adhere to the standard `net/http` method signature. Functions such as Index, which handles the `/debug/pprof/` end-point, and Profile, which serves the `/debug/pprof/profile` CPU profiling end-point.

The problem is that these functions only take two inputs, `http.ResponseWriter` and `http.Request`. They don't match our HTTP middleware's signature, but we still want to use our middleware for these functions.

Luckily, we can. Using the `http.HanderFunc()` adapter we can convert these functions into `http.Handler`'s. And from there, we can use another small wrapper to wrap this `http.Handler` with our middleware.

```golang
package main

import (
        "fmt"
        "github.com/julienschmidt/httprouter"
        "log"
        "net/http"
        "net/http/pprof"
)

// handler is a basic HTTP handler that prints hello world.
func handler(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
        fmt.Fprintf(w, "Hello %s", ps.ByName("name"))
}

// middleware is used to intercept incoming HTTP calls and apply general functions upon them.
func middleware(n httprouter.Handle) httprouter.Handle {
        return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
                log.Printf("HTTP request sent to %s from %s", r.URL.Path, r.RemoteAddr)

                // call registered handler
                n(w, r, ps)
        }
}

// wrapper will wrap an http.Handler function with the middleware function.
func wrapper(h http.Handler) httprouter.Handle {
        return middleware(func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
                h.ServeHTTP(w, r)
        })
}

func main() {
        // Create Router
        router := httprouter.New()
        router.GET("/hello/:name", middleware(handler))
        router.GET("/debug/pprof", wrapper(http.HandlerFunc(pprof.Index)))

        // Start HTTP Listener
        err := http.ListenAndServe(":8080", router)
        if err != nil {
                log.Printf("HTTP Server stopped - %s", err)
        }
}
```

As we can see from the code above, we added a `wrapper()` function with an input of `http.Handler`, and that wrapper function is wrapping an anonymous function running `http.Handler.ServeHTTP()` with our middleware.

With the addition of this `wrapper()` function, we can now introduce our HTTP middleware on any standard HTTP handler, whether it's from PProf or other libraries.

Now that we have our `wrapper()` function defined, let's go ahead and add the rest of the PProf parts.

```golang
package main

import (
        "fmt"
        "github.com/julienschmidt/httprouter"
        "log"
        "net/http"
        "net/http/pprof"
)

// handler is a basic HTTP handler that prints hello world.
func handler(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
        fmt.Fprintf(w, "Hello %s", ps.ByName("name"))
}

// middleware is used to intercept incoming HTTP calls and apply general functions upon them.
func middleware(n httprouter.Handle) httprouter.Handle {
        return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
                log.Printf("HTTP request sent to %s from %s", r.URL.Path, r.RemoteAddr)

                // call registered handler
                n(w, r, ps)
        }
}

// wrapper will wrap an http.Handler function with the middleware function.
func wrapper(h http.Handler) httprouter.Handle {
        return middleware(func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
                h.ServeHTTP(w, r)
        })
}

func main() {
        // Create Router
        router := httprouter.New()
        router.GET("/hello/:name", middleware(handler))
        router.GET("/debug/pprof/", wrapper(http.HandlerFunc(pprof.Index)))
        router.GET("/debug/pprof/cmdline", wrapper(http.HandlerFunc(pprof.Cmdline)))
        router.GET("/debug/pprof/profile", wrapper(http.HandlerFunc(pprof.Profile)))
        router.GET("/debug/pprof/symbol", wrapper(http.HandlerFunc(pprof.Symbol)))
        router.GET("/debug/pprof/trace", wrapper(http.HandlerFunc(pprof.Trace)))
        router.GET("/debug/pprof/allocs", wrapper(pprof.Handler("allocs")))
        router.GET("/debug/pprof/mutex", wrapper(pprof.Handler("mutex")))
        router.GET("/debug/pprof/goroutine", wrapper(pprof.Handler("goroutine")))
        router.GET("/debug/pprof/heap", wrapper(pprof.Handler("heap")))
        router.GET("/debug/pprof/threadcreate", wrapper(pprof.Handler("threadcreate")))
        router.GET("/debug/pprof/block", wrapper(pprof.Handler("block")))

        // Start HTTP Listener
        err := http.ListenAndServe(":8080", router)
        if err != nil {
                log.Printf("HTTP Server stopped - %s", err)
        }
}
```

In the above example, a keen eye may notice that about halfway through registering `/debug/pprof` paths, we stop using the `http.HandlerFunc()` adapter. Instead, we are registering a `pprof.Handler()` function with various arguments. Some paths are satisfied with the PProf package via the `pprof.Handler()` function, which returns an `http.Handler` type.

## Summary

With the above, we have a simple hello world application that shows how easy it is to create HTTP Middleware functions with httprouter. We can also see how it is possible to use this middleware even with packages like PProf, where the HTTP handlers use a different signature.

If you build a complex service with many routes and different handlers, routers such as httprouter can be a great tool. But the best thing about Go is, if all you need to do is simple HTTP services, you don't need much beyond the standard library.



