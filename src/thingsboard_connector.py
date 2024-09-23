import logging
from typing import Dict, Optional
from tb_device_mqtt import TBDeviceMqttClient

logger = logging.getLogger(__name__)

class ThingsBoardConnector:
    def __init__(self, host: str, port: int, token: str):
        self.host = host
        self.port = port
        self.token = token
        self.client: Optional[TBDeviceMqttClient] = None

    def connect(self) -> bool:
        try:
            self.client = TBDeviceMqttClient(self.host, self.port, self.token)
            self.client.connect()
            logger.info(f"Successfully connected to ThingsBoard at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to ThingsBoard: {e}")
            return False

    def send_telemetry(self, telemetry: Dict[str, float]) -> None:
        if not self.client:
            logger.error("Attempted to send telemetry, but ThingsBoard client is not connected")
            return
        self.client.send_telemetry(telemetry)
        logger.debug(f"Sent telemetry: {telemetry}")

    def send_attributes(self, attributes: Dict[str, str]) -> None:
        if not self.client:
            logger.error("Attempted to send attributes, but ThingsBoard client is not connected")
            return
        self.client.send_attributes(attributes)
        logger.debug(f"Sent attributes: {attributes}")

    def disconnect(self) -> None:
        if self.client:
            self.client.disconnect()
            logger.info("Disconnected from ThingsBoard")