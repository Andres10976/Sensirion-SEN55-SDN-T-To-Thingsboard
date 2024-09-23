import logging
from typing import Dict, Any, Optional
from sensirion_i2c_driver import I2cConnection, LinuxI2cTransceiver
from sensirion_i2c_sen5x import Sen5xI2cDevice

logger = logging.getLogger(__name__)

class DeviceConnector:
    def __init__(self, i2c_port: str):
        self.i2c_port = i2c_port
        self.i2c_transceiver: Optional[LinuxI2cTransceiver] = None
        self.device: Optional[Sen5xI2cDevice] = None

    def connect(self) -> bool:
        try:
            self.i2c_transceiver = LinuxI2cTransceiver(self.i2c_port)
            self.i2c_transceiver.__enter__()
            self.device = Sen5xI2cDevice(I2cConnection(self.i2c_transceiver))
            logger.info(f"Successfully connected to SEN5x device on port {self.i2c_port}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to SEN5x device: {e}")
            return False

    def get_device_info(self) -> Dict[str, str]:
        if not self.device:
            logger.error("Attempted to get device info, but device is not connected")
            raise ValueError("Device not connected")
        info = {
            "version": str(self.device.get_version()),
            "product_name": self.device.get_product_name(),
            "serial_number": self.device.get_serial_number()
        }
        logger.info(f"Retrieved device info: {info}")
        return info

    def start_measurement(self) -> bool:
        if not self.device:
            logger.error("Attempted to start measurement, but device is not connected")
            return False
        try:
            self.device.start_measurement()
            logger.info("Measurement started successfully")
            return True
        except Exception as e:
            logger.error(f"Error starting measurement: {e}")
            return False

    def read_data(self) -> Optional[Dict[str, float]]:
        if not self.device:
            logger.error("Attempted to read data, but device is not connected")
            return None
        try:
            if self.device.read_data_ready():
                values = self.device.read_measured_values()
                telemetry = {
                    "pm1.0": values.mass_concentration_1p0.physical,
                    "pm2.5": values.mass_concentration_2p5.physical,
                    "pm4.0": values.mass_concentration_4p0.physical,
                    "pm10.0": values.mass_concentration_10p0.physical,
                    "humidity": values.ambient_humidity.percent_rh,
                    "temperature": values.ambient_temperature.degrees_celsius
                }
                voc_index = getattr(values.voc_index, 'scaled', None)
                if voc_index is not None:
                    telemetry["voc_index"] = voc_index
                nox_index = getattr(values.nox_index, 'scaled', None)
                if nox_index is not None:
                    telemetry["nox_index"] = nox_index
                logger.debug(f"Read data: {telemetry}")
                return telemetry
            logger.debug("No new data available")
            return None
        except Exception as e:
            logger.error(f"Error reading data: {e}")
            return None

    def start_fan_cleaning(self) -> None:
        if not self.device:
            logger.error("Attempted to start fan cleaning, but device is not connected")
            return
        try:
            self.device.start_fan_cleaning()
            logger.info("Fan cleaning started")
        except Exception as e:
            logger.error(f"Error starting fan cleaning: {e}")

    def stop_measurement(self) -> None:
        if not self.device:
            logger.error("Attempted to stop measurement, but device is not connected")
            return
        try:
            self.device.stop_measurement()
            logger.info("Measurement stopped")
        except Exception as e:
            logger.error(f"Error stopping measurement: {e}")