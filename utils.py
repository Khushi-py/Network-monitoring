#!/usr/bin/env python3
"""
Network Monitoring Utilities
Additional tools for network analysis
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from src.config import Config
from src.data_logger import DataLogger
from src.network_monitor import NetworkMonitor

def export_data(hours=24, output_file=None):
    """Export monitoring data to file"""
    data_logger = DataLogger()
    
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"network_data_export_{timestamp}.json"
    
    success = data_logger.export_data(output_file, 'all', hours)
    
    if success:
        print(f"✅ Data exported successfully to {output_file}")
    else:
        print("❌ Failed to export data")
        return False
    
    return True

def test_connectivity():
    """Test connectivity to monitored devices"""
    Config.setup_logging()
    monitor = NetworkMonitor()
    
    print("🔍 Testing connectivity to monitored devices...")
    print("=" * 50)
    
    for device_ip in Config.MONITORED_DEVICES:
        if device_ip.strip():
            status = monitor.ping_device(device_ip.strip(), Config.PING_TIMEOUT_SECONDS)
            
            status_icon = "✅" if status.is_reachable else "❌"
            response_time = f"{status.response_time:.1f}ms" if status.response_time else "N/A"
            
            print(f"{status_icon} {status.ip_address}: {response_time}")
    
    print("=" * 50)

def show_network_interfaces():
    """Display network interface information"""
    Config.setup_logging()
    monitor = NetworkMonitor()
    
    print("🌐 Network Interface Information")
    print("=" * 50)
    
    interfaces = monitor.get_network_interfaces()
    
    for interface_name, info in interfaces.items():
        print(f"\n📡 Interface: {interface_name}")
        print(f"   Status: {'UP' if info['is_up'] else 'DOWN'}")
        
        if info['speed']:
            print(f"   Speed: {info['speed']} Mbps")
        
        if info['mtu']:
            print(f"   MTU: {info['mtu']}")
        
        print("   Addresses:")
        for addr in info['addresses']:
            if addr['address']:
                print(f"     {addr['family']}: {addr['address']}")
                if addr['netmask']:
                    print(f"       Netmask: {addr['netmask']}")

def show_system_stats():
    """Display current system statistics"""
    Config.setup_logging()
    monitor = NetworkMonitor()
    
    print("💻 Current System Statistics")
    print("=" * 50)
    
    try:
        stats = monitor.get_system_stats()
        network_stats = monitor.get_network_stats()
        upload_mbps, download_mbps = monitor.calculate_bandwidth_usage(network_stats)
        
        print(f"🖥️  CPU Usage: {stats.cpu_percent:.1f}%")
        print(f"💾 Memory Usage: {stats.memory_percent:.1f}%")
        print(f"💿 Disk Usage: {stats.disk_percent:.1f}%")
        print(f"🌐 Upload: {upload_mbps:.2f} Mbps")
        print(f"🌐 Download: {download_mbps:.2f} Mbps")
        print(f"📦 Packets Sent: {network_stats.packets_sent:,}")
        print(f"📦 Packets Received: {network_stats.packets_recv:,}")
        print(f"📊 Bytes Sent: {network_stats.bytes_sent:,}")
        print(f"📊 Bytes Received: {network_stats.bytes_recv:,}")
        
    except Exception as e:
        print(f"❌ Error getting system stats: {e}")

def analyze_data(hours=24):
    """Analyze historical monitoring data"""
    data_logger = DataLogger()
    
    print(f"📈 Data Analysis - Last {hours} Hours")
    print("=" * 50)
    
    # Network data analysis
    network_data = data_logger.get_network_history(hours)
    if network_data:
        upload_speeds = [d['upload_mbps'] for d in network_data]
        download_speeds = [d['download_mbps'] for d in network_data]
        
        print(f"🌐 Network Statistics ({len(network_data)} data points):")
        print(f"   Upload - Avg: {sum(upload_speeds)/len(upload_speeds):.2f} Mbps, "
              f"Max: {max(upload_speeds):.2f} Mbps")
        print(f"   Download - Avg: {sum(download_speeds)/len(download_speeds):.2f} Mbps, "
              f"Max: {max(download_speeds):.2f} Mbps")
        
        # Count anomalies
        anomaly_count = sum(1 for d in network_data if d.get('anomalies'))
        print(f"   Anomalies detected: {anomaly_count}")
    
    # System data analysis
    system_data = data_logger.get_system_history(hours)
    if system_data:
        cpu_usage = [d['cpu_percent'] for d in system_data]
        memory_usage = [d['memory_percent'] for d in system_data]
        
        print(f"\n💻 System Statistics ({len(system_data)} data points):")
        print(f"   CPU - Avg: {sum(cpu_usage)/len(cpu_usage):.1f}%, "
              f"Max: {max(cpu_usage):.1f}%")
        print(f"   Memory - Avg: {sum(memory_usage)/len(memory_usage):.1f}%, "
              f"Max: {max(memory_usage):.1f}%")
    
    # Alert analysis
    alert_data = data_logger.get_alert_history(hours)
    if alert_data:
        alert_types = {}
        severity_counts = {}
        
        for alert in alert_data:
            alert_type = alert.get('alert_type', 'Unknown')
            severity = alert.get('severity', 'unknown')
            
            alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        print(f"\n🚨 Alert Statistics ({len(alert_data)} alerts):")
        print(f"   By Type:")
        for alert_type, count in sorted(alert_types.items()):
            print(f"     {alert_type}: {count}")
        
        print(f"   By Severity:")
        for severity, count in sorted(severity_counts.items()):
            print(f"     {severity.upper()}: {count}")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Network Monitoring Utilities')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export monitoring data')
    export_parser.add_argument('--hours', type=int, default=24, 
                              help='Hours of data to export (default: 24)')
    export_parser.add_argument('--output', type=str, 
                              help='Output filename (default: auto-generated)')
    
    # Test command
    subparsers.add_parser('test', help='Test connectivity to monitored devices')
    
    # Interfaces command
    subparsers.add_parser('interfaces', help='Show network interface information')
    
    # Stats command
    subparsers.add_parser('stats', help='Show current system statistics')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze historical data')
    analyze_parser.add_argument('--hours', type=int, default=24,
                               help='Hours of data to analyze (default: 24)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'export':
            export_data(args.hours, args.output)
        elif args.command == 'test':
            test_connectivity()
        elif args.command == 'interfaces':
            show_network_interfaces()
        elif args.command == 'stats':
            show_system_stats()
        elif args.command == 'analyze':
            analyze_data(args.hours)
        
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
