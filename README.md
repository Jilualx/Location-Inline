Assumptions made:
=================
	- Journey or path course is from a lower coordinate to a higher coordinate
	- lowest coordinate is starting point and highest coordinate is final destination
	- starting point and final destination are in a line (other coordinates are checked and corrected to this line)


DB details:
===========
	Database Platform: PostgreSQL
	Database Name : LocationDB
	No. Of Tables : 2
	
*Table 1:
		Table Name: TerrainMaster
		No. Of column: 2
		Column Names: Terrain_Id, Terrain_Name

*Table 2:
		Table Name: LocationCoordinates
		No. Of column: 5
		Column Names: Loc_Id, Latitude, Longitude, Distance, Terrain_Id


Algorithm Steps:
================
	#1: Open latitude_longitude_details.csv
	#2: Sort the data
	#3: Store Starting and Destination Coordinates
	#4: calculate slope/generate line expresion
	#5: loop through the 2nd to second last coordinates
		#5.1: check if its in the line
		#5.2: correct the coordinate to form line
		#5.3: store the coordinates to DB
		#5.4: calculate distance in KM from previous coordinates
		#5.5: find the terrains
		#5.6: Store the Coordinates details, distance and terrain details to DB
		#5.7: go to next Coordinates and repeat from Step #5.1
	#6: Query to list all the Coordinates details with terrain contains "road" and doesnot contain "civil station"
	
