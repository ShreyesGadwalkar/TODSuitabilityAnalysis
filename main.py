import pandas as pd
import geopandas as gpd
import ssl
import certifi
import urllib.request
import matplotlib.pyplot as plt


def download_csv(url):
    context = ssl.create_default_context(cafile=certifi.where())
    response = urllib.request.urlopen(url, context=context)
    return pd.read_csv(response)


def csv_to_gdf(url, lon_col, lat_col):
    df = download_csv(url)
    if lon_col in df.columns and lat_col in df.columns:
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]))
    else:
        raise KeyError(f"Columns '{lon_col}' and '{lat_col}' not found in the dataset.")
    return gdf


def process_schools_data(url):
    df = download_csv(url)
    if 'location_1' in df.columns:
        df[['latitude', 'longitude']] = df['location_1'].str.extract(r'\(([^,]+), ([^)]+)\)')
        df['latitude'] = df['latitude'].astype(float)
        df['longitude'] = df['longitude'].astype(float)
    else:
        raise KeyError("'location_1' column not found in the dataset.")
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['longitude'], df['latitude']))
    return gdf


parcels_gdf = csv_to_gdf('https://data.sfgov.org/resource/acdm-wktn.csv', lon_col='centroid_longitude', lat_col='centroid_latitude')
parks_gdf = csv_to_gdf('https://data.sfgov.org/resource/gtr9-ntp6.csv', lon_col='longitude', lat_col='latitude')
schools_gdf = process_schools_data('https://data.sfgov.org/resource/tpp3-epx2.csv')
bus_stops_gdf = csv_to_gdf('https://data.sfgov.org/resource/i28k-bkz6.csv', lon_col='longitude', lat_col='latitude')


parcels_gdf.crs = "EPSG:4326"
parks_gdf.crs = "EPSG:4326"
schools_gdf.crs = "EPSG:4326"
bus_stops_gdf.crs = "EPSG:4326"


def nearest_distance(row, gdf):
    point = row.geometry
    distances = gdf.geometry.distance(point)
    return distances.min()


parcels_gdf['dist_to_park'] = parcels_gdf.apply(nearest_distance, gdf=parks_gdf, axis=1)
parcels_gdf['dist_to_school'] = parcels_gdf.apply(nearest_distance, gdf=schools_gdf, axis=1)
parcels_gdf['dist_to_bus_stop'] = parcels_gdf.apply(nearest_distance, gdf=bus_stops_gdf, axis=1)


def score_distance(distance, max_distance):
    if distance > max_distance:
        return 0
    return (max_distance - distance) / max_distance


max_dist_to_park = parcels_gdf['dist_to_park'].max()
max_dist_to_school = parcels_gdf['dist_to_school'].max()
max_dist_to_bus_stop = parcels_gdf['dist_to_bus_stop'].max()


parcels_gdf['score_park'] = parcels_gdf['dist_to_park'].apply(lambda x: score_distance(x, max_dist_to_park))
parcels_gdf['score_school'] = parcels_gdf['dist_to_school'].apply(lambda x: score_distance(x, max_dist_to_school))
parcels_gdf['score_bus_stop'] = parcels_gdf['dist_to_bus_stop'].apply(lambda x: score_distance(x, max_dist_to_bus_stop))


parcels_gdf['total_score'] = parcels_gdf['score_park'] + parcels_gdf['score_school'] + parcels_gdf['score_bus_stop']



# Visualize results
fig, ax = plt.subplots(1, 1, figsize=(12, 8))  # Adjust the aspect ratio of the plot
parcels_gdf.plot(column='total_score', ax=ax, legend=True,
                 legend_kwds={'label': "TOD Suitability Score", 'orientation': "horizontal"})
parks_gdf.plot(ax=ax, color='green', markersize=10, label='Parks')
schools_gdf.plot(ax=ax, color='red', markersize=10, label='Schools')
# Reduce marker size for bus stops to distinguish individual stops
bus_stops_gdf.plot(ax=ax, color='orange', markersize=5, label='Bus Stops')
plt.legend()

# Set y-axis limits
plt.ylim(37.65, 37.85)
plt.xlim(-122.55, -122.35)

plt.show()


parcels_gdf.to_file('tod_suitability_parcels.shp')
