---
aliases: ["/post/golangs-interfaces-explained-with-mocks/"]
title: "Golang's Interfaces explained with Mocks"
date: 2021-02-15T00:01:00-07:00
draft: false
subtitle: "Learn how to use Go's interfaces by creating a mock."
summary: "This article covers Go interfaces' basics and how you can use them to create modular and testable code."
authors: ["Benjamin Cane"]
tags: ["golang",]
categories: ["Software Engineering"]
featured: true
url: /2021/02/15/golangs-interfaces-explained-with-mocks
---

When I was learning Golang, one of the concepts that took me the most time to grasp was Interfaces. Golang's Interfaces are a great way to make modular and testable code. But they can also be a bit confusing at first glance.

One of the best ways I've found to teach how interfaces work is by creating a mock implementation of an existing Interface. 

This article will cover creating an interface and creating a mock implementation for that Interface. But before we jump into a working example, we should first understand the value of Interfaces.

## Why Interfaces

When thinking about Interfaces, consider them in themselves as contracts. An Interface is a contract that users can import and code their application around. The Interface in itself does nothing; it's a simple contract with no functionality. 

An Interface requires implementations to be useful; an implementation is a Struct with the same Fields and Methods that adhere to the Interface's contract. To explain this better, we will create a simple `Speak` Interface.

```golang
type Speak interface {
        SayHello() string
}
```

From the above, we can see that our `Speak` Interface requires implementations to have a Method called `SayHello`.  By itself, this Interface has no functionality. You can't declare a variable as a `Speak` type and run `SayHello`. We need an implementation to do this.

```golang
type English struct{}

func (e English) SayHello() string {
        return "Hello"
}
```

The above is an example of an implementation that satisfies the `Speak` Interface. In the above, we have a simple Struct named `English`; this Struct also has a Method `SayHello`. Since this implementation has the same Methods and Fields as our `Speak` Interface, we can use it with our Interface.

```golang
package main

import (
        "fmt"
)

type Speak interface {
        SayHello() string
}

type English struct{}

func (e English) SayHello() string {
        return "Hello"
}

func main() {
        var voice Speak

        // Say Hello in English
        voice = English{}
        fmt.Println(voice.SayHello())
}
```

This example shows just how we can use the `English` implementation to fulfill our Interface. We declared our variable `voice` to be of the type `Speak`, we then set the `voice` value to a new `English` instance. Now, any time we execute `voice.SayHello()`, we will use the `English` implementation.

So far, we've shown how you can define an Interface and use a single implementation to satisfy that Interface. But none of this shows how we can use Interfaces to create "modular" code. Let's do that by adding another implementation of our `Speak` Interface.

```golang
package main

import (
        "fmt"
)

type Speak interface {
        SayHello() string
}

type English struct{}

func (e English) SayHello() string {
        return "Hello"
}

type Spanish struct{}

func (s Spanish) SayHello() string {
        return "Hola"
}

func NewVoice(lang string) Speak {
        switch lang {
        case "Spanish":
                return Spanish{}
        default:
                return English{}
        }
}

func main() {
        var voice Speak
        voice = NewVoice("Spanish")
        fmt.Println(voice.SayHello())
}
```

In the above example, we have added a new function `NewVoice()`. Based on the user's input, this function will return either a `Spanish` or an `English` implementation of our `Speak` Interface. This example shows just how we can use Interfaces to create modular programs.

As a user of the Interface throughout our application, we can reference the `voice` variable and use the contracted Methods. No matter how many further implementations we add, we don't have to change our base code, only what `NewVoice()` returns.

Now that we've explored the basics of Interfaces and how they can help us write modular code. We can now explore how Interfaces can also help us write testable code.

## Mocking a Database Interface

Databases are a ubiquitous example of where Interfaces come in handy. Interfaces' modular nature allows us to change the underlying database logic or even platform without modifying the application logic.

From a testing perspective, Interfaces give us a simple way to introduce variability into our code. By creating mock implementations of our `Database` Interface, we can make testing scenarios where the database provides different results. 

