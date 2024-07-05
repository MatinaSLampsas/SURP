import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load the data
data = pd.read_csv('data/combined_final.csv')

# Define the function to calculate distance based on coordinates
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    # Convert coordinates from degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

# Real coastal access points along the SLO coastline
coastal_access_points = [
    (35.142753, -120.641283),  # Pismo Beach
    (35.179982, -120.731913),  # Avila Beach
    (35.365837, -120.853276)   # Morro Bay
]

# Coordinates for Downtown SLO and Cal Poly
downtown_slo_coords = (35.282752, -120.659616)
calpoly_coords = (35.300399, -120.662362)

# Function to find the minimum distance to any coastal access point
def min_distance_to_coast(lat, lon, access_points):
    distances = [haversine(lat, lon, lat2, lon2) for lat2, lon2 in access_points]
    return min(distances)

# Calculate the minimum distance to the coast, downtown, and Cal Poly
data['dist_ocean'] = data.apply(lambda row: min_distance_to_coast(row['LATITUDE'], row['LONGITUDE'], coastal_access_points), axis=1)
data['dist_downtown'] = data.apply(lambda row: haversine(row['LATITUDE'], row['LONGITUDE'], downtown_slo_coords[0], downtown_slo_coords[1]), axis=1)
data['dist_calpoly'] = data.apply(lambda row: haversine(row['LATITUDE'], row['LONGITUDE'], calpoly_coords[0], calpoly_coords[1]), axis=1)

# Show updated DataFrame with new distance variables
data[['ADDRESS', 'dist_ocean', 'dist_downtown', 'dist_calpoly']].head()
print(data[['ADDRESS', 'dist_ocean', 'dist_downtown', 'dist_calpoly']].head())


#Read in the coastline data
coastline_data = gpd.read_file('C:/Users/matin/OneDrive - Cal Poly/noaa_composite/composite_shoreline_final.shp')
coastline = gpd.GeoSeries(coastline_data.geometry.union_all())


home_locations = gpd.GeoDataFrame(geometry=gpd.points_from_xy(data['LONGITUDE'], data['LATITUDE']), crs='EPSG:4326')

# Assuming home locations are in WGS84 (lat/lon))
# preview the coastal data
print(coastline_data.head())
