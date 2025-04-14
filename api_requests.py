import requests

access_token = "pk.eyJ1IjoianJvb25leTA1IiwiYSI6ImNtOHE1ODE4YjA5YTMyaXNocGE4OTl6eGwifQ.vS0CZaN1jviMfPYsj4UWNQ"
coordinates = "-122.42,37.78;-122.45,37.91;-122.48,37.73"  # example long,lat;long,lat;... -> can take multiple
                                                           # co-ords from server and input as a concatenated string
                                                           # in order to retrieve optimised order of nodes to be visited
url = f"https://api.mapbox.com/optimized-trips/v1/mapbox/driving/{coordinates}?geometries=geojson&access_token={access_token}"

response = requests.get(url)
data = response.json()

# Get the optimized route geometry and order
route = data["trips"][0]["geometry"]
waypoint_order = [wp["waypoint_index"] for wp in data["waypoints"]] # retrieves node id for each node/waypoint

print("Optimized order of stops:", waypoint_order)