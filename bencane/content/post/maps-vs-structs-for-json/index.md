---
title: "Golang working with JSON: Maps vs. Structs"
subtitle: "Which is the best method for parsing JSON and why?"
summary: "This article covers how to use maps and structs to parse JSON, which is better and safer. It also covers how to work with maps safely."
date: 2020-12-08T00:29:19-07:00
authors: ["Benjamin Cane"]
tags: ["golang",]
categories: ["Software Engineering"]
featured: true
draft: false
url: /2020/12/08/maps-vs-structs-for-json
aliases: ["/post/maps-vs-structs-for-json/"]
---

Before learning Go, I used to write most of my applications in Python. When I was transitioning from Python to Go, I was familiar with parsing JSON, YAML, etc., into Python dictionaries. What I never understood is why I would see so many examples parsing JSON into Go structs. Why not use maps, which are equivalent to a Python dictionary.  What were the benefits of using structs vs. maps, or were maps some secret technique that Python taught me that all these Gophers didn't know?

The truth is, it all depends on how we use the JSON data; in some cases, maps work better than structs. In most cases, structs are safer than maps.

In today's article, I will explore the benefits of these techniques and highlight where one might be more useful than the other.

## Parsing JSON in Go

To start breaking down these techniques, let's first establish the differences between parsing a JSON into a map and parsing into a struct. We can use the following JSON as an example throughout our article.

```json
{
	"name": "example",
	"numbers": [
		1, 2, 3, 4
	],
	"nested": {
		"isit": true,
		"description": "a nested json"
	}
}
```

This JSON is a useful example because it addresses several types of data, including nesting JSON. This nesting will help highlight differences in the parsing methods of maps and structs.

### Parsing JSON with Maps

We will first start parsing our JSON into a map. Once we've parsed the JSON, we can begin breaking down the code and explaining how to access our data once it is within a map. 

The code snippet below is what we will use to parse our JSON.

```golang
package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	// Create a map to parse the JSON
	var data map[string]interface{}

	// Define a JSON string
	j := `{"name":"example","numbers":[1,2,3,4],"nested":{"isit":true,"description":"a nested json"}}`

	// Parse our JSON string
	err := json.Unmarshal([]byte(j), &data)
	if err != nil {
		fmt.Printf("Error parsing JSON string - %s", err)
	}

	// Print out one of our JSON values
	fmt.Printf("Name is %s", data["name"].(string))
}
```

To parse the JSON, we can see from the code we first created a `map[string]interface{}` called `data`. Then we took our JSON string and used the `Unmarshal()` function to populate the `data` map. So far, this seems pretty easy and straightforward.

As far as parsing goes, the nice thing about this method is we don't need to know much about the JSON structure to parse it. Everything goes into the map, and because the map is of `interface{}` types, it can hold whatever we want.

That concept of using an `interface{}` type is where things get complicated.

In the example above, we parse the JSON and then use `Printf()` to print a JSON field. The way we print that field, though, is very unsafe.

The first problem is, by just tossing `data["name"]` into the `Printf()` function, we are assuming that the field is actually within the JSON. But what if it isn't? The bad news is, our program would panic because we tried to access a value that doesn't exist.

To access our data in a way that checks for its existence, we need to do the following.

```golang
	// Print out one of our JSON values
	n, ok := data["name"]
	if !ok {
		// access it another way
		n = "default"
	}
	fmt.Printf("Name is %s", n.(string))
```

This method uses the "comma ok" pattern to determine if the map has a key named `name`. If it does, the `ok` value will be `true`; if not, the `ok` value will be `false`. This pattern makes our code safe from missing map values, but it's still not 100% safe. 

Our code above uses type assertion to declare that the `name` value is a string type. But what if it's not a string? JSON allows for many different types. When parsing with maps, the values are not type enforced. Meaning, everything is an interface until you tell it otherwise. Suppose we were to parse a JSON where the `name` key held a boolean instead of a string. Our code, as it stands today, would once again panic.

It is unsafe to assume you know the type of value a JSON map is going to hold. This rule is especially true when working with API's where users provide the input JSON. To safely assert type, we need to use the "comma ok" pattern once again.  

```golang
	// Print out one of our JSON values
	n, ok := data["name"]
	if !ok {
		// access it another way
		n = "default"
	}
	v, ok := n.(string)
	if !ok {
		// figure out type another way
		v = "default"
	}
	fmt.Printf("Name is %s", v)
```

Now our code is finally safe to access the name data without any panics. But that took a lot of work for just one field. What does it take for a more complex field like our numbers list? Let's take a look.

