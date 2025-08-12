import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration management for the network monitoring system"""
    
    # SMTP Configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    ALERT_RECIPIENTS = os.getenv('ALERT_RECIPIENTS', '').split(',')
    
    # Monitoring Thresholds
    BANDWIDTH_THRESHOLD_MBPS = float(os.getenv('BANDWIDTH_THRESHOLD_MBPS', 100))
    CPU_THRESHOLD_PERCENT = float(os.getenv('CPU_THRESHOLD_PERCENT', 80))
    MEMORY_THRESHOLD_PERCENT = float(os.getenv('MEMORY_THRESHOLD_PERCENT', 85))
    DISK_THRESHOLD_PERCENT = float(os.getenv('DISK_THRESHOLD_PERCENT', 90))
    PING_TIMEOUT_SECONDS = int(os.getenv('PING_TIMEOUT_SECONDS', 5))
    
    # Monitoring Intervals
    NETWORK_CHECK_INTERVAL = int(os.getenv('NETWORK_CHECK_INTERVAL', 30))
    SYSTEM_CHECK_INTERVAL = int(os.getenv('SYSTEM_CHECK_INTERVAL', 60))
    DEVICE_PING_INTERVAL = int(os.getenv('DEVICE_PING_INTERVAL', 120))
    
    # Devices to monitor
    MONITORED_DEVICES = os.getenv('MONITORED_DEVICES', '8.8.8.8,1.1.1.1').split(',')
    
    # Alert Settings
    ALERT_COOLDOWN_MINUTES = int(os.getenv('ALERT_COOLDOWN_MINUTES', 15))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/network_monitor.log')
    
    @classmethod
    def setup_logging(cls):
        """Setup logging configuration"""
        os.makedirs(os.path.dirname(cls.LOG_FILE), exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(cls.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration"""
        required_configs = {
            'EMAIL_USER': cls.EMAIL_USER,
            'EMAIL_PASSWORD': cls.EMAIL_PASSWORD
        }
        
        missing_configs = [key for key, value in required_configs.items() if not value]
        
        if missing_configs:
            raise ValueError(f"Missing required configuration: {', '.join(missing_configs)}")
        
        return True
