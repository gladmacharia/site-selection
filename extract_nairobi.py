import requests
import time
import pandas as pd 



url = "http://overpass-api.de/api/interpreter"

amenities_to_find = ["hospital","clinic"]

all_healthcare_facilities = []

for amenity in amenities_to_find:
    print(f"Extracting '{amenity}' data")


    query = f"""
    [out:json][timeout:90][bbox: -1.45,36.5, -1.15,37.10];
    nwr["amenity"="{amenity}"];
    out center;
    """
    try:
        response = requests.post(url, data={'data': query}, timeout=100)

        response.raise_for_status()

        data = response.json()
        elements = data.get('elements', [])

        for facility in elements:

            name = facility.get('tags',{}).get('name','Unnamed Facility')
            type = facility['type']

            if type == 'node':
                lat = facility['lat']
                lon = facility['lon']
            else:
                lat = facility.get('center',{}).get('lat')
                lon = facility.get('center',{}).get('lon')

            if lat and lon:
                clean_facility = {
                    'name': name,
                    'amenity_type': amenity,
                    'osm-type': type,
                    'latitude': lat,
                    'longitude': lon    
                }
                all_healthcare_facilities.append(clean_facility)

       
    except requests.exceptions.ConnectTimeout:
        print("Connection timed out. Please try again later.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")

    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")

    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

    time.sleep(5)  # Wait before retrying

print(f"Total healthcare facilities in Nairobi: {len(all_healthcare_facilities)}")

if len(all_healthcare_facilities) > 0:
    df = pd.DataFrame(all_healthcare_facilities)
    df.to_csv('nairobi_healthcare_facilities.csv', index=False)

else:
    print("No healthcare facilities found in Nairobi.")