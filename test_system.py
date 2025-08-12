#!/usr/bin/env python3
"""
Quick test script for Network Monitoring System
"""

import sys
import os
from datetime import datetime

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from src.config import Config
        from src.network_monitor import NetworkMonitor
        from src.alert_manager import AlertManager
        from src.data_logger import DataLogger
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("🧪 Testing configuration...")
    
    try:
        from src.config import Config
        
        # Test basic config loading
        print(f"   SMTP Server: {Config.SMTP_SERVER}")
        print(f"   Network Check Interval: {Config.NETWORK_CHECK_INTERVAL}s")
        print(f"   Monitored Devices: {len(Config.MONITORED_DEVICES)}")
        
        # Setup logging
        logger = Config.setup_logging()
        logger.info("Test log message")
        
        print("✅ Configuration test passed")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_network_monitoring():
    """Test basic network monitoring functionality"""
    print("🧪 Testing network monitoring...")
    
    try:
        from src.network_monitor import NetworkMonitor
        
        monitor = NetworkMonitor()
        
        # Test network stats
        stats = monitor.get_network_stats()
        print(f"   Network stats collected: {stats.bytes_sent:,} bytes sent")
        
        # Test system stats
        sys_stats = monitor.get_system_stats()
        print(f"   System stats: CPU {sys_stats.cpu_percent:.1f}%, "
              f"Memory {sys_stats.memory_percent:.1f}%")
        
        # Test ping (use localhost)
        ping_result = monitor.ping_device("127.0.0.1", 2)
        print(f"   Localhost ping: {'✅' if ping_result.is_reachable else '❌'}")
        
        print("✅ Network monitoring test passed")
        return True
    except Exception as e:
        print(f"❌ Network monitoring test failed: {e}")
        return False

def test_data_logging():
    """Test data logging functionality"""
    print("🧪 Testing data logging...")
    
    try:
        from src.data_logger import DataLogger
        from src.network_monitor import NetworkMonitor
        
        data_logger = DataLogger()
        monitor = NetworkMonitor()
        
        # Test network data logging
        network_stats = monitor.get_network_stats()
        upload_mbps, download_mbps = monitor.calculate_bandwidth_usage(network_stats)
        
        success = data_logger.log_network_data(upload_mbps, download_mbps, network_stats)
        print(f"   Network data logging: {'✅' if success else '❌'}")
        
        # Test system data logging
        system_stats = monitor.get_system_stats()
        success = data_logger.log_system_data(system_stats)
        print(f"   System data logging: {'✅' if success else '❌'}")
        
        print("✅ Data logging test passed")
        return True
    except Exception as e:
        print(f"❌ Data logging test failed: {e}")
        return False

def test_alert_manager():
    """Test alert manager (without sending emails)"""
    print("🧪 Testing alert manager...")
    
    try:
        from src.alert_manager import AlertManager
        
        # Create alert manager with dummy config
        alert_manager = AlertManager(
            smtp_server="smtp.example.com",
            smtp_port=587,
            email_user="test@example.com",
            email_password="dummy",
            recipients=["admin@example.com"],
            cooldown_minutes=1
        )
        
        # Test alert creation
        alert = alert_manager.create_alert(
            "Test Alert",
            "This is a test alert message",
            "low"
        )
        
        print(f"   Alert created: {alert.alert_type}")
        print(f"   Alert severity: {alert.severity}")
        
        # Test alert summary
        summary = alert_manager.get_alert_summary()
        print(f"   Alert summary: {summary['total_alerts']} total alerts")
        
        print("✅ Alert manager test passed")
        return True
    except Exception as e:
        print(f"❌ Alert manager test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Network Monitoring System - Quick Test Suite")
    print("=" * 60)
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("Network Monitoring", test_network_monitoring),
        ("Data Logging", test_data_logging),
        ("Alert Manager", test_alert_manager),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 40)
        
        if test_func():
            passed += 1
        else:
            print(f"⚠️ Test '{test_name}' failed")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\n📝 Next steps:")
        print("1. Configure your .env file")
        print("2. Run 'python main.py' to start monitoring")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
