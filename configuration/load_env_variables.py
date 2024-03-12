from dotenv import load_dotenv
from pathlib import Path

import os

from helpers.logger import logger


def load_env_variables() -> bool:
    try:
        base_dir = Path(__file__).resolve().parent.parent
        load_dotenv(dotenv_path=os.path.join(base_dir, ".env"))

        logger(
            "config",
            "success",
            "Environment variables loaded successfully",
        )

        return True
    except Exception as e:
        logger(
            "config",
            "error",
            f"Error loading environment variables: {e}",
        )

        return False
