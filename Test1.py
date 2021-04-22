import csv
import numpy
import geopy.distance
import psycopg2


class Location:
    def __init__(self, latitude, longitude):
        self.lat = float(latitude)
        self.long = float(longitude)

    def checkCurrentlocation(self):
        m1 = (self.lat - startLocation.lat) / (self.long - startLocation.long)
        try:
            m2 = (self.lat - destinationLocation.lat) / (self.long - destinationLocation.long)
        except ZeroDivisionError as error:
            m2 = 0
        # check if its in the line
        if m1 == m2:
            return self
        else:
            # correct the coordinate to form line
            cf = (destinationLocation.lat - startLocation.lat) / (destinationLocation.long - startLocation.long)
            correctedlong = float("{:.6f}".format(((self.lat - startLocation.lat) / cf) + startLocation.long))
            return Location(self.lat, correctedlong)

    def calcDistance(self):
        coord1 = (startLocation.lat, startLocation.long)
        coord2 = (self.lat, self.long)
        return float("{:.1f}".format(geopy.distance.geodesic(coord1, coord2).km))

    def insertLocationDetails(self, distance, terrain):
        conn = psycopg2.connect(
            database="LocationDB", user='postgres', password='123456', host='localhost', port='5432')
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute('SELECT \"Terrain_Id\" from public.\"TerrainMaster\" WHERE \"Terrain_Name\" = \'%s\'' % terrain)
        terrainid = cursor.fetchone()

        cursor.execute('''INSERT INTO public.\"LocationCoordinates\"(\"Latitude\", \"Longitude\", \"Distance\", \"Terrain_Id\")
                        VALUES (%f, %f, %f, %d)''' % (self.lat, self.long, distance, terrainid[0]))
        try:
            conn.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def queryroadlist(self):
        conn = psycopg2.connect(
            database="LocationDB", user='postgres', password='123456', host='localhost', port='5432')
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute('''SELECT p.\"Latitude\", p.\"Longitude\", p.\"Distance\", c.\"Terrain_Name\" 
            FROM public.\"LocationCoordinates\" p LEFT JOIN public.\"TerrainMaster\" c ON p.\"Terrain_Id\" = c.\"Terrain_Id\"
            WHERE c.\"Terrain_Name\" LIKE \'%road%\' and c.\"Terrain_Name\" NOT LIKE \'%civil station%\'''')

        rows = cursor.fetchall()
        for r in rows:
            print(str(r[0]) + "  " + str(r[1]) + "  " + str(r[2]) + "  " + str(r[3]))

        try:
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


if __name__ == "__main__":

    # Read Data from latitude_longitude_details.csv
    file_in = csv.reader(open('latitude_longitude_details.csv', 'r'), delimiter=',')
    header = next(file_in)
    coordinates = []
    for row in file_in:
        coordinates.append(row[:])

    # Sort the data is list
    sortedCoordinates = numpy.array(sorted(coordinates, key=lambda x: (x[0], x[1])))

    # Store Starting and Destination Coordinates
    startLocation = Location(sortedCoordinates[0, 0], sortedCoordinates[0, 1])
    destinationLocation = Location(sortedCoordinates[-1, 0], sortedCoordinates[-1, 1])

    for i in range(0, len(sortedCoordinates)):
        distance = 0
        currentLocation = Location(sortedCoordinates[i, 0], sortedCoordinates[i, 1])
        if i == 0 or i == len(sortedCoordinates)+1:  # current location is same as starting position or destination
            correctedLocation = currentLocation
        else:
            correctedLocation = currentLocation.checkCurrentlocation()

        # Calculating distance between previous location to current location
        distance = float(correctedLocation.calcDistance())

        # getting Terrain details
        if distance >= 3:
            terrain = "civil station, road"
        elif distance >= 1.5:
            terrain = "river side"
        elif distance >= 0.5:
            terrain = "road"
        else:
            terrain = "boundary wall,road"

        # Updating data into LocationDB
        correctedLocation.insertlocationdetails(distance, terrain)

    # Query to list all the Coordinates details with terrain contains "road" and does not contain "civil station"
    correctedLocation.queryroadlist()

