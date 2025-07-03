import os
import requests
import openpyxl
from dotenv import load_dotenv
from datetime import datetime, timezone

def get_weather_data(latitude: float, longitude: float) -> dict | None:
    """
    Retrieve current weather data from OpenWeatherMap API.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Returns:
        dict | None: Extracted weather data or None if API call fails.
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("Error: API_KEY not found in environment variables.")
        return None

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # city name is included in the API response
        weather_data = {
            "city": data.get("name"),
            "temperature_celsius": data["main"].get("temp"),
            "humidity": data["main"].get("humidity"),
            "wind_speed": data["wind"].get("speed"),
            "description": data["weather"][0].get("description").capitalize(),
            "timestamp": datetime.fromtimestamp(data.get("dt"), tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        }
        return weather_data

    except requests.RequestException as e:
        print(f"Error retrieving weather data: {e}")
        return None
    except (KeyError, TypeError) as e:
        print(f"Unexpected data format: {e}")
        return None

def generate_excel_file(weather_data: dict) -> None:
    """
    Create an Excel file containing the weather data.

    Args:
        weather_data (dict): Weather data to write to Excel file.
    """
    if not weather_data:
        print("No weather data provided. Excel file not generated.")
        return

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Sheet1"

    headers = [
        "City",
        "Temperature (Celsius)",
        "Temperature (Fahrenheit)",
        "Description",
        "Humidity (%)",
        "Wind Speed (m/s)",
        "Timestamp",
    ]
    sheet.append(headers)

    temp_c = weather_data["temperature_celsius"]
    temp_f = round((temp_c * 9 / 5) + 32, 2)

    row = [
        weather_data["city"],
        temp_c,
        temp_f,
        weather_data["description"],
        weather_data["humidity"],
        weather_data["wind_speed"],
        weather_data["timestamp"],
    ]
    sheet.append(row)

    # dynamic file name based on city name
    filename = f"weather_data_{weather_data['city']}.xlsx"
    workbook.save(filename)

def main():
    load_dotenv()

    # coordinates for London
    latitude = 51.5074
    longitude = -0.1278

    weather_data = get_weather_data(latitude, longitude)

    if weather_data:
        print("Weather data:")
        for key, value in weather_data.items():
            print(f"{key}: {value}")
        generate_excel_file(weather_data)
    else:
        print("Failed to retrieve or process weather data.")

if __name__ == "__main__":
    main()