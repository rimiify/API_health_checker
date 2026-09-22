import logging
from pathlib import Path


LOG_FILE = Path("logs/api_health.log")


def setup_logger():
    """
    Configure application logging.
    """

    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return logging.getLogger("api_health_checker")