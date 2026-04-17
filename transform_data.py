import pandas as pd 
import geopandas as gdp 

df = pd.read_csv('nairobi_healthcare_facilities.csv')

print("n\2. Transforming into a spatial Geodataframe")

gdf = gdp.GeoDataFrame(
    df,
    geometry=gdp.points_from_xy(df.longitude, df.latitude),
    crs="EPSG:4326"
)

print(gdf[['name', 'amenity_type', 'osm-type', 'geometry']].head())

gdf.to_file('nairobi_healthcare_facilities.geojson', driver='GeoJSON' )