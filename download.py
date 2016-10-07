import flickrapi
import urllib.request as url 
import json
import re 
import os 

api_key = None
api_secret = None

with open("flickr_keys.txt") as keys:
    for line in keys:
        if line.startswith("API_KEY"):
            key = line.lstrip("API_KEY")
            api_key = key.strip()
        if line.startswith("API_SECRET"):
            secret = line.lstrip("API_SECRET")
            api_secret = secret.strip()

if api_key is None or api_secret is None:
    print("Missing key.")
    quit()

#authenticate 
flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='read')


#
# downloads large variants and saves to file 
#
#set = flickr.walk_set('72157661873664226')
set = flickr.walk(tag_mode='all',user_id='30912233@N04') 

for photo in set:
    id = photo.get('id') 
    data = flickr.photos.getSizes(photo_id=id, format="json").decode("utf-8")  
    js = json.loads(data)
    array = js["sizes"]["size"] 
    link = array[len(array) - 1]["source"] 
    print(link)
    data = flickr.photos.getInfo(photo_id=id, format="json").decode("utf-8")
    js = json.loads(data)
    date=js["photo"]["dates"]["posted"]
    filename=date + "_" + id + ".jpg"

    if not os.path.isfile(filename):
        url.urlretrieve(link, filename)
        print("ok")


