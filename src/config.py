import yaml
import logging
import sys
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

# Get the absolute path to the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def load_config() -> Dict[str, Any]:
    config_path = PROJECT_ROOT / 'config' / 'config.yml'
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logger.info("Configuration loaded successfully")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        sys.exit(1)