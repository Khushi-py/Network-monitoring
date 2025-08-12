import logging
from scapy.all import sniff, IP, TCP, UDP
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading

class PacketAnalyzer:
    """Advanced packet analysis using Scapy"""
    
    def __init__(self, interface: str = None):
        self.logger = logging.getLogger(__name__)
        self.interface = interface
        self.packet_stats = defaultdict(int)
        self.protocol_stats = defaultdict(int)
        self.traffic_by_port = defaultdict(int)
        self.suspicious_activities = []
        self.capture_thread = None
        self.is_capturing = False
        
    def start_capture(self, duration: int = 60):
        """Start packet capture for specified duration"""
        if self.is_capturing:
            self.logger.warning("Packet capture already running")
            return
        
        self.is_capturing = True
        self.logger.info(f"Starting packet capture for {duration} seconds")
        
        def capture_packets():
            try:
                sniff(
                    iface=self.interface,
                    prn=self._process_packet,
                    timeout=duration,
                    store=False
                )
            except Exception as e:
                self.logger.error(f"Error during packet capture: {e}")
            finally:
                self.is_capturing = False
        
        self.capture_thread = threading.Thread(target=capture_packets, daemon=True)
        self.capture_thread.start()
    
    def _process_packet(self, packet):
        """Process individual packets"""
        try:
            if IP in packet:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                protocol = packet[IP].proto
                
                # Update basic stats
                self.packet_stats['total'] += 1
                self.packet_stats[f'from_{src_ip}'] += 1
                self.packet_stats[f'to_{dst_ip}'] += 1
                
                # Protocol analysis
                if TCP in packet:
                    self.protocol_stats['TCP'] += 1
                    self.traffic_by_port[packet[TCP].dport] += 1
                    
                    # Detect potential port scanning
                    if packet[TCP].flags == 2:  # SYN flag
                        self._check_port_scan(src_ip, dst_ip, packet[TCP].dport)
                
                elif UDP in packet:
                    self.protocol_stats['UDP'] += 1
                    self.traffic_by_port[packet[UDP].dport] += 1
                
                else:
                    self.protocol_stats['Other'] += 1
                
                # Check for suspicious patterns
                self._check_suspicious_activity(packet)
                
        except Exception as e:
            self.logger.error(f"Error processing packet: {e}")
    
    def _check_port_scan(self, src_ip: str, dst_ip: str, port: int):
        """Detect potential port scanning activity"""
        # Simple port scan detection - multiple ports from same source
        current_time = datetime.now()
        recent_threshold = current_time - timedelta(minutes=5)
        
        # Count recent connections from this source
        recent_ports = set()
        for activity in self.suspicious_activities:
            if (activity.get('type') == 'port_scan' and 
                activity.get('src_ip') == src_ip and
                activity.get('timestamp') > recent_threshold):
                recent_ports.add(activity.get('port'))
        
        if len(recent_ports) > 10:  # More than 10 different ports in 5 minutes
            self.suspicious_activities.append({
                'type': 'potential_port_scan',
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'port_count': len(recent_ports),
                'timestamp': current_time,
                'severity': 'high'
            })
    
    def _check_suspicious_activity(self, packet):
        """Check for other suspicious network activities"""
        if IP in packet:
            # Check for unusual packet sizes
            if len(packet) > 1500:  # Larger than typical MTU
                self.suspicious_activities.append({
                    'type': 'large_packet',
                    'src_ip': packet[IP].src,
                    'dst_ip': packet[IP].dst,
                    'size': len(packet),
                    'timestamp': datetime.now(),
                    'severity': 'medium'
                })
    
    def get_analysis_report(self) -> Dict:
        """Generate comprehensive packet analysis report"""
        total_packets = self.packet_stats.get('total', 0)
        
        report = {
            'capture_status': 'active' if self.is_capturing else 'stopped',
            'total_packets': total_packets,
            'protocol_distribution': dict(self.protocol_stats),
            'top_ports': dict(sorted(self.traffic_by_port.items(), 
                                   key=lambda x: x[1], reverse=True)[:10]),
            'suspicious_activities': self.suspicious_activities[-50:],  # Last 50 activities
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return report
    
    def stop_capture(self):
        """Stop packet capture"""
        self.is_capturing = False
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=5)
        self.logger.info("Packet capture stopped")
    
    def reset_stats(self):
        """Reset all statistics"""
        self.packet_stats.clear()
        self.protocol_stats.clear()
        self.traffic_by_port.clear()
        self.suspicious_activities.clear()
        self.logger.info("Packet analysis statistics reset")
