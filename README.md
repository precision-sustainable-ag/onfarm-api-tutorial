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

### SAS:

1. The libraries are pre-installed, nothing else to do!

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

There are two advantages of APIs for our purposes: data complexity, and data quality.

1. Some of the data collected by the on-farm team is highly complex, and stored across multiple tables. If you had to download each table from the database and join them yourself, there's a likelihood of an error or a misunderstanding of the metadata. By using an API, we store all that logic on one place in the server, and reuse it for every user.

2. The data coming in from a source may change over time, whether there's new entries, or entries have been edited because of errors. Calling an API at the top of your script ensures you have the highest quality data at that moment, as opposed to whatever the state was at the time you downloaded a CSV.

### How is an API?

#### Basic request structure
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

#### Basic response structure

So far we've talked about is how to do the asking, but not how the server does the answering. The response a server returns to the client is called the **response**, and it has headers as well as a **body**, also called the **content**.

The format of the response body might be something you specify in your request, or there might only be one format available. You can only tell this by trying it out and reading the documentation of a particular API. However, a common format is what's called **JSON** (Javascript Object Notation), and it looks like this:

```json
{
    "sometext": "this is text",
    "somenumbers": [0,1]
}
```

JSON is human-readable, and a standard format for computers to communicate in. You can even use an array of JSON objects to represent rows of a table (here, the well-known **iris** data):

```json
[
    {
        "Sepal.Length": 5.1,
        "Sepal.Width": 3.5,
        "Petal.Length": 1.4,
        "Petal.Width": 0.2,
        "Species": "setosa"
    },
    {
        "Sepal.Length": 4.9,
        "Sepal.Width": 3,
        "Petal.Length": 1.4,
        "Petal.Width": 0.2,
        "Species": "setosa"
    },
    {
        "Sepal.Length": 4.7,
        "Sepal.Width": 3.2,
        "Petal.Length": 1.3,
        "Petal.Width": 0.2,
        "Species": "setosa"
    }
]
```

This is just like a CSV, but a little more careful about how certain types of data are encoded for transmitting over the internet. There are ways to use JSON in your code just as easily as a CSV without you needing to change anything else.

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

### Basic use
Since we're using R, Python, or SAS, we don't need to remember the syntax for `curl`. Instead we can use packages that handle request construction for us.

First you set up a request and send it, then you parse the response. There are three simple examples in this repository for you to copy snippets from:

 - [R_tutorial.R](R_tutorial.R)
 - [py_tutorial.py](py_tutorial.py)
 - [SAS_tutorial.sas](SAS_tutorial.sas)

### Advanced use

Let's look at an example where you might need to make multiple API calls:

```r
library(httr)
library(jsonlite)

# Make the call
my_sites_req <- GET(
  url = "https://api.precisionsustainableag.org/onfarm/raw",
  query = list(
    table = "site_information",
    code = "ETO,NDK",
    output = "json"
  ),
  add_headers(
    "x-api-key" = "myAPIkey"
  )
)

# Read the response
my_sites_response <- fromJSON(content(my_sites_req, as = "text"))
```

Notice that instead of a long URL with an embedded query string, I could pass in parameters as a familiar list (familiar to an R user, anyway). I also added the API key header separately. This means that if I wanted to loop over mulitple sites, or multiple endpoints, I could just generate that list using a loop, or `lapply`, or `purrr::map`, and pass the list in to `httr::GET`.

Now I have a dataframe `my_sites_response` that has location data in it. So if I wanted to look up the soils in one of those sites, I could use the SSURGO endpoint:

```r
my_soils_req <- GET(
  url = "https://api.precisionsustainableag.org/ssurgo",
  query = list(
    lat = my_sites_response$latitude[1],
    lon = my_sites_response$longitude[1]
    # [1] to get the first item, site 'ETO'
  )
)

# Read the response
my_soils <- fromJSON(content(my_soils_req, as = "text"))
```

And that would return the soil information at the location specified in the first row of the `my_sites_response` dataframe.