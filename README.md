# Sensor & Quote Plugin for InkyPi

This plugin for InkyPi displays ambient sensor data and an inspirational Zen quote. 

## Features

This plugin is an extension for the [InkyPI](https://github.com/fatihak/InkyPi) e-paper display frame and includes the following features:

*   **Sensor Data Display:** Shows readings from a temperature and humidity sensor, such as a BME680.
*   **Inspirational Quote:** Displays a random Zen quote alongside the sensor data.
*   **Flexible Data Sourcing:** You can choose how to get your sensor data:
    *   **Remote (SSH):** Fetch sensor data from a device on your network.
    *   **Local (File):** Read sensor data directly from a local file.

    
## Install

Install the plugin using the InkyPi CLI, providing the plugin ID and GitHub repository URL:

```bash
inkypi install sensor_quote https://github.com/rs9000/inkypi-plugin-sensor-quote
```

## JSON Data Format

The plugin expects a JSON file with the following structure. 

```json
{
    "temperature": "22.0°C",
    "humidity": "56.8%",
    "air_quality_score": "74.1",
    "air_quality_label": "GOOD"  
}
```

Air quality labels "CLEAN AIR", "GOOD", "MEDIUM", "BAD" are mapped to colors.

## Example on e-ink display

<img src="sensor_quote/icons/sensor_quote_Bme.png" alt="Sensor and Quote Example" width="400"/>
