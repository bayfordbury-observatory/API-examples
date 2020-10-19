<?php
	#
	# A simple script to download any images taken from your plans over the past 24 hours
	#

	#API details
	$observer_id = 0;
	$api_key = "xyz";

	#current time in unix format
	$unix_time = time();

	#current time in julian date
	$julian_date = 2440587.5 + ($unix_time/86400);

	#julian date 24 hours ago
	$julian_date_yesterday = $julian_date - 1;

	#build image search url
	$url = "http://observatory.herts.ac.uk/api/imagesearch.php?id=".$observer_id."&key=".$api_key."&minjd=".$julian_date_yesterday."&mine=true";

	#read the return data
	$return_data = file_get_contents($url);

	#load the json data
	$data = json_decode($return_data, JSON_OBJECT_AS_ARRAY);

	#get the number of images
	$image_count = $data['imageCount'];

	print ("Found ".$image_count." images".PHP_EOL);

	#if no images, don't do anything
	if($image_count>0){

		#the list of images
		$image_list = $data['images'];

		$image_count=3;
		
		#loop through images
		for($n=0; $n<$image_count; $n++){
			
			#get the id number
			$dbid = $image_list[$n]['id'];
		
			print ("Downloading " .$dbid.PHP_EOL);
			
			#construct the download url
			$download_url = "http://observatory.herts.ac.uk/api/getfit.php?id=".$observer_id."&key=".$api_key."&dbid=".$dbid;

			#output directory
			$output_dir= getcwd();
			
			#output file name
			$file_name = $output_dir."/".$dbid.".fit";
			
			#download the fits file
			$file = file_get_contents($download_url);
			
			#write to file
			file_put_contents($file_name, $file);
			
		}
	}
			
?>		
