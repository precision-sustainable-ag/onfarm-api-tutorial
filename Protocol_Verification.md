Protocol Verification
================

## How to know whether to include a site for a particular metric

When we executed this trial, some sites did not complete all protocols.
We have checked whether a site attempted, completed, or did not attempt
each metric in the study. This is stored in a column returned from
almost all of the API queries called `protocols`. The contents of this
column are:

-   **1** if a site is expected to execute a protocol; does not indicate
    data quality.
-   **0** if a site does not execute a protocol.
-   **-1** if a site does a protocol, but shouldn’t be included in
    analysis because of experimental design or other site factors (like
    unplanned irrigation, improper termination of the bare strip, etc);
    we still track/show the data for other reasons.
-   **-999** if a site started (or even completed) the protocol but the
    data is bad/incomplete and shouldn’t be shown anywhere, e.g. the
    field person reports they conducted the protocol incorrectly.

This is also noted at the API documentation:
<https://api.precisionsustainableag.org/onfarm>

## Checking a site

For almost all endpoints, the protocols column is included in every
query. Here’s an example using dates:

``` r
library(httr)
library(dplyr, warn.conflicts = F)

my_API_key = readLines("my_API_key.txt")

date_rq <- 
  GET(
    "https://api.precisionsustainableag.org/onfarm/dates",
    query = list(code = "UVV"),
    add_headers(
      "x-api-key" = my_API_key
    )
  )

content(date_rq, as = "text") %>% 
  jsonlite::prettify()
```

    ## [
    ##     {
    ##         "code": "UVV",
    ##         "producer_id": "2022Indigo665",
    ##         "year": "2023",
    ##         "affiliation": "Indigo",
    ##         "protocols_enrolled": null,
    ##         "cover_planting": "2022-11-03",
    ##         "cover_termination": "2023-04-20",
    ##         "biomass_harvest": "2023-04-19",
    ##         "cash_planting": "2023-05-04",
    ##         "protocols": {
    ##             "forage_box": 0,
    ##             "sensor_data": -1,
    ##             "bulk_density": 0,
    ##             "corn_disease": null,
    ##             "farm_history": 0,
    ##             "soil_texture": 1,
    ##             "gps_locations": 1,
    ##             "soil_nitrogen": 0,
    ##             "yield_monitor": null,
    ##             "decomp_biomass": 1,
    ##             "cash_crop_yield": 0,
    ##             "in_field_biomass": 1,
    ##             "weed_visual_rating": null,
    ##             "weed_quadrat_photos_beta": null
    ##         }
    ##     }
    ## ]
    ## 

The returned JSON object shows the protocol values for each metric. So
in this example, this site can be used for decomp bags, for example, but
not cash crop yield or soil moisture sensors.

If you coerce this JSON object to a dataframe, you can see the
`protocols` column is actually a nested dataframe that you can interact
with programmatically.

``` r
content(date_rq, as = "text") %>% 
  jsonlite::fromJSON() %>% 
  as_tibble()
```

    ## # A tibble: 1 × 10
    ##   code  producer_id   year  affiliation protocols_enrolled cover_planting
    ##   <chr> <chr>         <chr> <chr>       <lgl>              <chr>         
    ## 1 UVV   2022Indigo665 2023  Indigo      NA                 2022-11-03    
    ## # ℹ 4 more variables: cover_termination <chr>, biomass_harvest <chr>,
    ## #   cash_planting <chr>, protocols <df[,14]>

## Checking a site specifically for soil moisture

Because the soil moisture API endpoint returns so many rows that would
be duplicated in the `protocols` column, we decided that there should be
a two step procedure for these queries. First you need to check one of
the other endpoints to get the `protocols` column, then use that to
clean the list of sites you’re actually querying. In this example we’re
using the `/raw` endpoint to return the contents of the
`site_information` table, but we could use the `/dates`, `/locations`,
`/biomass`, or `/yield` endpoints, for example.

