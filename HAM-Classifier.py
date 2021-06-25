###searches Harvard Art Museum digital collections by (common era), four digit year-of-production, and applies object classification to images of objects from that year
###Prints list of objects detected and outputs wordcloud based on those classifications
###Requires unique Harvard Art Museum API key, accessible here: https://harvardartmuseums.org/collections/api
###Matt Cook - 2020

import urllib3
import cvlib as cv
from cvlib.object_detection import draw_bbox
import sys
import cv2
import requests
import json
import urllib.request
import re
from wordcloud import WordCloud

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
        'size':250,
        'page':5,
        'apikey': 'xxx', #add HAM api key here
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
    if 'primaryimageurl' in records[idNumber]:
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

with open("xxx.txt", "w") as output:
    output.write(list2)
    
wordcloud = WordCloud().generate(list2)

# Display the generated image the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
print("\n")


print("program terminated")
