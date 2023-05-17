from geopy.geocoders import Nominatim
import geocoder
import requests


API_KEY = 'YOUR API KEY' # change to your open weather api key
METRIC = 'metric' # default unit system
USER_AGENT = 'YOUR USER' # change to your desired user agent

def get_location():
    # Returns a tuple with device latitude and longitude

    loc = geocoder.ip('me')
    return loc.latlng

def get_weather_data(lat, lon, api_key, unit_system, language='en'):
    # Returns current weather data for given latitude and longitude

    link = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={unit_system}&lang={language}'
    return requests.get(link).json()

def get_forecast_data(lat, lon, api_key, unit_system, language='en'):
    # Returns weather forecast data for given latitude and longitude

    link = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units={unit_system}&lang={language}'
    return requests.get(link).json()

def get_address(lat, lon):
    # Returns a string with the device address

    geolocator = Nominatim(user_agent=USER_AGENT)
    location = geolocator.reverse(f"{lat}, {lon}")
    return location.address

def get_temperature_unit(country):
    # Returns the temperature unit based on the country

    if country == 'United States Of America' or country == 'USA' or country == 'U.S.A.' or country == 'United States':
        return '°F'
    return '°C'

def format_values(values):
    # Returns a formatted string with weather data

    weather_desc = values['weather'][0]['description']
    temperature = values['main']['temp']
    temp_min = values['main']['temp_min']
    temp_max = values['main']['temp_max']
    humidity = values['main']['humidity'] 
    return f'{weather_desc}, {temperature}, {temp_max}, {temp_min}, {humidity}'

def print_weather_info(city, state, temperature, metric, weather_desc, humidity, temp_max, temp_min):
    # Prints weather information
    
    print(f'Weather in {city}, {state}\n')
    print(f'{temperature}{metric} {weather_desc} with {humidity}% humidity\n')
    print(f'Maximum of {temp_max}{metric} and minimum of {temp_min}{metric}\n\n')

def print_forecast_info(tomorrow, day, city, state, temperature, metric, weather_desc, humidity, temp_max, temp_min):
    # Prints weather forecast information

    if tomorrow == 1:
        print(f'Tomorrow {day}:\n')
    else:
        print(f'{day}:\n')
    print_weather_info(city, state, temperature, metric, weather_desc, humidity, temp_max, temp_min)

def split_list(lista):
    # Split the information from the list to a string

    weather = lista['weather'][0]['description']

    temperature = lista['main']['temp']

    temp_min = lista['main']['temp_min']
    temp_max = lista['main']['temp_max']

    humidity = lista['main']['humidity'] 

    splited = f'{weather}, {temperature}, {temp_max}, {temp_min}, {humidity}'

    return splited


def main():
    # Start the actually app

    lat, lon = get_location()
    location = get_address(lat, lon)

    location = location.split(',')
    country = location[-1]
    state = location[-4]
    city = location[0]
    metric = get_temperature_unit(country)
    unit_sis = 'metric'
    if metric == '°F':
        unit_sis = 'imperial'
    
    weather_data = get_weather_data(lat, lon, API_KEY, unit_sis)
    forecast_data = get_forecast_data(lat, lon, API_KEY, unit_sis)

    temperature = round(weather_data['main']['temp'])
    weather_desc = weather_data['weather'][0]['description']
    humidity = weather_data['main']['humidity']
    temp_max = round(weather_data['main']['temp_max'])
    temp_min = round(weather_data['main']['temp_min'])


    # Get weather forecast for today

    print('Today: \n')
    print_weather_info(city, state, temperature, metric, weather_desc, humidity, temp_max, temp_min)

    # Get weather forecast for next 5 days

    x = 1

    forecast_list = forecast_data['list']

    for i in range(0,39):
    
        time = forecast_list[i]['dt_txt'].split()

        forecast_date, hour = time

        if hour == '12:00:00':

            value = split_list(forecast_list[i])

            
            forecast_weather, forecast_temperature, forecast_temp_max, forecast_temp_min, forecast_humidity = value.split(',')
            forecast_temperature = float(forecast_temperature)
            forecast_temp_max = float(forecast_temp_max)
            forecast_temp_min = float(forecast_temp_min)

            print_forecast_info(x, forecast_date, city, state, round(forecast_temperature), metric, forecast_weather, forecast_humidity, round(forecast_temp_max), round(forecast_temp_min))
            
            x += 1
            

main()


