"""
This code serves to produce a static map
with two markers in a hybrid satellite style
static google map.

The API Key is taken from my personal Google account
and should be changed further on.
"""
def createStaticMap(size='600x400', scale='2', maptype='hybrid',img_format='jpg',marker1='lagerstrasse+1,zuerich,ch', marker2='buelachstrasse+9g,zuerich,ch'):
    import urllib.request

    exportedImgName = 'img1.jpg'

    #API Key and URL are static and should be chagned if needed
    key = '&key=AIzaSyBtMIthbknn345WE5rJxBqE4McsTwkwmVk'
    url = 'https://maps.googleapis.com/maps/api/staticmap?'

    size = ''.join(('&size=',size))
    scale = ''.join(('&scale=',scale))
    #zoom = '&zoom=12'
    maptype = ''.join(('&maptype=', maptype))
    img_format = ''.join(('&format=', img_format))
    marker1 = ''.join(('&markers=', marker1))
    marker2 = ''.join(('&markers=', marker2))

    param_url = ''.join((url, size, marker1, marker2, scale, maptype, img_format, key))
    urllib.request.urlretrieve(param_url, exportedImgName)

    return print("Static image created from {}\n Exported as {}.".format(param_url, exportedImgName))

if __name__=="__main__":
    createStaticMap()