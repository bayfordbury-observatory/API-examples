#
# A simple script to download images within a chosen radius of a target
#

from urllib.request import urlopen
import json

#API details
observer_id = 1
api_key = "xyz"

#Target name
target = "M82"

#Search radius (degs)
radius=0.2

#SIMBAD URL to get decimal coordinates from target name
simbadURL = "http://simbad.u-strasbg.fr/simbad/sim-script?script=output%20console=off%20script=off%0Aformat%20object%20%22%25COO%28d;%20A%20D;FK5;J2000;%29%22%0A"+target

#run the SIMBAD query
response = urlopen(simbadURL)

#read the return data
return_data = response.read().decode("utf-8").strip()

#extract ra and dec, no need to convert to decimal
coords = return_data.split()

#build image search url
url = "http://observatory.herts.ac.uk/api/imagesearch.php?id="+str(observer_id)+"&key="+api_key+"&ra="+coords[0]+"&dec="+coords[1]+"&dist="+str(radius)+"&solved=true"

#run the image search
response = urlopen(url)

#read the return data
return_data = response.read()

#load the json data
data = json.loads(return_data)

#get the number of images
image_count = data['imageCount']

print ("Found "+ str(image_count) +" images within "+str(radius)+" degrees of "+target)

#if no images, don't do anything
if image_count>0:

	#the list of images
	image_list = data['images']

	#loop through images
	for n in range(image_count):
		
		#get the id number from the list
		dbid = image_list[n]['id']
	
		print ("Downloading " + str(dbid))
		
		#construct the URL to download the image
		download_url = "http://observatory.herts.ac.uk/api/getfit.php?id="+str(observer_id)+"&key="+api_key+"&dbid="+str(dbid)

		#output file name
		file_name = str(dbid)+".fit"
		
		#download the fits file
		with urlopen(download_url) as response, open(file_name, 'wb') as out_file:
			data = response.read()
			out_file.write(data)