import requests  # import the requests library
import pprint    # print JSON cleanly


# Example query URLs

# url = ('https://api.precisionsustainableag.org/weather'
#        '/averages?lat=39.03&lon=-76.87'  # climate normals, location
#        '&start=2021-05-01'               # start date in YMD
#        '&end=2021-06-01'                 # end date in YMD
#        '&output=json'                    # format
#        )

url = ('https://api.precisionsustainableag.org/onfarm'
       '/soil_moisture?type=tdr'         # endpoint for soil moisture sensors
       '&code=KTA'                       # farm code
       '&output=json'                    # format
       )       

headers = {'x-api-key': 'YOUR_API_KEY'}

# Make a GET request to the URL
response = requests.get(url, headers = headers)  

# Print status code (and associated text)
print(f"Request returned {response.status_code} : '{response.reason}'")

# Print data returned (parsing as JSON)
payload = response.json()  # Parse `response.text` into JSON

pp = pprint.PrettyPrinter(indent=1)
pp.pprint(payload)