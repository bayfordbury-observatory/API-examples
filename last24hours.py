#
# A simple script to download any images taken from your plans over the past 24 hours
#

from urllib.request import urlopen
import json
import time

#API details
observer_id = 0
api_key = "xyz"

#current time in unix format
unix_time = time.time()

#current time in julian date
julian_date = 2440587.5 + (unix_time/86400)

#julian date 24 hours ago
julian_date_yesterday = julian_date - 1

#build image search url
url = "http://observatory.herts.ac.uk/api/imagesearch.php?id="+str(observer_id)+"&key="+api_key+"&minjd="+str(julian_date_yesterday)+"&showProject=true&mine=true"

#run the image search
response = urlopen(url)

#read the return data
return_data = response.read()

#load the json data
data = json.loads(return_data)

#get the number of images
image_count = data['imageCount']

print ("Found "+ str(image_count) +" images")

#if no images, don't do anything
if image_count>0:

	#the list of images
	image_list = data['images']

	#loop through images
	for n in range(image_count):
		
		#get the id number
		dbid = image_list[n]['id']
		
		#get the project name
		projectname = image_list[n]['prj']
	
		print ("Downloading " + str(dbid))
		
		#construct the download url
		download_url = "http://observatory.herts.ac.uk/api/getfit.php?id="+str(observer_id)+"&key="+api_key+"&dbid="+str(dbid)

		#output file name
		file_name = str(dbid)+".fit"
		
		#download the fits file
		with urlopen(download_url) as response, open(file_name, 'wb') as out_file:
			data = response.read()
			out_file.write(data)
			
			
			
