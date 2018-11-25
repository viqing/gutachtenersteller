"""
This code serves to produce a static map
with two markers in a hybrid satellite style
static google map.

Sizes are to be considered as follows:
Hauptobjekt 
makro: 1100, 750
mikro: 1100, 750

Vergleichsobjekte
makro: 1000, 800
mikro: 1200, 750

The API Key is taken from my personal Google account
and should be changed further on.
"""

def createStaticHOMap(zoom, exportedImgName, size='550x375', scale='2', maptype='hybrid',img_format='jpg', address='lagerstrasse+1,zuerich,ch', exportPath='img'):
    import urllib.request

    #API Key and URL are static and should be chagned if needed
    with open('api-key.txt', 'r') as api_file:
        key = api_file.readline()

    key = ''.join(('&key=', key))
    url = 'https://maps.googleapis.com/maps/api/staticmap?'

    size = ''.join(('&size=',size))
    scale = ''.join(('&scale=',scale))
    maptype = ''.join(('&maptype=', maptype))
    img_format = ''.join(('&format=', img_format))
    marker = ''.join(('&markers=', address))
    zoom = ''.join(('&zoom=',zoom))
    import os 
    fullExportPath = ''.join((exportPath,'/',exportedImgName))

    param_url = ''.join((url, size, marker, scale, maptype, img_format, zoom, key))
    urllib.request.urlretrieve(param_url, fullExportPath)
    print("Static mikro image created from {}\n Exported as {}.".format(param_url, fullExportPath))

    return fullExportPath

def createStaticVOMakroMap(size='500x400', scale='2', maptype='hybrid',img_format='jpg', address1='Place+de+la+Gare+5A,+1003+Lausanne', address2='buelachstrasse+9g,zuerich,ch', exportPath='test', exportedImgName='makro.jpg'):
    import urllib.request

    #API Key and URL are static and should be chagned if needed
    with open('api-key.txt', 'r') as api_file:
        key = api_file.readline()

    key = ''.join(('&key=', key))
    url = 'https://maps.googleapis.com/maps/api/staticmap?'

    size = ''.join(('&size=',size))
    scale = ''.join(('&scale=',scale))
    #zoom = '&zoom=12'
    maptype = ''.join(('&maptype=', maptype))
    img_format = ''.join(('&format=', img_format))
    path = ''.join(('&path=color:0xd34d3dff|weight:3|', address1, '|', address2))
    marker1 = ''.join(('&markers=', address1))
    marker2 = ''.join(('&markers=', address2))

    import os
    print(fullExportPath)

    param_url = ''.join((url, size, marker1, marker2, scale, maptype, img_format, path, key))
    urllib.request.urlretrieve(param_url, fullExportPath)
    #print the distance on the image
    from PIL import Image
    from PIL import ImageFont
    from PIL import ImageDraw
    import os

    img = Image.open(fullExportPath)
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    if os.name == 'posix':
        font = ImageFont.truetype("Arial.ttf", 48)
    elif os.name == 'nt':
        font = ImageFont.truetype("arial.ttf", 48)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((500, 400), ''.join((str(distance),'m')), (255,250,250), font=font)
    img.save(fullExportPath)

    return fullExportPath

def createStaticVOMikroMap(size='600x375', scale='2', maptype='hybrid',img_format='jpg', address='lagerstrasse+1,zuerich,ch',exportPath='test', exportedImgName='mikro.jpg'):
    import urllib.request

    #API Key and URL are static and should be chagned if needed
    with open('api-key.txt', 'r') as api_file:
        key = api_file.readline()

    key = ''.join(('&key=', key))
    url = 'https://maps.googleapis.com/maps/api/staticmap?'

    size = ''.join(('&size=',size))
    scale = ''.join(('&scale=',scale))
    zoom = '&zoom=18'
    maptype = ''.join(('&maptype=', maptype))
    img_format = ''.join(('&format=', img_format))
    marker = ''.join(('&markers=', address))

    fullExportPath = ''.join((exportPath,'/',exportedImgName))

    param_url = ''.join((url, size, marker, scale, maptype, img_format, zoom, key))
    urllib.request.urlretrieve(param_url, fullExportPath)
    print("Static mikro image created from {}\n Exported as {}.".format(param_url, fullExportPath))

    return fullExportPath

def findLatLng(address):

    #API Key and URL are static and should be chagned if needed
    with open('api-key.txt', 'r') as api_file:
        key = api_file.readline()

    key = ''.join(('&key=', key))
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    address = ''.join(('&address=', address))
    param_url = ''.join((url, address, key))

    import requests
    response = requests.get(param_url)
    resp_json_payload = response.json()

    return resp_json_payload['results'][0]['geometry']['location']['lat'], resp_json_payload['results'][0]['geometry']['location']['lng']

def findClosestPlace(location=[47.401492, 8.547384], type='grocery_or_supermarket', rank_by='distance'):
    import googlemaps

    # documentatio for supported types:
    # https://developers.google.com/places/web-service/supported_types

    with open('api-key.txt', 'r') as api_file:
        key = api_file.readline()
    gmaps = googlemaps.Client(key=key)
    results = gmaps.places_nearby(location=location, type=type, rank_by='distance')

    nearestPlace = results['results'][0]
    nearestPlaceLatLng = [nearestPlace['geometry']['location']['lat'],nearestPlace['geometry']['location']['lng']]
    distanceToNearestPlace = calculateDistance(location, nearestPlaceLatLng)
    nearestPlace['dist'] = distanceToNearestPlace

    return nearestPlace
    

def calculateDistance(point1, point2):

    import math    
    def rad(x):
        return x * math.pi / 180

    R = 6378137
    dLat = rad(point2[0] - point1[0])
    dLng = rad(point2[1] - point1[1])
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(rad(point1[0])) * math.cos(rad(point2[0])) * math.sin(dLng / 2) * math.sin(dLng / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return round(d)

if __name__=="__main__":
    createStaticHOMap(zoom='14', exportedImgName='ho-makro.jpg')
    createStaticHOMap(zoom='18', exportedImgName='ho-mikro.jpg')
    createStaticVOMakroMap()
    createStaticVOMikroMap()