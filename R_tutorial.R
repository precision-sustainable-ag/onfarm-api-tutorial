library(httr)

resp <- GET(
  url = "https://api.precisionsustainableag.org/weather/averages",
  query = list(
    lat = 39.03, lon = -76.87,  # location
    start = "2021-06-01",       # start date in YMD
    end = "2021-06-01",         # end date in YMD
    output = "json" 
  )
)

http_status(resp)

jsonlite::prettify(
  content(resp, as = "text")
  )

tibble::as_tibble(
  jsonlite::fromJSON(
    content(resp, as = "text")
  )
)