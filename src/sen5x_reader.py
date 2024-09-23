import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any
from src.device_connector import DeviceConnector
from src.thingsboard_connector import ThingsBoardConnector
from tabulate import tabulate

logger = logging.getLogger(__name__)

class Sen5xReader:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.device_connector = DeviceConnector(config['i2c_port'])
        self.tb_connector = ThingsBoardConnector(config['tb_host'], config['tb_port'], config['tb_token'])
        self.running = False
        self.last_fan_cleaning = datetime.now()
        self.fan_cleaning_interval = timedelta(hours=24)

    def pretty_print_telemetry(self, telemetry):
        table_data = [
            ["PM1.0", f"{telemetry['pm1.0']}"],
            ["PM2.5", f"{telemetry['pm2.5']}"],
            ["PM4.0", f"{telemetry['pm4.0']}"],
            ["PM10.0", f"{telemetry['pm10.0']}"],
            ["Humidity", f"{telemetry['humidity']}%"],
            ["Temperature", f"{telemetry['temperature']}°C"],
            ["VOC Index", f"{telemetry['voc_index']}"],
            ["NOx Index", f"{telemetry['nox_index']}"]
        ]
        
        table = tabulate(table_data, headers=["Measurement", "Value"], tablefmt="pretty")
        
        logger.info(f"New telemetry data:\n{table}")

    def connect(self) -> bool:
        device_connected = self.device_connector.connect()
        tb_connected = self.tb_connector.connect()
        if device_connected and tb_connected:
            logger.info("Successfully connected to both SEN5x device and ThingsBoard")
            return True
        else:
            logger.error("Failed to connect to either SEN5x device or ThingsBoard")
            return False

    def start_measurement(self) -> bool:
        return self.device_connector.start_measurement()

    def run(self) -> None:
        self.running = True
        device_info = self.device_connector.get_device_info()
        self.tb_connector.send_attributes(device_info)
        
        while self.running:
            self.check_and_run_fan_cleaning()
            telemetry = self.device_connector.read_data()
            if telemetry:
                self.pretty_print_telemetry(telemetry)
                self.tb_connector.send_telemetry(telemetry)
            else:
                logger.debug("Waiting for new data...")
            time.sleep(self.config['publish_interval'])

    def check_and_run_fan_cleaning(self) -> None:
        if datetime.now() - self.last_fan_cleaning >= self.fan_cleaning_interval:
            logger.info("Starting scheduled fan cleaning...")
            self.device_connector.start_fan_cleaning()
            self.last_fan_cleaning = datetime.now()

    def stop(self) -> None:
        self.running = False
        self.device_connector.stop_measurement()
        self.tb_connector.disconnect()
        logger.info("Sen5x Reader stopped")
