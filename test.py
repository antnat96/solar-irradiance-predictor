import pandas as pd
from geopy.geocoders import Nominatim

#place = input ("Enter Address :")
place = "408 brook pine trl, apex, nc"
geolocator = Nominatim(user_agent="Test")
location = geolocator.geocode(place)



print("Hello World")