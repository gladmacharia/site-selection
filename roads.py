import osmnx as ox
import geopandas as gpd

G = ox.graph_from_place("Nairobi, Kenya", network_type="drive")

#conversion to geodataframe

nodes, edges = ox.graph_to_gdfs(G)

nodes = nodes.reset_index()
edges = edges.reset_index()


# cleaning the edges data 

for col in edges.columns:
    if col != 'geometry':
        if edges[col].apply(type).eq(list).any():
            edges[col] = edges[col].apply(lambda x: ','.join(map(str, x)) if isinstance(x, list) else x)

# cleaning the nodes data
for col in nodes.columns:
    if col != 'geometry':
        if nodes[col].apply(type).eq(list).any():
            nodes[col] = nodes[col].apply(lambda x: ','.join(map(str, x)) if isinstance(x, list) else x)

nodes_clean = nodes[['osmid', 'x', 'y', 'geometry']]

edges_cols = ['u', 'v', 'name', 'highway', 'length', 'maxspeed', 'geometry']

edges_clean = edges[[col for col in edges_cols if col in edges.columns]]

nodes_clean.to_file('nairobi_nodes.geojson', driver='GeoJSON')
edges_clean.to_file('nairobi_edges.geojson', driver='GeoJSON')

print("Succesfully extracted and saved the road network data for Nairobi as GeoJSON files.")