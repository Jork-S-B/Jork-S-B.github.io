"""
log_config.py - 日志配置模块

提供统一的日志配置，支持控制台输出和文件输出。
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_dir: str = "logs",
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5
) -> None:
    """
    配置日志系统
    
    Args:
        level: 日志级别（默认 INFO）
        log_file: 日志文件名（默认 None，仅控制台输出）
        log_dir: 日志文件目录
        max_bytes: 单个日志文件最大大小（默认 10MB）
        backup_count: 保留的日志文件数量（默认 5）
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    root_logger.addHandler(console_handler)
    
    if log_file:
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True, parents=True)
        
        file_handler = RotatingFileHandler(
            log_path / log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的日志器
    
    Args:
        name: 日志器名称（通常使用 __name__）
    
    Returns:
        logging.Logger: 日志器实例
    """
    return logging.getLogger(name)


class LogLevel:
    """日志级别常量"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


if __name__ == "__main__":
    setup_logging(level=LogLevel.DEBUG, log_file="rag.log")
    
    logger = get_logger("test")
    logger.debug("这是一条调试日志")
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")
