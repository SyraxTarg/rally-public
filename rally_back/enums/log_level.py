"""This file contains the enum for log level"""
from enum import Enum

class LogLevelEnum(str, Enum):
    """used for log level in action logs"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
