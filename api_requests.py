import requests
import sys

waypoints = sys.argv[1] # where waypoints has some variables long and lat for the longitude and latitude of the node respectively 
coordinates = ""
# string formatting for input into mapbox api
for node in waypoints:
    coordinates = coordinates + waypoints["long"] + "," + waypoints["lat"] + ";"
coordinates = coordinates[:-1] # remove last ; from coordinates string

access_token = "" # api token
url = f"https://api.mapbox.com/optimized-trips/v1/mapbox/driving/{coordinates}?geometries=geojson&access_token={access_token}"

response = requests.get(url)
data = response.json()

# Get the optimized route geometry and order
route = data["trips"][0]["geometry"]
waypoint_order = [wp["waypoint_index"] for wp in data["waypoints"]] # retrieves node id for each node/waypoint

print("Optimized order of stops:", waypoint_order)
