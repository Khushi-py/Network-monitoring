import json
import os
from datetime import datetime
from typing import Dict, List, Any
import logging

class DataLogger:
    """Handles data logging and storage for network monitoring"""
    
    def __init__(self, data_directory: str = 'data'):
        self.data_directory = data_directory
        self.logger = logging.getLogger(__name__)
        
        # Ensure data directory exists
        os.makedirs(data_directory, exist_ok=True)
        
        # Initialize data files
        self.network_data_file = os.path.join(data_directory, 'network_data.json')
        self.system_data_file = os.path.join(data_directory, 'system_data.json')
        self.device_data_file = os.path.join(data_directory, 'device_data.json')
        self.alert_data_file = os.path.join(data_directory, 'alert_data.json')
    
    def _load_data_file(self, filename: str) -> List[Dict]:
        """Load data from JSON file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.logger.error(f"Error loading data file {filename}: {e}")
            return []
    
    def _save_data_file(self, filename: str, data: List[Dict]) -> bool:
        """Save data to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            self.logger.error(f"Error saving data file {filename}: {e}")
            return False
    
    def _cleanup_old_data(self, data: List[Dict], max_records: int = 10000) -> List[Dict]:
        """Keep only the most recent records"""
        if len(data) > max_records:
            # Sort by timestamp and keep the most recent
            data.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return data[:max_records]
        return data
    
    def log_network_data(self, upload_mbps: float, download_mbps: float, 
                        network_stats, anomalies: List[str] = None) -> bool:
        """Log network monitoring data"""
        try:
            data = self._load_data_file(self.network_data_file)
            
            record = {
                'timestamp': datetime.now().isoformat(),
                'upload_mbps': upload_mbps,
                'download_mbps': download_mbps,
                'bytes_sent': network_stats.bytes_sent,
                'bytes_recv': network_stats.bytes_recv,
                'packets_sent': network_stats.packets_sent,
                'packets_recv': network_stats.packets_recv,
                'anomalies': anomalies or []
            }
            
            data.append(record)
            data = self._cleanup_old_data(data)
            
            return self._save_data_file(self.network_data_file, data)
            
        except Exception as e:
            self.logger.error(f"Error logging network data: {e}")
            return False
    
    def log_system_data(self, system_stats) -> bool:
        """Log system monitoring data"""
        try:
            data = self._load_data_file(self.system_data_file)
            
            record = {
                'timestamp': system_stats.timestamp.isoformat(),
                'cpu_percent': system_stats.cpu_percent,
                'memory_percent': system_stats.memory_percent,
                'disk_percent': system_stats.disk_percent
            }
            
            data.append(record)
            data = self._cleanup_old_data(data)
            
            return self._save_data_file(self.system_data_file, data)
            
        except Exception as e:
            self.logger.error(f"Error logging system data: {e}")
            return False
    
    def log_device_data(self, device_statuses: List) -> bool:
        """Log device monitoring data"""
        try:
            data = self._load_data_file(self.device_data_file)
            
            for status in device_statuses:
                record = {
                    'timestamp': status.timestamp.isoformat(),
                    'ip_address': status.ip_address,
                    'is_reachable': status.is_reachable,
                    'response_time': status.response_time
                }
                data.append(record)
            
            data = self._cleanup_old_data(data)
            
            return self._save_data_file(self.device_data_file, data)
            
        except Exception as e:
            self.logger.error(f"Error logging device data: {e}")
            return False
    
    def log_alert_data(self, alerts: List) -> bool:
        """Log alert data"""
        try:
            data = self._load_data_file(self.alert_data_file)
            
            for alert in alerts:
                record = {
                    'timestamp': alert.timestamp.isoformat(),
                    'alert_type': alert.alert_type,
                    'message': alert.message,
                    'severity': alert.severity,
                    'resolved': alert.resolved
                }
                data.append(record)
            
            data = self._cleanup_old_data(data)
            
            return self._save_data_file(self.alert_data_file, data)
            
        except Exception as e:
            self.logger.error(f"Error logging alert data: {e}")
            return False
    
    def get_network_history(self, hours: int = 24) -> List[Dict]:
        """Get network data history for specified hours"""
        try:
            data = self._load_data_file(self.network_data_file)
            
            # Filter data for the specified time period
            cutoff_time = datetime.now().timestamp() - (hours * 3600)
            
            filtered_data = []
            for record in data:
                try:
                    record_time = datetime.fromisoformat(record['timestamp']).timestamp()
                    if record_time >= cutoff_time:
                        filtered_data.append(record)
                except:
                    continue
            
            return filtered_data
            
        except Exception as e:
            self.logger.error(f"Error getting network history: {e}")
            return []
    
    def get_system_history(self, hours: int = 24) -> List[Dict]:
        """Get system data history for specified hours"""
        try:
            data = self._load_data_file(self.system_data_file)
            
            # Filter data for the specified time period
            cutoff_time = datetime.now().timestamp() - (hours * 3600)
            
            filtered_data = []
            for record in data:
                try:
                    record_time = datetime.fromisoformat(record['timestamp']).timestamp()
                    if record_time >= cutoff_time:
                        filtered_data.append(record)
                except:
                    continue
            
            return filtered_data
            
        except Exception as e:
            self.logger.error(f"Error getting system history: {e}")
            return []
    
    def get_device_history(self, ip_address: str = None, hours: int = 24) -> List[Dict]:
        """Get device data history for specified device and time period"""
        try:
            data = self._load_data_file(self.device_data_file)
            
            # Filter data for the specified time period
            cutoff_time = datetime.now().timestamp() - (hours * 3600)
            
            filtered_data = []
            for record in data:
                try:
                    record_time = datetime.fromisoformat(record['timestamp']).timestamp()
                    if record_time >= cutoff_time:
                        if ip_address is None or record.get('ip_address') == ip_address:
                            filtered_data.append(record)
                except:
                    continue
            
            return filtered_data
            
        except Exception as e:
            self.logger.error(f"Error getting device history: {e}")
            return []
    
    def get_alert_history(self, hours: int = 24) -> List[Dict]:
        """Get alert history for specified hours"""
        try:
            data = self._load_data_file(self.alert_data_file)
            
            # Filter data for the specified time period
            cutoff_time = datetime.now().timestamp() - (hours * 3600)
            
            filtered_data = []
            for record in data:
                try:
                    record_time = datetime.fromisoformat(record['timestamp']).timestamp()
                    if record_time >= cutoff_time:
                        filtered_data.append(record)
                except:
                    continue
            
            return filtered_data
            
        except Exception as e:
            self.logger.error(f"Error getting alert history: {e}")
            return []
    
    def export_data(self, filename: str, data_type: str = 'all', hours: int = 24) -> bool:
        """Export data to a file"""
        try:
            export_data = {}
            
            if data_type in ['all', 'network']:
                export_data['network'] = self.get_network_history(hours)
            
            if data_type in ['all', 'system']:
                export_data['system'] = self.get_system_history(hours)
            
            if data_type in ['all', 'device']:
                export_data['device'] = self.get_device_history(hours=hours)
            
            if data_type in ['all', 'alert']:
                export_data['alert'] = self.get_alert_history(hours)
            
            export_data['export_timestamp'] = datetime.now().isoformat()
            export_data['export_period_hours'] = hours
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            self.logger.info(f"Data exported to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting data: {e}")
            return False
