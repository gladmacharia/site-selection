import pandas as pd 
import geopandas as gpd

df = pd.read_csv('nairobi_healthcare_facilities.csv')

# Transforming into a spatial Geodataframe

gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df.longitude, df.latitude),
    crs="EPSG:4326"
)
countyofInterest = "./Nairobi_boundary/nairobi_boundary.shp"
gdf_boundary = gpd.read_file(countyofInterest)

# Projection
gdf_boundary = gdf_boundary.to_crs("EPSG:4326")

#clipping the healthcare facilities to the boundary of Nairobi

gdf_clipped = gpd.clip(gdf,gdf_boundary)


gdf_clipped.to_file('nairobi_healthcare.geojson', driver='GeoJSON' )

print("Successfully transformed and saved the healthcare facilities data as GeoJSON.")