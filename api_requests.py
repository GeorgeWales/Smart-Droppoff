import requests

def get_order(waypoints):
    coordinates = ""
    for node in waypoints:
        coordinates = coordinates + node["long"] + "," + node["lat"] + ";"
    coordinates = coordinates[:-1]

    access_token = "" # api key
    url = f"https://api.mapbox.com/optimized-trips/v1/mapbox/driving/{coordinates}?geometries=geojson&access_token={access_token}"

    response = requests.get(url)
    data = response.json()

    # Get the optimized route geometry and order
    route = data["trips"][0]["geometry"]
    waypoint_order = [wp["waypoint_index"] for wp in data["waypoints"]] # retrieves node id for each node/waypoint

    print("Optimized order of stops:", waypoint_order)

    return route
