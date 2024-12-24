"""
作者：Yuanl
日期：2024年12月24日
"""
from loguru import logger

logger.add("log/log_{time}.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}", rotation="200 MB")

if __name__ == "__main__":
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")