# weather_forecast

This app uses [openWeatherMap API One Call](https://openweathermap.org/api/one-call-api) to retrieve an hourly weather forecast.
The idea is for PLC logic operating the control system to discover this app and pull in weather data from the web to optmize the HVAC systems. Examples can include:

### Pre-building occupancy economizer free cooling flush
* At 5AM after the hourly weather data is retrieved and updated via BACnet, if the current dewpoint is ideal for free cooling (Current-Dewpoint) is below 60°F (adj.) and the hourly weather forecast data for the next 24 hours yields a hot humid day coming up requiring heavy mechanical cooling use (IE., the outside air dry bulb will be greater than 80°F (adj.)) run a building pre-occupancy sequence to economizer pre-cool of the building. To further elaborate if these weather conditions are True in PLC code on the control system start air handling units (AHU) early for a 2 hour (adj.) flush of the building in a free cooling economizer mode with lowering all zone setpoints by -2°F. When building is occupied slowly reset zone setpoints upward where during hottest hours of the day zone setpoints would be +2°F (adj.).

## Discoverable BACnet points

* `Next 24Hours-Hi-Temp` (Analog Value 0)
* `Next 24Hours-Hi-Humidity` (Analog Value 1)
* `Next 24Hours-Hi-Dewpoint` (Analog Value 2)
* `Current-Temp` (Analog Value 3)
* `Current-Humidity` (Analog Value 4)
* `Current-Dewpoint` (Analog Value 5)
* `Web-Weather-Error` (Binary Value 0)

### Note
* `Next 24Hours-Hi-Humidity` and `Next 24Hours-Hi-Dewpoint` represents the weather data active during the `Next 24Hours-Hi-Temp` time period. The idea is that when the hottest part of the day exists in degrees dry bulb what is also the humidity and dewpoint value during that hottest part of the day?


## With text editor modify `config.py`




## Install Python dependencies 
```bash
$ python -m pip install -r requirements.txt
```

## Run app 
```bash
$ python app.py
````

