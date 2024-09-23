# Sen5x Reader

This project reads data from a Sensirion SEN5x environmental sensor and publishes it to ThingsBoard.

## Setup

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Configure the `config/config.yml` file with your ThingsBoard and I2C settings.

3. Run the script:
   ```
   python src/main.py
   ```

## Project Structure

- `src/`: Contains the main Python modules
- `config/`: Contains the configuration file
- `logs/`: Directory where log files are stored
- `requirements.txt`: List of Python dependencies
- `README.md`: Project documentation

## Modules

- `main.py`: Entry point of the application
- `device_connector.py`: Handles connection and communication with the SEN5x device
- `thingsboard_connector.py`: Manages connection and data publishing to ThingsBoard
- `sen5x_reader.py`: Orchestrates the reading and publishing process
- `config.py`: Loads the configuration from the YAML file
