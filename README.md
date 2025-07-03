1. While developing this task i used a `.env` enviroment file with variable `API_KEY`
where i stored my OpenWeatherMap API key. To run the script on your machine you'd have
to <u>create a similar file with your own key</u>.

2. `requirements.txt` file contains list of all the necessary packages required to run the script.
To install them (ideally while in a virtual environment) use: `pip install -r requirements.txt`.

3. The `weather_data_London.xlsx` file can be deleted as it is included only for preview purposes and is 
automatically generated when running the script. The hardcoded `latitude` and `longitude` values can be
changed to dynamically retrieve weather data for another location. The Excel file name will adjust accordingly.

Used Python 3.12.0. I mention it because in the requirements it says any version later than 3.0 is acceptable.