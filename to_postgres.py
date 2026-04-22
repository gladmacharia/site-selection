import os
import geopandas as gpd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DB_URL")

if not db_url:
    print("could not find the database connection")
    exit()

engine = create_engine(db_url)

geojson_files = {
    "nairobi_healthcare.geojson": "healthcare_facilities",
    "nairobi_nodes.geojson": "nairobi_nodes",
    "nairobi_edges.geojson": "nairobi_edges"

}

# Pushing data to postgis

for file_name, table_name in geojson_files.items():
    try:
        gdf = gpd.read_file(file_name)
        gdf.to_postgis(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False
        )
        print(f"Successfully added {table_name} to the database")
    
    except Exception as e:
        print(f"Database error for {table_name}: {e}")

# for the boundary
file_name = "./Nairobi_boundary/nairobi_boundary.shp"
gdf_boundary = gpd.read_file(file_name)

#reprojecting

gdf_boundary = gdf_boundary.to_crs(epsg=4326)

try:
    gdf_boundary.to_postgis(
        name="nairobi_boundary",
        con=engine,
        if_exists="replace",
        index=False
    )

except Exception as e:
    print(f"Database error: {e}")

print("All data has been successfully added to the database.")