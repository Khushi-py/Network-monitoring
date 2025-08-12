#!/usr/bin/env python3
"""
Network Monitoring and Alert System
Main application file
"""

import time
import threading
import signal
import sys
import logging
from datetime import datetime
from typing import Dict, List

from src.config import Config
from src.network_monitor import NetworkMonitor
from src.alert_manager import AlertManager
from src.data_logger import DataLogger

class NetworkMonitoringSystem:
    """Main network monitoring system orchestrator"""
    
    def __init__(self, dashboard_mode=False):
        # Setup logging
        self.logger = Config.setup_logging()
        self.dashboard_mode = dashboard_mode
        self.logger.info("🚀 Initializing Network Monitoring System...")
        
        # Validate configuration (skip email validation in dashboard mode for demo)
        try:
            if not dashboard_mode:
                Config.validate_config()
                self.logger.info("✅ Configuration validated successfully")
            else:
                self.logger.info("🌐 Running in dashboard mode - skipping email validation")
        except ValueError as e:
            if not dashboard_mode:
                self.logger.error(f"❌ Configuration error: {e}")
                sys.exit(1)
            else:
                self.logger.warning(f"⚠️ Configuration warning: {e} (continuing in dashboard mode)")
        
        # Initialize components
        self.network_monitor = NetworkMonitor()
        
        # Initialize AlertManager with error handling for missing email config
        try:
            self.alert_manager = AlertManager(
                smtp_server=Config.SMTP_SERVER,
                smtp_port=Config.SMTP_PORT,
                email_user=Config.EMAIL_USER or "demo@example.com",
                email_password=Config.EMAIL_PASSWORD or "demo_password",
                recipients=Config.ALERT_RECIPIENTS if Config.ALERT_RECIPIENTS != [''] else ["demo@example.com"],
                cooldown_minutes=Config.ALERT_COOLDOWN_MINUTES
            )
        except Exception as e:
            self.logger.warning(f"⚠️ Alert manager initialization warning: {e}")
            self.alert_manager = None
        
        self.data_logger = DataLogger()
        
        # Control flags
        self.running = False
        self.threads = []
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("✅ Network Monitoring System initialized successfully")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"📡 Received signal {signum}, shutting down gracefully...")
        self.stop()
    
    def start(self):
        """Start the monitoring system"""
        if self.running:
            self.logger.warning("⚠️ System is already running")
            return
        
        self.running = True
        self.logger.info("🔄 Starting Network Monitoring System...")
        
        # Start monitoring threads
        self._start_network_monitoring()
        self._start_system_monitoring()
        self._start_device_monitoring()
        
        self.logger.info("✅ All monitoring threads started")
        
        # Main loop
        try:
            while self.running:
                self._print_status()
                time.sleep(60)  # Status update every minute
        except KeyboardInterrupt:
            self.logger.info("👋 Received keyboard interrupt")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the monitoring system"""
        if not self.running:
            return
        
        self.logger.info("🛑 Stopping Network Monitoring System...")
        self.running = False
        
        # Wait for threads to finish
        for thread in self.threads:
            if thread.is_alive():
                self.logger.info(f"⏳ Waiting for {thread.name} to finish...")
                thread.join(timeout=5)
        
        self.logger.info("✅ Network Monitoring System stopped")
    
    def _start_network_monitoring(self):
        """Start network monitoring thread"""
        def monitor_network():
            self.logger.info("🌐 Starting network monitoring thread")
            
            while self.running:
                try:
                    # Get network statistics
                    network_stats = self.network_monitor.get_network_stats()
                    upload_mbps, download_mbps = self.network_monitor.calculate_bandwidth_usage(network_stats)
                    
                    # Detect anomalies
                    anomalies = self.network_monitor.detect_anomalies(
                        upload_mbps, download_mbps, Config.BANDWIDTH_THRESHOLD_MBPS
                    )
                    
                    # Log data
                    self.data_logger.log_network_data(
                        upload_mbps, download_mbps, network_stats, anomalies
                    )
                    
                    # Process alerts
                    alerts = []
                    if self.alert_manager:
                        alerts = self.alert_manager.process_network_alerts(
                            upload_mbps, download_mbps, anomalies, Config.BANDWIDTH_THRESHOLD_MBPS
                        )
                        
                        if alerts:
                            self.data_logger.log_alert_data(alerts)
                            result = self.alert_manager.send_all_alerts(alerts)
                            if result['failed'] > 0:
                                self.logger.warning(f"⚠️ Failed to send {result['failed']} alerts")
                    
                    # Log anomalies even without alert manager
                    if anomalies:
                        for anomaly in anomalies:
                            self.logger.warning(f"🚨 Network anomaly: {anomaly}")
                    
                    # Log current status
                    if upload_mbps > 1 or download_mbps > 1:  # Only log significant traffic
                        self.logger.info(
                            f"📊 Network: ↑{upload_mbps:.2f} Mbps ↓{download_mbps:.2f} Mbps"
                        )
                    
                    time.sleep(Config.NETWORK_CHECK_INTERVAL)
                    
                except Exception as e:
                    self.logger.error(f"❌ Error in network monitoring: {e}")
                    time.sleep(10)  # Short delay before retry
        
        thread = threading.Thread(target=monitor_network, name="NetworkMonitor", daemon=True)
        thread.start()
        self.threads.append(thread)
    
    def _start_system_monitoring(self):
        """Start system monitoring thread"""
        def monitor_system():
            self.logger.info("💻 Starting system monitoring thread")
            
            while self.running:
                try:
                    # Get system statistics
                    system_stats = self.network_monitor.get_system_stats()
                    
                    # Log data
                    self.data_logger.log_system_data(system_stats)
                    
                    # Process alerts
                    alerts = []
                    if self.alert_manager:
                        thresholds = {
                            'cpu': Config.CPU_THRESHOLD_PERCENT,
                            'memory': Config.MEMORY_THRESHOLD_PERCENT,
                            'disk': Config.DISK_THRESHOLD_PERCENT
                        }
                        
                        alerts = self.alert_manager.process_system_alerts(system_stats, thresholds)
                        
                        if alerts:
                            self.data_logger.log_alert_data(alerts)
                            result = self.alert_manager.send_all_alerts(alerts)
                            if result['failed'] > 0:
                                self.logger.warning(f"⚠️ Failed to send {result['failed']} alerts")
                    
                    # Log threshold violations even without alert manager
                    if system_stats.cpu_percent > Config.CPU_THRESHOLD_PERCENT:
                        self.logger.warning(f"🚨 High CPU usage: {system_stats.cpu_percent:.1f}%")
                    if system_stats.memory_percent > Config.MEMORY_THRESHOLD_PERCENT:
                        self.logger.warning(f"🚨 High memory usage: {system_stats.memory_percent:.1f}%")
                    if system_stats.disk_percent > Config.DISK_THRESHOLD_PERCENT:
                        self.logger.warning(f"🚨 High disk usage: {system_stats.disk_percent:.1f}%")
                    
                    # Log current status
                    self.logger.info(
                        f"🖥️ System: CPU {system_stats.cpu_percent:.1f}% "
                        f"RAM {system_stats.memory_percent:.1f}% "
                        f"Disk {system_stats.disk_percent:.1f}%"
                    )
                    
                    time.sleep(Config.SYSTEM_CHECK_INTERVAL)
                    
                except Exception as e:
                    self.logger.error(f"❌ Error in system monitoring: {e}")
                    time.sleep(10)  # Short delay before retry
        
        thread = threading.Thread(target=monitor_system, name="SystemMonitor", daemon=True)
        thread.start()
        self.threads.append(thread)
    
    def _start_device_monitoring(self):
        """Start device monitoring thread"""
        def monitor_devices():
            self.logger.info("📱 Starting device monitoring thread")
            
            while self.running:
                try:
                    device_statuses = []
                    
                    # Ping all monitored devices
                    for device_ip in Config.MONITORED_DEVICES:
                        if device_ip.strip():  # Skip empty entries
                            status = self.network_monitor.ping_device(
                                device_ip.strip(), Config.PING_TIMEOUT_SECONDS
                            )
                            device_statuses.append(status)
                    
                    # Log data
                    self.data_logger.log_device_data(device_statuses)
                    
                    # Process alerts
                    alerts = []
                    if self.alert_manager:
                        alerts = self.alert_manager.process_device_alerts(device_statuses)
                        
                        if alerts:
                            self.data_logger.log_alert_data(alerts)
                            result = self.alert_manager.send_all_alerts(alerts)
                            if result['failed'] > 0:
                                self.logger.warning(f"⚠️ Failed to send {result['failed']} alerts")
                    
                    # Log device status
                    reachable_count = sum(1 for status in device_statuses if status.is_reachable)
                    total_count = len(device_statuses)
                    
                    self.logger.info(
                        f"📡 Devices: {reachable_count}/{total_count} reachable"
                    )
                    
                    # Log individual device issues
                    for status in device_statuses:
                        if not status.is_reachable:
                            self.logger.warning(f"❌ Device {status.ip_address} unreachable")
                        elif status.response_time and status.response_time > 500:
                            self.logger.warning(
                                f"⚠️ Device {status.ip_address} high latency: {status.response_time:.1f}ms"
                            )
                    
                    time.sleep(Config.DEVICE_PING_INTERVAL)
                    
                except Exception as e:
                    self.logger.error(f"❌ Error in device monitoring: {e}")
                    time.sleep(10)  # Short delay before retry
        
        thread = threading.Thread(target=monitor_devices, name="DeviceMonitor", daemon=True)
        thread.start()
        self.threads.append(thread)
    
    def _print_status(self):
        """Print system status summary"""
        try:
            # Get alert summary
            if self.alert_manager:
                alert_summary = self.alert_manager.get_alert_summary()
            else:
                alert_summary = {'total_alerts': 0, 'by_severity': {}}
            
            # Get recent data
            recent_network = self.data_logger.get_network_history(hours=1)
            recent_system = self.data_logger.get_system_history(hours=1)
            
            print("\n" + "="*60)
            print(f"📊 NETWORK MONITORING SYSTEM STATUS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60)
            
            # Alert summary
            if alert_summary['total_alerts'] > 0:
                print(f"🚨 Active Alerts: {alert_summary['total_alerts']}")
                for severity, count in alert_summary['by_severity'].items():
                    print(f"   {severity.upper()}: {count}")
            else:
                print("✅ No active alerts")
            
            # Network summary
            if recent_network:
                avg_upload = sum(r['upload_mbps'] for r in recent_network[-10:]) / min(len(recent_network), 10)
                avg_download = sum(r['download_mbps'] for r in recent_network[-10:]) / min(len(recent_network), 10)
                print(f"🌐 Network (avg last 10 readings): ↑{avg_upload:.2f} Mbps ↓{avg_download:.2f} Mbps")
            
            # System summary
            if recent_system:
                latest_system = recent_system[-1]
                print(f"💻 System: CPU {latest_system['cpu_percent']:.1f}% "
                      f"RAM {latest_system['memory_percent']:.1f}% "
                      f"Disk {latest_system['disk_percent']:.1f}%")
            
            # Dashboard info
            if self.dashboard_mode:
                print("🌐 Dashboard: http://localhost:8501")
            
            print("="*60)
            
        except Exception as e:
            self.logger.error(f"❌ Error printing status: {e}")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Network Monitoring System')
    parser.add_argument('--dashboard', action='store_true', 
                       help='Run in dashboard mode (less strict validation)')
    args = parser.parse_args()
    
    print("🚀 Network Monitoring and Alert System")
    print("=====================================")
    
    try:
        # Create and start the monitoring system
        monitor_system = NetworkMonitoringSystem(dashboard_mode=args.dashboard)
        monitor_system.start()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
