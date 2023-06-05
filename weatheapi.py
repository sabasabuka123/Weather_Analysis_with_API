
import requests
import csv
from datetime import datetime, timedelta

# Replace 'YOUR_API_KEY' with your actual API key from OpenWeatherMap
API_KEY = 'f43e3a784877b50342496s'

# Replace 'YOUR_GEOCODING_API_KEY' with your actual API key from OpenCage Geocoder
GEOCODING_API_KEY = '16b62039123s'

# List of countries in Europe
countries = ['United Kingdom', 'France', 'Germany', 'Italy', 'Spain', 'Netherlands', 'Austria', 'Greece', 'Czech Republic',
             'Sweden', 'Ireland', 'Portugal', 'Hungary', 'Poland', 'Switzerland', 'Norway', 'Spain', 'Finland', 'Denmark', 'Russia']

# Create an empty list to store the weather and geolocation data for each country
country_data = []

# Iterate over the countries and fetch weather and geolocation data for each country
for country in countries:
    # Fetch current weather data
    current_weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={country}&appid={API_KEY}&units=metric'
    current_weather_response = requests.get(current_weather_url)
    current_weather_data = current_weather_response.json()
    
    # Extract relevant current weather information from the API response
    current_temperature = current_weather_data['main']['temp']
    current_humidity = current_weather_data['main']['humidity']
    current_description = current_weather_data['weather'][0]['description']
    current_wind_speed = current_weather_data['wind']['speed']
    current_sunrise_timestamp = current_weather_data['sys']['sunrise']
    current_sunset_timestamp = current_weather_data['sys']['sunset']
    current_pressure = current_weather_data['main']['pressure']
    current_visibility = current_weather_data.get('visibility', 'N/A')
    
    # Convert sunrise and sunset timestamps to local time
    current_sunrise_time = datetime.fromtimestamp(current_sunrise_timestamp).strftime('%H:%M:%S')
    current_sunset_time = datetime.fromtimestamp(current_sunset_timestamp).strftime('%H:%M:%S')
    
    # Fetch geolocation data
    geocoding_url = f'https://api.opencagedata.com/geocode/v1/json?q={country}&key={GEOCODING_API_KEY}'
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()
    
    # Extract latitude and longitude from the geolocation API response
    latitude = geocoding_data['results'][0]['geometry']['lat']
    longitude = geocoding_data['results'][0]['geometry']['lng']
    
    # Create a dictionary with the weather and geolocation information for the country
    country_info = {
        'Country': country,
        'Latitude': latitude,
        'Longitude': longitude,
        'Temperature (°C)': current_temperature,
        'Humidity (%)': current_humidity,
        'Description': current_description,
        'Wind Speed (m/s)': current_wind_speed,
        'Sunrise Time': current_sunrise_time,
        'Sunset Time': current_sunset_time,
        'Pressure (hPa)': current_pressure,
        'Visibility': current_visibility
    }
    
    # Append the country information to the list
    country_data.append(country_info)

# Define the path and name of the CSV file
csv_file = 'weather_geolocation_data.csv'

# Define the CSV headers
csv_headers = ['Country', 'Latitude', 'Longitude', 'Temperature (°C)', 'Humidity (%)', 'Description', 'Wind Speed (m/s)',
               'Sunrise Time', 'Sunset Time', 'Pressure (hPa)', 'Visibility']

# Write the weather and geolocation data to the CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)
    writer.writeheader()
    writer.writerows(country_data)

print(f"Weather and geolocation data has been saved to '{csv_file}'.")

