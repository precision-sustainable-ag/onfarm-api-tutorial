# PSA API Tutorial

## 1. Setting up your environment:
### R:
1. Load two packages from your R console:
```r
install.packages(c("httr", "jsonlite"))
```
2. That's it!
---


### Python:
1. Install two packages (`{requests}`, `{pprint}`) from the terminal:
```sh
pip install requests pprint
```

2. Alternatively inside a Jupyter notebook:
```python
import sys
!{sys.executable} -m pip install requests
!{sys.executable} -m pip install pprint
```

---

## 2. The structure of an API call:

### What is an API?

An API (Application Programming Interface) is any method by which two computers talk to each other. That definition is so broad as to be useless, so we're going to specifically talk about "HTTP requests" and "API calls" interchangeably.

HTTP requests use a handful of "verbs" to communicate what you want, but we're going to only discuss the **`GET`** method. A **GET** API call is what your browser is doing when you visit a website by typing in the address bar. Some other words you might hear thrown around are:
 - `curl`/`libcurl`/`wget` (libraries that run on your computer to make API calls)
 - **REST** (a style of API design)
 - **client** (that's you! or your script)
 - **server** (that's the computer on the other end)

The anatomy and more vocab will be broken down in the **How** section below.

### Why is an API?

### How is an API?

# Basic call structure
A typical API call from the command line might look like this, which will generate a random number and tell you a fact about it.

```sh
curl -X GET "http://numbersapi.com/random"
```

 - `curl` is the command line program that does the call
- `-X GET` is a flag that says we're making a **`GET`** request
- `"http://numbersapi.com"` is the **URL**
- `"/random"` is the **endpoint**

The URL is the name of the computer you're talking to, just like going to a URL in your browser. An endpoint is telling the other computer what kind of data you're after. What if you need to be more specific about the kind of data you want? For that you need a **query**, like this one where we restrict our random number to a range:

```sh
curl -X GET "http://numbersapi.com/random?min=10&max=20"
```
Now we've added `?` which starts the query string, and passed in two **parameters**: `min` of 10 and `max` of 20.
> Notice that multiple parameters are connected with an ampersand **`&`** and that parameters are key/value pairs designated with an equals sign **`=`**.

> There are restrictions on what characters you can use in a query string. No spaces and only certain punctuation are allowed.

Not all APIs are open and free like this toy one. Sometimes you need to identify yourself with an **API key**. This is a way for the server to verify who you are, what permissions you have, and how much you're using a service. Sometimes API keys are passed in the query string as parameters, but often nowadays they're passed as **headers**:

```sh
curl -H "my-custom-header: my-custom-token" -X GET "https://httpbin.org/anything?param=500"
```

The `-H` flag says we're passing an additional header, and the string after identifies it. There are other headers your computer is sending that you don't specify, like a **user agent**, which is the name of the program you're using.

This is all fine for making a single request, but you probably want to make multiple requests from your data analysis environment. For this, there are packages that make specifying these strings a lot easier dynamically. We'll talk about those in the last section below.

## 3. How to get and use your API key:

We have three main APIs that we currently maintain, all at https://api.precisionsustainableag.org:

 - `/onfarm` - The PSA on-farm experiment data
 - `/SSURGO` - A wrapper that returns data from the NRCS soil survey
 - `/weather` - A database of gridded weather data pulled from public sources and archived for PSA sites

 To get your API key, you need to contact Brian (bwdavis3@ncsu.edu) and get signed up. It will look like this: `57aaf904-e915-11eb-90d2-001dd801118b`. To use your API key, pass it as the custom header:

 ```
 "x-api-key: 57aaf904-e915-11eb-90d2-001dd801118b" 
 ```

You can find the documentation for all of these by going to the address above in your browser. There you can read which endpoints each API has, and what query parameters you can pass.

## 4. Putting it all together:

