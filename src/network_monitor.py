import psutil
import subprocess
import platform
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class NetworkStats:
    """Data class for network statistics"""
    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int
    timestamp: datetime
    interface: str = "total"

@dataclass
class SystemStats:
    """Data class for system statistics"""
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: NetworkStats
    timestamp: datetime

@dataclass
class DeviceStatus:
    """Data class for device status"""
    ip_address: str
    is_reachable: bool
    response_time: Optional[float]
    timestamp: datetime

class NetworkMonitor:
    """Core network monitoring functionality"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.previous_network_io = None
        self.bandwidth_history = []
        
    def get_network_stats(self) -> NetworkStats:
        """Get current network I/O statistics"""
        try:
            io_counters = psutil.net_io_counters()
            return NetworkStats(
                bytes_sent=io_counters.bytes_sent,
                bytes_recv=io_counters.bytes_recv,
                packets_sent=io_counters.packets_sent,
                packets_recv=io_counters.packets_recv,
                timestamp=datetime.now()
            )
        except Exception as e:
            self.logger.error(f"Error getting network stats: {e}")
            raise
    
    def calculate_bandwidth_usage(self, current_stats: NetworkStats) -> Tuple[float, float]:
        """Calculate bandwidth usage in Mbps"""
        if self.previous_network_io is None:
            self.previous_network_io = current_stats
            return 0.0, 0.0
        
        # Calculate time difference
        time_diff = (current_stats.timestamp - self.previous_network_io.timestamp).total_seconds()
        
        if time_diff <= 0:
            return 0.0, 0.0
        
        # Calculate bytes per second
        bytes_sent_per_sec = (current_stats.bytes_sent - self.previous_network_io.bytes_sent) / time_diff
        bytes_recv_per_sec = (current_stats.bytes_recv - self.previous_network_io.bytes_recv) / time_diff
        
        # Convert to Mbps
        upload_mbps = (bytes_sent_per_sec * 8) / (1024 * 1024)
        download_mbps = (bytes_recv_per_sec * 8) / (1024 * 1024)
        
        # Update previous stats
        self.previous_network_io = current_stats
        
        # Store in history (keep last 100 measurements)
        self.bandwidth_history.append({
            'timestamp': current_stats.timestamp,
            'upload_mbps': upload_mbps,
            'download_mbps': download_mbps
        })
        
        if len(self.bandwidth_history) > 100:
            self.bandwidth_history.pop(0)
        
        return upload_mbps, download_mbps
    
    def get_system_stats(self) -> SystemStats:
        """Get comprehensive system statistics"""
        try:
            network_stats = self.get_network_stats()
            
            return SystemStats(
                cpu_percent=psutil.cpu_percent(interval=1),
                memory_percent=psutil.virtual_memory().percent,
                disk_percent=psutil.disk_usage('/').percent,
                network_io=network_stats,
                timestamp=datetime.now()
            )
        except Exception as e:
            self.logger.error(f"Error getting system stats: {e}")
            raise
    
    def ping_device(self, ip_address: str, timeout: int = 5) -> DeviceStatus:
        """Ping a device to check reachability"""
        try:
            # Determine ping command based on OS
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), ip_address]
            else:
                cmd = ["ping", "-c", "1", "-W", str(timeout), ip_address]
            
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 2)
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            is_reachable = result.returncode == 0
            
            return DeviceStatus(
                ip_address=ip_address,
                is_reachable=is_reachable,
                response_time=response_time if is_reachable else None,
                timestamp=datetime.now()
            )
            
        except subprocess.TimeoutExpired:
            self.logger.warning(f"Ping timeout for {ip_address}")
            return DeviceStatus(
                ip_address=ip_address,
                is_reachable=False,
                response_time=None,
                timestamp=datetime.now()
            )
        except Exception as e:
            self.logger.error(f"Error pinging {ip_address}: {e}")
            return DeviceStatus(
                ip_address=ip_address,
                is_reachable=False,
                response_time=None,
                timestamp=datetime.now()
            )
    
    def get_network_interfaces(self) -> Dict[str, Dict]:
        """Get network interface information"""
        try:
            interfaces = {}
            for interface_name, addresses in psutil.net_if_addrs().items():
                interface_stats = psutil.net_if_stats().get(interface_name)
                
                interfaces[interface_name] = {
                    'addresses': [
                        {
                            'family': addr.family.name if hasattr(addr.family, 'name') else str(addr.family),
                            'address': addr.address,
                            'netmask': addr.netmask,
                            'broadcast': addr.broadcast
                        }
                        for addr in addresses
                    ],
                    'is_up': interface_stats.isup if interface_stats else False,
                    'speed': interface_stats.speed if interface_stats else None,
                    'mtu': interface_stats.mtu if interface_stats else None
                }
            
            return interfaces
        except Exception as e:
            self.logger.error(f"Error getting network interfaces: {e}")
            return {}
    
    def detect_anomalies(self, upload_mbps: float, download_mbps: float, threshold: float) -> List[str]:
        """Detect network traffic anomalies"""
        anomalies = []
        
        # Check if current usage exceeds threshold
        if upload_mbps > threshold:
            anomalies.append(f"High upload traffic: {upload_mbps:.2f} Mbps (threshold: {threshold} Mbps)")
        
        if download_mbps > threshold:
            anomalies.append(f"High download traffic: {download_mbps:.2f} Mbps (threshold: {threshold} Mbps)")
        
        # Check for sudden spikes (if we have enough history)
        if len(self.bandwidth_history) >= 10:
            recent_avg_upload = sum(h['upload_mbps'] for h in self.bandwidth_history[-10:]) / 10
            recent_avg_download = sum(h['download_mbps'] for h in self.bandwidth_history[-10:]) / 10
            
            # If current usage is 3x the recent average, flag as anomaly
            if upload_mbps > recent_avg_upload * 3 and upload_mbps > 10:  # Minimum 10 Mbps to avoid false positives
                anomalies.append(f"Upload spike detected: {upload_mbps:.2f} Mbps (avg: {recent_avg_upload:.2f} Mbps)")
            
            if download_mbps > recent_avg_download * 3 and download_mbps > 10:
                anomalies.append(f"Download spike detected: {download_mbps:.2f} Mbps (avg: {recent_avg_download:.2f} Mbps)")
        
        return anomalies
