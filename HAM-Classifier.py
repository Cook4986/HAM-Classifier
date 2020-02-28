import urllib3
import cvlib as cv
from cvlib.object_detection import draw_bbox
import sys
import cv2
import requests
import json
import urllib.request
import re

#get User Input 
inputString = input("Input four digit (common era) year: ")
inputString = str(inputString)

#declarations
idNumber = 0
objects = []

# Find and return image URL based on input string
http = urllib3.PoolManager()
r = http.request('GET', 'https://api.harvardartmuseums.org/object',
    fields = {
        'size':100,
        'page':10,
        'apikey': 'd9da03d0-fbef-11e9-896e-3bd7722ada6a',
        'yearmade': inputString,
        'fields': 'primaryimageurl',
        
     })

print("completed Harvard Art Museums API request")
print("\n")

#parse json response
resp_dict = json.loads(r.data)
records = resp_dict['records']

#classify image contents 
def Classifier():
# read input image 
    image = cv2.imread(imageCache)
     
# apply object detection
    bbox, label, conf = cv.detect_common_objects(image)

# draw bounding box over detected objects
    out = draw_bbox(image, bbox, label, conf)
    if label != []:
        objects.append(label)
    
# save output
    cv2.imwrite("obtec" + "_image " + str(idNumber) + ".jpg", out)
    
# release resources
    cv2.destroyAllWindows()

#iterate over all images on page 
for value in records:
    print("image url #", idNumber + 1,"=", records[idNumber]['primaryimageurl'])
    imageCache = "cache.jpg"
    urllib.request.urlretrieve(records[idNumber]['primaryimageurl'], imageCache)
    Classifier()
    idNumber = idNumber + 1  

#cleanup, print and save classifications
list2 = [x for x in objects if x != []]
list2 = str(list2)
list2 = list2.strip()
list2 = list2.replace("'", '')
list2 = list2.replace("]", '')
list2 = list2.replace("[", '')
print("the following objects were detected in images from the year " + inputString + ":")
print("\n")
print(list2)

with open("outputFile.txt", "w") as output:
    output.write(list2)

print("program terminated")