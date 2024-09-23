import signal
import sys
import logging
from src.config import load_config
from src.sen5x_reader import Sen5xReader
import time
import logging
from pathlib import Path

# Get the absolute path to the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Create the logs directory if it doesn't exist
logs_dir = PROJECT_ROOT / 'logs'
logs_dir.mkdir(exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(logs_dir / "sen5x_reader.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def signal_handler(sig, frame):
    logger.info("Received signal to stop. Shutting down...")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    logger.info("Starting Sen5x Reader")
    config = load_config()
    reader = Sen5xReader(config)

    retry_interval = 5
    max_retry_interval = 300

    while True:
        if reader.connect() and reader.start_measurement():
            try:
                reader.run()
            except Exception as e:
                logger.error(f"An error occurred during run: {e}")
        else:
            logger.warning(f"Failed to initialize. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
            retry_interval = min(retry_interval * 2, max_retry_interval)  

        reader.stop()

if __name__ == "__main__":
    main()