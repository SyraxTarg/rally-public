"""This file contains the enum payment status"""
from enum import Enum

class PaymentStatusEnum(str, Enum):
    """used for status in payments"""
    SUCCESS = "success"
    PENDING = "pending"
    FAILED = "failed"
    FREE = "free"