This section of the article will first create a simple application that fetches data from a database. We will then create a mock implementation of that database and use it to test how the application behaves with different responses.

```golang
package main

import (
        "fmt"
)

type Database interface {
        Fetch(key string) (int, error)
}

var DB Database

func isOver9000() bool {
        i, err := DB.Fetch("powerlevel")
        if err != nil {
                // if this were a real program, this should return an error
                // but this is an example, so it's ok.
                return false
        }

        if i > 9000 {
                return true
        }

        return false
}

func main() {
        if isOver9000() {
                fmt.Println("It's over 9000!!!")
        }
}
```

The above example application is relatively simple. We have a simple `Database` Interface with a single method, `Fetch`. We also have an instance of this Interface named DB. DB is used to retrieve database records, and based on the results; our function returns either a `True` or a `False`.

While this example is simplistic, it's a great start to show how creating a mock can help test application logic. To get started making our mock, we will start our `main_test.go` file. Within this file, we will create our Mock implementation of the `Database` Interface.

```golang
type MockDB struct {
        // FakeFetch is used to provide unique test case results
        FakeFetch func(string) (int, error)
}

func (m *MockDB) Fetch(k string) (int, error) {
        if m.FakeFetch != nil {
                return m.FakeFetch(k)
        }
        return 0, nil
}
```

In this implementation, we can see something a bit more sophisticated from our original example. Our `MockDB` Struct has a Field called `FakeFetch`, which is a `func()` type. What's more interesting is that the `FakeFetch` will execute within our `Fetch` method.

This setup is something I've found useful when creating Mocks. Users who use this `MockDB` type to mock DB can define what they want the `Fetch` method to return. This part will be more apparent as we create the individual tests. What is more important to call out is the `m.FakeFetch(...)` call.

When defining Struct methods, we also define a receiver, `m` in this case. Users can use the receiver to reference internal values within the Struct. This use of the `m` receiver is what we are doing with `FakeFetch`. As the users define the `MockDB` instance, they are also creating the `FakeFetch` function. As our method executes, the user-defined `FakeFetch` is then also called. To understand this concept better, let's take a look at some tests using this `MockDB` implementation.

```golang
func TestIsOver9k(t *testing.T) {
        t.Run("TestOver9000", func(t *testing.T) {
                DB = &MockDB{
                        FakeFetch: func(string) (int, error) {
                                return 9001, nil
                        },
                }
                if !isOver9000() {
                        t.Errorf("Test did not return expected results")
                }
        })

        t.Run("TestUnder9000", func(t *testing.T) {
                DB = &MockDB{
                        FakeFetch: func(string) (int, error) {
                                return 8999, nil
                        },
                }
                if isOver9000() {
                        t.Errorf("Test did not return expected results")
                }
        })

        t.Run("TestDBError", func(t *testing.T) {
                DB = &MockDB{
                        FakeFetch: func(string) (int, error) {
                                return 0, fmt.Errorf("unable to connect to database")
                        },
                }
                if isOver9000() {
                        t.Errorf("Test did not return expected results")
                }
        })
}
```

In the above, we can see that each test execution defines a different behavior for the `DB.Fetch()` method call. In turn, each of these tests drives different return values from our `isOver9000()` function. In one test, we fake a result over `9000`, which causes our `isOver9000()` function to return `True`.

In another test, we return an error from the database forcing the `isOver9000()` function to return `False`. These tests show just how easy it can be to use Interface mocks to test application logic and, sometimes, more importantly, error handling within applications.

## Summary

With this article, we have explored Golang's Interfaces' basics and how we can use them to create both modular and testable code. While the examples may have been rudimentary, they should serve as a good starting point.

For more examples of how we can use Interfaces, I'd suggest checking out one of my side projects, [Hord](https://github.com/madflojo/hord). Hord aims to be a friendly Interface for key/value databases. As part of this package, I created a [Mock database driver](https://github.com/madflojo/hord/blob/master/drivers/mock/mock.go) that makes it easy for Hord users to test application logic driven by database results.