``` r
info_rq <- 
  GET(
    "https://api.precisionsustainableag.org/onfarm/raw",
    query = list(
      table = "site_information",
      code = "NSF"
      ),
    add_headers(
      "x-api-key" = my_API_key
    )
  )

content(info_rq, as = "text") %>% 
  jsonlite::prettify()
```

    ## [
    ##     {
    ##         "code": "NSF",
    ##         "cash_crop": "Corn",
    ##         "cid": 2398,
    ##         "year": "2018",
    ##         "affiliation": "MD",
    ##         "county": "PRINCE GEORGE",
    ##         "longitude": -76.9427490234375,
    ##         "latitude": 39.0159645080566,
    ##         "notes": null,
    ##         "additional_contact": null,
    ##         "producer_id": "2018MD002",
    ##         "address": null,
    ##         "state": "MD",
    ##         "protocols_enrolled": null,
    ##         "protocols": {
    ##             "forage_box": null,
    ##             "sensor_data": 1,
    ##             "bulk_density": 1,
    ##             "corn_disease": null,
    ##             "farm_history": 1,
    ##             "soil_texture": 1,
    ##             "gps_locations": 0,
    ##             "soil_nitrogen": 1,
    ##             "yield_monitor": null,
    ##             "decomp_biomass": 1,
    ##             "cash_crop_yield": 1,
    ##             "in_field_biomass": 1,
    ##             "weed_visual_rating": null,
    ##             "weed_quadrat_photos_beta": 0
    ##         },
    ##         "last_name": "Richards",
    ##         "email": null,
    ##         "phone": null,
    ##         "first_name": null
    ##     }
    ## ]
    ## 

Here we can see that this site has the value `1` for the `sensor_data`
field of the `protocols` column. This means you can proceed to use this
site for soil moisture analysis (after checking whether the data needs
to be cleaned further for your use). Then you can query the
`/soil_moisture` endpoint for that site:

``` r
vwc_rq <- 
  GET(
    "https://api.precisionsustainableag.org/onfarm/soil_moisture",
    query = list(
      type = "tdr",
      code = "NSF"
      ),
    add_headers(
      "x-api-key" = my_API_key
    )
  )

content(vwc_rq, as = "text") %>% 
  jsonlite::fromJSON() %>% 
  as_tibble()
```

    ## # A tibble: 10,674 × 23
    ##    uid    node_serial_no timestamp  ts_up tdr_sensor_id center_depth tdr_address
    ##    <chr>  <chr>          <chr>      <chr> <lgl>                <int> <chr>      
    ##  1 372575 nbctdwjp       2018-05-0… 2018… NA                     -15 A          
    ##  2 596942 nbctdwjp       2018-05-0… 2018… NA                     -45 B          
    ##  3 820371 nbctdwjp       2018-05-0… 2018… NA                     -80 C          
    ##  4 372584 nbctdwjp       2018-05-0… 2018… NA                     -15 A          
    ##  5 596951 nbctdwjp       2018-05-0… 2018… NA                     -45 B          
    ##  6 820380 nbctdwjp       2018-05-0… 2018… NA                     -80 C          
    ##  7 377672 nbctdwjp       2018-05-2… 2018… NA                     -15 A          
    ##  8 602139 nbctdwjp       2018-05-2… 2018… NA                     -45 B          
    ##  9 825398 nbctdwjp       2018-05-2… 2018… NA                     -80 C          
    ## 10 377692 nbctdwjp       2018-05-2… 2018… NA                     -15 A          
    ## # ℹ 10,664 more rows
    ## # ℹ 16 more variables: vwc <dbl>, soil_temp <dbl>, permittivity <dbl>,
    ## #   ec_bulk <dbl>, ec_pore_water <int>, travel_time <lgl>,
    ## #   is_vwc_outlier <lgl>, vwc_outlier_who_decided <chr>,
    ## #   vwc_outlier_comment <chr>, code <chr>, subplot <int>, serial <chr>,
    ## #   trt <chr>, treatment <chr>, time_begin <chr>, time_end <chr>
