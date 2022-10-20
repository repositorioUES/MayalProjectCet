import folium
import phonenumbers
from mynumber import number
from phonenumbers import geocoder

llave = '30e3f905fb6b4f5dbf4bf759a091fe8c'

sanNumber = phonenumbers.parse(number)
tulocacion = geocoder.description_for_number(sanNumber,"en")
print(tulocacion)


##get service provider

from phonenumbers import carrier

provedorServicio =phonenumbers.parse(number)
print(carrier.name_for_number(provedorServicio, "en"))

from opencage.geocoder import OpenCageGeocode

geocoder = OpenCageGeocode(llave)

query = str(tulocacion)
resultado = geocoder.geocode(query)
print(resultado)

latitud = resultado[0]['geometry']['lat']

longitud = resultado[0]['geometry']['lng']

print(latitud, longitud)

myMap = folium.Map(location=[latitud, longitud], zoom_start = 9)

folium.Marker([latitud, longitud],popup=tulocacion).add_to((myMap))

## save map in html file

myMap.save("myLocation.html")
