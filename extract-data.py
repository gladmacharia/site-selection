import requests

url = "http://api.open-notify.org/astros.json"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Check if the request was successful
    data = response.json()
    print(f"Number of people in space: {data['number']}")

except requests.exceptions.ConnectTimeout:
    print("Connection timed out. Please try again later.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")