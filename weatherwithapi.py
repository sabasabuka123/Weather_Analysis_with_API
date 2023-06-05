import requests
import csv
import pandas as pd
from datetime import datetime, timedelta
from opencage.geocoder import OpenCageGeocode

# Replace 'YOUR_API_KEY' with your actual API key from OpenWeatherMap
API_KEY = 'f43e3a784877b503424966b18d4b4b07'

# Replace 'YOUR_GEOCODING_API_KEY' with your actual API key from OpenCage Geocoder
GEOCODING_API_KEY = '16b6203912374ad29c7498b68cb6fbef'

# List of cities in Europe
cities = ['London', 'Paris', 'Berlin', 'Rome', 'Madrid', 'Amsterdam', 'Vienna', 'Athens', 'Prague',
          'Stockholm', 'Dublin', 'Lisbon', 'Budapest', 'Warsaw', 'Zurich', 'Oslo',
          'Barcelona', 'Helsinki', 'Copenhagen', 'Moscow']

# Create an empty list to store the weather data for each city
weather_data = []

# Create an instance of the OpenCage Geocode client
geocoder = OpenCageGeocode(GEOCODING_API_KEY)

# Function to get latitude and longitude coordinates for a given city
def get_coordinates(city):
    result = geocoder.geocode(city)
    if result and len(result):
        lat = result[0]['geometry']['lat']
        lng = result[0]['geometry']['lng']
        return lat, lng
    return None, None

# Iterate over the cities and fetch weather data for each city
for city in cities:
    # Get latitude and longitude for the city
    lat, lng = get_coordinates(city)
    
    # Fetch current weather data
    current_weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
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
    
    # Create a dictionary with the current weather information for the city
    current_weather_info = {
        'City': city,
        'Latitude': lat,
        'Longitude': lng,
        'Temperature (°C)': current_temperature,
        'Humidity (%)': current_humidity,
        'Description': current_description,
        'Wind Speed (m/s)': current_wind_speed,
        'Sunrise Time': current_sunrise_time,
        'Sunset Time': current_sunset_time,
        'Pressure (hPa)': current_pressure,
        'Visibility': current_visibility
    }
    
    # Append the current weather information to the list
    weather_data.append(current_weather_info)
    
    # Fetch forecast data
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()
    
    # Extract relevant forecast information from the API response
    forecast_list = forecast_data['list']
    forecast_items = forecast_list[:4]  # Take the first 4 forecast items (4-day forecast)
    
    for item in forecast_items:
        timestamp = item['dt']
        datetime_obj = datetime.fromtimestamp(timestamp)
        date = datetime_obj.strftime('%Y-%m-%d')
        time = datetime_obj.strftime('%H:%M:%S')
        temperature = item['main']['temp']
        humidity = item['main']['humidity']
        description = item['weather'][0]['description']
        wind_speed = item['wind']['speed']
    
    # Create a dictionary with the forecast information
    forecast_info = {
        'City': city,
        'Latitude': lat,
        'Longitude': lng,
        'Date': date,
        'Time': time,
        'Temperature (°C)': temperature,
        'Humidity (%)': humidity,
        'Description': description,
        'Wind Speed (m/s)': wind_speed,
    }
    
    # Append the forecast information to the list
    weather_data.append(forecast_info)

# Define the path and name of the CSV file
csv_file = 'weather_data.csv'

# Define the CSV headers
csv_headers = ['City', 'Latitude', 'Longitude', 'Date', 'Time', 'Temperature (°C)', 'Humidity (%)',
               'Description', 'Wind Speed (m/s)', 'Sunrise Time', 'Sunset Time',
               'Pressure (hPa)', 'Visibility']

# Write the weather and forecast data to the CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)
    writer.writeheader()
    writer.writerows(weather_data)

print(f"Weather and forecast data has been saved to '{csv_file}'.")
