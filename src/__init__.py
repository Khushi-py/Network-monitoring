"""
Network Monitoring and Alert System

A comprehensive Python-based tool for monitoring network bandwidth usage,
device uptime, and system performance with automated email alerts.
"""

__version__ = "1.0.0"
__author__ = "Network Monitoring Team"
__email__ = "network@company.com"

from .config import Config
from .network_monitor import NetworkMonitor
from .alert_manager import AlertManager
from .data_logger import DataLogger

__all__ = [
    'Config',
    'NetworkMonitor', 
    'AlertManager',
    'DataLogger'
]