```golang
	// Print out the JSON Numbers
	var nums []int
	i, ok := data["numbers"].([]interface{})
	if ok {
		for _, v := range i {
			x, ok := v.(float64)
			if !ok {
				// set to default
				nums = []int{}
				break
			}
			nums = append(nums, int(x))

		}
	}
	fmt.Printf("Numbers are")
	for _, v := range nums {
		fmt.Printf(" %d", v)
	}
	fmt.Printf("\n")
```

Our numbers are a lot more complicated because we have an array within our JSON. Any array is parsed and placed into the map as an array of interfaces. In this example, we are both checking for key existence and type asserting it's value to a `[]interface{}` with a single "comma ok" check. 

But our assertions don't stop there; now we need to loop through the values and type assert each value individually. Where this gets tricky is when our values are not numbers. Technically, our JSON could have mixed types in this array; it could provide us with integers and strings. As we check each value individually, we also need to put in logic that verifies the whole list's integrity. 

When it comes to complicated JSON's like this, maps can be very problematic when using the data. The reason is that you have to account for all sorts of variations in your code. If you forget to type assert one value or forget to check if a key exists, your program will crash. 

### Parsing JSON with structs

When parsing JSON with maps, it is not necessary to define the structure of the JSON in code. With structs, the opposite is true. When using structs, it's vital to describe all of the JSON elements needed in code.

Let's look at a simple parser that prints the name field as we did with the previous example.

```golang
package main

import (
	"encoding/json"
	"fmt"
)

// Example is our main data structure used for JSON parsing
type Example struct {
	Name    string `json:"name"`
	Numbers []int  `json:"numbers"`
	Nested  Nested `json:"nested"`
}

// Nested is an embedded structure within Example
type Nested struct {
	IsIt        bool   `json:"isit"`
	Description string `json:"description"`
}

func main() {
	// Define a JSON string
	j := `{"name":"example","numbers":[1,2,3,4],"nested":{"isit":true,"description":"a nested json"}}`

	// Parse JSON string into data object
	var data Example
	err := json.Unmarshal([]byte(j), &data)
	if err != nil {
		fmt.Printf("Error parsing JSON string - %s", err)
	}

	// Print the name
	fmt.Printf("Name is %s", data.Name)
}
```

A significant difference in this example vs. our original map example is that this code is safe. No matter what the JSON input looks like, our code is panic free.

When using structs to parse JSON, the JSON parser itself handles all of the type assertions. When we define our structs, we set our types; if these fields hold any other type, our `Unmarshal()` call will return an error.

Let's take a closer look at our struct definition.

```golang
// Example is our main data structure used for JSON parsing
type Example struct {
	Name    string `json:"name"`
	Numbers []int  `json:"numbers"`
	Nested  Nested `json:"nested"`
}

// Nested is an embedded structure within Example
type Nested struct {
	IsIt        bool   `json:"isit"`
	Description string `json:"description"`
}
```

In our struct, we can see there is a `Name` field defined as a string. We can also see we are using the JSON parsers tags to associate the `Name` struct field with the `name` JSON field. These definitions are essential, the tags help the JSON parser figure out where a JSON field's data needs to go, and the type within the struct is what enforces whether the parser can populate the JSON data within that field.

When parsing JSON with structs, all the work to perform type assertions is upfront, a safer and more comfortable way of working with JSON. To drive this point home, we can look at how easy it is to access the other JSON elements via structs.

```golang
	// Print the name
	fmt.Printf("Name is %s\n", data.Name)

	// Print the Numbers
	fmt.Printf("Numbers include")
	for _, v := range data.Numbers {
		fmt.Printf(" %d", v)
	}
	fmt.Printf("\n")

	// Print the Description
	fmt.Printf("Description is %s", data.Nested.Description)
```

As we can see, the way to access data is simple. Using structs, we can use the data assuming it is either there or, worst case, a default value such as an empty list or string.

With it being so easy to use structs, it might seem like we should always use structs, but it's not that simple.

## Summary: When to use Maps vs. Structs

As we saw from this article, using structs are a safe and easy way to access JSON data. We can also see that using maps is generally unsafe and require extra work to use the data safely once parsed.

So why ever use maps instead of structs? The answer is simple.

When using structs, we must define every element within the JSON into the struct. We have to know the field name and data type of each JSON element while writing our code. This limit is sufficient for most use cases, APIs, configuration, or anything else where the data names and types are static.

However, there are times when we don't know the JSON structure in advance when we need to parse an unknown JSON; that's where maps come in handy. An example of this could be an API where the server must respond to the client with all the original request elements. If we used a struct for this case, the parser would drop any unknown fields. 

While use cases that require maps are somewhat limited, they exist, and it's useful to know when and when not to use this method.

