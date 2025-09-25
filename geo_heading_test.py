from geopy.distance import geodesic
from math import atan2, degrees

def calculate_heading(lat1, lon1, lat2, lon2):
    delta_lon = lon2 - lon1
    x = atan2(delta_lon, lat2 - lat1)
    bearing = (degrees(x) + 360) % 360
    return bearing  # 0° is north, 90° is east

# Sample data
heading = calculate_heading(19.123, 73.456, 19.124, 73.457)
print("Direction (degrees from North):", heading)
