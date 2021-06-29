filename resp temp;
 
proc http 
  url="https://api.precisionsustainableag.org/weather/averages"
  query = (
    "lat" = "39.03"
    "lon" = "-76.87"
    "start" = "2021-05-31",
    "end" = "2020-06-01",
    "output" = "json"
  )
  out=resp;
run;

libname wx JSON fileref=resp;
proc datasets lib=wx; quit;

proc print data=wx.root;
run;
 
 
quit;