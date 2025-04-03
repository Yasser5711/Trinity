import json
import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = (
            logger.level(record.levelname).name
            if record.levelname in logger._levels
            else record.levelno
        )
        logger.log(level, record.getMessage())


def setup_logger():
    logger.remove()  # Remove default handler

    def serialize_log(record):
        return json.dumps(
            {
                "timestamp": record["time"].strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "level": record["level"].name,
                "message": record["message"],
                "module": record["module"],
                "function": record["function"],
                "line": record["line"],
            }
        )

    logger.add(sys.stdout, format=serialize_log, level="DEBUG", serialize=False)

    # Redirect stdlib logging to loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)
