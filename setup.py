#!/usr/bin/env python3
"""
Setup script for Network Monitoring and Alert System
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_config_file():
    """Create .env file from template"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        response = input("⚠️ .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("📝 Keeping existing .env file")
            return True
    
    if env_example.exists():
        shutil.copy2(env_example, env_file)
        print("✅ Created .env file from template")
        print("📝 Please edit .env file with your configuration:")
        print("   - Email settings for alerts")
        print("   - Monitoring thresholds")
        print("   - Device IPs to monitor")
        return True
    else:
        print("❌ .env.example template not found")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["logs", "data"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def check_system_requirements():
    """Check system-specific requirements"""
    print("🔍 Checking system requirements...")
    
    # Check if ping is available
    ping_cmd = "ping" if os.name == 'nt' else "ping"
    if not shutil.which(ping_cmd):
        print("⚠️ Warning: ping command not found. Device monitoring may not work.")
    else:
        print("✅ Ping command available")
    
    return True

def create_systemd_service():
    """Create systemd service file (Linux only)"""
    if os.name != 'posix' or not Path('/etc/systemd/system').exists():
        print("ℹ️ Systemd not available, skipping service creation")
        return True
    
    current_dir = Path.cwd().absolute()
    python_path = sys.executable
    
    service_content = f"""[Unit]
Description=Network Monitoring and Alert System
After=network.target
Wants=network.target

[Service]
Type=simple
User={os.getenv('USER', 'root')}
WorkingDirectory={current_dir}
ExecStart={python_path} main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    service_file = Path("network-monitor.service")
    with open(service_file, 'w') as f:
        f.write(service_content)
    
    print(f"✅ Created systemd service file: {service_file}")
    print("📝 To install the service:")
    print(f"   sudo cp {service_file} /etc/systemd/system/")
    print("   sudo systemctl daemon-reload")
    print("   sudo systemctl enable network-monitor.service")
    print("   sudo systemctl start network-monitor.service")
    
    return True

def run_initial_test():
    """Run initial test to verify setup"""
    print("🧪 Running initial tests...")
    
    try:
        # Test imports
        from src.config import Config
        from src.network_monitor import NetworkMonitor
        from src.alert_manager import AlertManager
        from src.data_logger import DataLogger
        
        print("✅ All modules imported successfully")
        
        # Test basic functionality
        Config.setup_logging()
        monitor = NetworkMonitor()
        
        # Test network stats
        stats = monitor.get_network_stats()
        print(f"✅ Network monitoring test passed")
        
        # Test system stats
        sys_stats = monitor.get_system_stats()
        print(f"✅ System monitoring test passed")
        
        print("✅ All tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup process"""
    print("🚀 Network Monitoring and Alert System Setup")
    print("=" * 50)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Installing dependencies", install_dependencies),
        ("Creating configuration file", create_config_file),
        ("Creating directories", create_directories),
        ("Checking system requirements", check_system_requirements),
        ("Creating systemd service", create_systemd_service),
        ("Running initial tests", run_initial_test),
    ]
    
    for step_name, step_function in steps:
        print(f"\n🔧 {step_name}...")
        if not step_function():
            print(f"❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Edit .env file with your configuration")
    print("2. Run 'python utils.py test' to test connectivity")
    print("3. Run 'python main.py' to start monitoring")
    print("\n💡 Tips:")
    print("- Use 'python utils.py --help' for utility commands")
    print("- Check logs/ directory for monitoring logs")
    print("- Data is stored in data/ directory")
    print("=" * 50)

if __name__ == "__main__":
    main()
