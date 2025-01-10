import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

# List of locations with names and addresses
locations = [
    {
        "name": "Blaskovics Autószerviz",
        "address": "9027 Győr, Bajza u. 3",
        "tel": "+36 20 261 1525"
    },
    {
        "name": "FitAuto gyorsszerviz",
        "address": "null",
        "tel": "null"
    },
    {
        "name": "Iniciál Autóház Győr",
        "address": "9028 Győr, Külső Veszprémi u. 6.",
        "tel": "+36 96 998 080"
    },
    {
        "name": "Műszaki Vizsgáztató",
        "address": "9027 Győr, Puskás Tivadar utca 8.",
        "tel": "+36 30 527 1135"
    },
    {
        "name": "Garázspont Autószerviz Kft.",
        "address": "9027 Győr, Puskás Tivadar utca 8.",
        "tel": "+36 30 527 1135"
    },
    {
        "name": "Leier Autó",
        "address": "9024 Győr, Szauter út 9",
        "tel": "+36 96 513 213"
    },
    {
        "name": "Beni Autószerviz",
        "address": "9029 Győr, Csalogány utca 51-53.",
        "tel": "+36 70 775 5147, +36 96 332 079"
    },
    {
        "name": "Turbo-Tec Szerviz",
        "address": "9025 Győr, Kossuth Lajos utca 166",
        "tel": "+36 96 627 422"
    },
    {
        "name": "Németh Autószerviz Tét",
        "address": "9100 Tét, Fő utca 135.",
        "tel": "+36 20 510 2535"
    },
    {
        "name": "Magyar Autóklub Szerviz- és vizsgapont",
        "address": "9027 Győr, Tompa utca 2.",
        "tel": "+36 96 317 900"
    }
]

# Initialize the geocoder with increased timeout
geolocator = Nominatim(user_agent="my_geocoder", timeout=10)


def get_coordinates(address, max_retries=3):
    for i in range(max_retries):
        try:
            location = geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
            time.sleep(2)  # Increased delay between requests
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            print(f"Attempt {i + 1} failed for {address}: {str(e)}")
            if i == max_retries - 1:
                print(f"Failed to geocode address after {max_retries} attempts: {address}")
                return None
            time.sleep(2)  # Wait longer between retries
    return None


# Alternative coordinates for Győr city center
GYOR_CENTER = [47.6875, 17.6504]

try:
    # Get coordinates for all locations
    for loc in locations:
        print(f"Geocoding: {loc['address']}")
        coords = get_coordinates(loc["address"])
        if coords:
            loc["lat"], loc["lon"] = coords
            print(f"Success: {loc['name']} -> {coords}")
        else:
            print(f"Failed to geocode: {loc['name']}")

    # Create a map centered around Győr
    m = folium.Map(location=GYOR_CENTER, zoom_start=13)

    # Add markers for each location
    for loc in locations:
        if "lat" in loc and "lon" in loc:
            folium.Marker(
                location=[loc["lat"], loc["lon"]],
                popup=f"{loc['name']}<br>{loc['address']}",
                tooltip=loc['name']
            ).add_to(m)

    # Save the map to an HTML file
    m.save("gyor_muszaki_vizsga_map.html")
    print("Map created and saved as gyor_muszaki_vizsga_map.html")

except Exception as e:
    print(f"An error occurred: {str(e)}")
