import requests

waypoints = [
    # some dictionaries of waypoints containing lat (latitude) and long (longitude) values
]

def get_data(waypoints):
    coordinates = ""
    # format input for Mapbox API
    # coordinates = "long,lat;long,lat;long,lat"
    for node in waypoints:
        coordinates = coordinates + str(node["long"]) + "," + str(node["lat"]) + ";"
    coordinates = coordinates[:-1]

    access_token = # API key
    url = f"https://api.mapbox.com/optimized-trips/v1/mapbox/driving/{coordinates}?geometries=geojson&access_token={access_token}"

    response = requests.get(url)
    data = response.json()

    return data

def get_order(data=get_data(waypoints)):
    waypoint_order = [wp["waypoint_index"] for wp in data["waypoints"]] # retrieves node id for each node/waypoint
    print(waypoint_order)
    return waypoint_order

def get_route(data=get_data(waypoints)):
    route = data["trips"][0]["geometry"]["coordinates"] # retrieves the coordinates of the route
    print(route)
    return route

get_order()
get_route()
