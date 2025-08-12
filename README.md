# 🌐 Network Monitoring and Alert System

A comprehensive, real-time network monitoring solution built with Python that tracks bandwidth usage, system performance, device uptime, and provides intelligent anomaly detection with automated email alerts and a modern web dashboard.

## 📋 Table of Contents
- [🎯 What It Does](#-what-it-does)
- [⚡ Why This Project](#-why-this-project)
- [🏗️ How It Works](#️-how-it-works)
- [💻 Tech Stack](#-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [📊 Dashboard Features](#-dashboard-features)
- [⚙️ Configuration](#️-configuration)
- [🔧 Advanced Usage](#-advanced-usage)
- [📈 Monitoring Features](#-monitoring-features)
- [🚨 Alert System](#-alert-system)
- [📊 Data Management](#-data-management)
- [🛠️ Development](#️-development)
- [🤝 Contributing](#-contributing)

## 🎯 What It Does

This Network Monitoring and Alert System provides **enterprise-grade monitoring capabilities** for:

### 🌐 **Network Monitoring**
- **Real-time bandwidth tracking** (upload/download speeds in Mbps)
- **Traffic anomaly detection** (sudden spikes, unusual patterns)
- **Network interface monitoring** (all active interfaces)
- **Packet analysis** (counts, transmission rates)
- **Historical bandwidth trends** with configurable time ranges

### 💻 **System Performance Monitoring** 
- **CPU usage monitoring** with configurable thresholds
- **Memory (RAM) consumption tracking**
- **Disk space utilization monitoring**
- **Real-time system health indicators**
- **Performance trend analysis**

### 📱 **Device Uptime Monitoring**
- **Ping-based connectivity checks** for network devices
- **Response time measurement** (latency tracking)
- **Device availability statistics** (uptime percentages)
- **Multi-device monitoring** (routers, servers, endpoints)
- **Network topology health assessment**

### 🚨 **Intelligent Alert System**
- **SMTP email notifications** with HTML formatting
- **Severity-based alerting** (Low, Medium, High, Critical)
- **Alert cooldown periods** to prevent spam
- **Customizable thresholds** for all metrics
- **Multi-recipient support** for team notifications

### 📊 **Interactive Web Dashboard**
- **Real-time visualization** with auto-refresh capabilities
- **Interactive charts** using Plotly for responsive design
- **Historical data analysis** with configurable time ranges
- **Device status overview** with visual indicators
- **Alert management interface** with filtering and search

## ⚡ Why This Project

### **🏢 Business Use Cases**
- **IT Infrastructure Monitoring**: Monitor office networks, servers, and endpoints
- **Home Network Management**: Track internet usage, device connectivity
- **ISP Performance Monitoring**: Verify bandwidth allocation and service quality
- **Security Monitoring**: Detect unusual network traffic patterns
- **Capacity Planning**: Analyze historical usage for infrastructure decisions

### **🎓 Technical Learning**
This project demonstrates:
- **Multi-threaded Python applications** for concurrent monitoring
- **Real-time data visualization** with modern web frameworks
- **Network programming** using psutil and system calls
- **SMTP integration** for automated notifications
- **Data persistence** and time-series analysis
- **Cross-platform compatibility** (Windows, macOS, Linux)

### **🚀 Production Ready**
- **Scalable architecture** for enterprise deployment
- **Configurable monitoring intervals** and thresholds
- **Robust error handling** and recovery mechanisms
- **Comprehensive logging** for troubleshooting
- **Systemd service integration** for Linux deployment

## 🏗️ How It Works

### **System Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    NETWORK MONITORING SYSTEM                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │   Console   │  │ Web Dashboard│  │    Email Alerts    │   │
│  │  Interface  │  │ (Streamlit)  │  │   (SMTP/HTML)      │   │
│  └─────────────┘  └─────────────┘  └─────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │   Network   │  │   System    │  │     Device         │   │
│  │  Monitor    │  │  Monitor    │  │    Monitor         │   │
│  │  Thread     │  │   Thread    │  │     Thread         │   │
│  └─────────────┘  └─────────────┘  └─────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │    Data     │  │    Alert    │  │    Configuration   │   │
│  │   Logger    │  │   Manager   │  │      Manager       │   │
│  └─────────────┘  └─────────────┘  └─────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              JSON Data Storage Layer                    │ │
│  │  network_data.json | system_data.json | device_data.json│ │
│  │              alert_data.json                            │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### **Data Flow Process**

1. **Data Collection**: Three concurrent threads collect metrics every 30-120 seconds
2. **Processing**: Raw data is processed, analyzed for anomalies, and threshold violations
3. **Storage**: All data is stored in JSON files with automatic cleanup (10,000 records max)
4. **Alerting**: Threshold violations trigger email alerts with configurable cooldown periods
5. **Visualization**: Dashboard reads stored data and presents real-time visualizations
6. **Analysis**: Historical data enables trend analysis and capacity planning

### **Threading Model**

```python
Main Application Thread
├── Network Monitor Thread (30s interval)
│   ├── Bandwidth calculation (psutil.net_io_counters)
│   ├── Anomaly detection (statistical analysis)
│   └── Data logging & alerting
├── System Monitor Thread (60s interval)  
│   ├── CPU/Memory/Disk monitoring (psutil)
│   ├── Threshold checking
│   └── Performance logging
└── Device Monitor Thread (120s interval)
    ├── Ping operations (subprocess)
    ├── Latency measurement
    └── Connectivity logging
```

## 💻 Tech Stack

### **Core Technologies**
- **🐍 Python 3.7+**: Main programming language
- **🔧 psutil**: System and network monitoring
- **📊 Streamlit**: Web dashboard framework
- **📈 Plotly**: Interactive data visualization
- **🐼 Pandas**: Data manipulation and analysis
- **📧 smtplib**: Email notification system
- **🌐 scapy**: Advanced network packet analysis (optional)

### **System Integration**
- **🔄 Threading**: Concurrent monitoring operations
- **� JSON**: Data persistence and configuration
- **�🚀 systemd**: Linux service integration
- **🖥️ Cross-platform**: Windows, macOS, Linux support
- **📱 Responsive Design**: Mobile-friendly dashboard

### **Development Tools**
- **📝 Environment Variables**: Configuration management
- **🧪 Unit Testing**: Comprehensive test suite
- **📋 Logging**: Multi-level logging system
- **🔍 Error Handling**: Robust exception management
- **📖 Documentation**: Comprehensive README and code comments

## 🚀 Quick Start

### **Prerequisites**
- Python 3.7 or higher
- pip package manager
- Network access for device monitoring
- SMTP email account (Gmail recommended) for alerts

### **1. Installation**

```bash
# Clone or download the project
cd network

# Install dependencies
pip install -r requirements.txt

# Create configuration file
cp .env.example .env
```

### **2. Basic Configuration**

Edit `.env` file with your settings:

```env
# Required for email alerts
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ALERT_RECIPIENTS=admin@company.com,team@company.com

# Optional - customize thresholds
BANDWIDTH_THRESHOLD_MBPS=100
CPU_THRESHOLD_PERCENT=80
MEMORY_THRESHOLD_PERCENT=85
MONITORED_DEVICES=8.8.8.8,1.1.1.1,192.168.1.1
```

### **3. Run the System**

#### **🌟 Option 1: Full System with Dashboard (Recommended)**
```bash
python start_dashboard.py
# Access dashboard at: http://localhost:8501
```

#### **💻 Option 2: Console Only**
```bash
python main.py
```

#### **📊 Option 3: Dashboard Only**
```bash
streamlit run dashboard.py
```

#### **🎯 Option 4: Interactive Menu**
```bash
python quickstart.py
```

### **4. Verify Installation**

```bash
# Run system tests
python test_system.py

# Test connectivity
python utils.py test

# View current statistics
python utils.py stats
```

## 📊 Dashboard Features

### **Real-time Web Interface** (http://localhost:8501)

#### **📈 Current Status Panel**
- **Live System Metrics**: CPU, Memory, Disk usage with color-coded indicators
- **Network Speed Display**: Real-time upload/download bandwidth
- **Gauge Visualizations**: Circular progress indicators with threshold warnings
- **Status Indicators**: Green (good), Yellow (warning), Red (critical)

#### **🌐 Network Monitoring Dashboard**
- **Bandwidth Charts**: Dual-pane upload/download speed visualization
- **Time Series Analysis**: Historical bandwidth trends with configurable ranges
- **Traffic Anomaly Indicators**: Visual markers for detected unusual patterns
- **Interface Statistics**: Comprehensive network interface information

#### **💻 System Performance Graphs**
- **Resource Utilization**: Multi-line charts for CPU, Memory, Disk over time
- **Threshold Overlays**: Visual indication of configured alert thresholds
- **Historical Trending**: Performance analysis over hours, days, weeks
- **Capacity Planning**: Data-driven insights for infrastructure decisions

#### **📱 Device Monitoring Panel**
- **Uptime Visualization**: Bar charts showing device availability percentages
- **Response Time Tracking**: Latency measurements and trends
- **Connectivity Status**: Real-time reachability indicators
- **Network Topology Health**: Overall infrastructure status assessment

#### **🚨 Alert Management Dashboard**
- **Recent Alerts Timeline**: Chronological view of system alerts
- **Severity-based Filtering**: Organize alerts by criticality levels
- **Alert Statistics**: Counts and trends by type and severity
- **Resolution Tracking**: Alert lifecycle management

#### **⚙️ Dashboard Configuration**
- **Time Range Selector**: 1 hour to 3 days of historical data
- **Auto-refresh Control**: Configurable update intervals (30 seconds default)
- **Manual Refresh**: Force immediate data updates
- **Export Capabilities**: Download data in JSON format

## ⚙️ Configuration

### **Environment Variables (.env)**

#### **Email Configuration**
```env
# SMTP settings for email alerts
SMTP_SERVER=smtp.gmail.com          # SMTP server address
SMTP_PORT=587                       # SMTP port (587 for TLS)
EMAIL_USER=your_email@gmail.com     # Sender email address
EMAIL_PASSWORD=your_app_password    # Email password or app password
ALERT_RECIPIENTS=admin@company.com,team@company.com  # Comma-separated recipients
```

#### **Monitoring Thresholds**
```env
# Network monitoring
BANDWIDTH_THRESHOLD_MBPS=100        # Alert when bandwidth exceeds this value
PING_TIMEOUT_SECONDS=5              # Ping timeout for device monitoring

# System monitoring  
CPU_THRESHOLD_PERCENT=80            # CPU usage alert threshold
MEMORY_THRESHOLD_PERCENT=85         # Memory usage alert threshold
DISK_THRESHOLD_PERCENT=90           # Disk usage alert threshold
```

#### **Monitoring Intervals**
```env
# How often to check each metric (in seconds)
NETWORK_CHECK_INTERVAL=30           # Network bandwidth monitoring
SYSTEM_CHECK_INTERVAL=60            # System resource monitoring
DEVICE_PING_INTERVAL=120            # Device connectivity checks
```

#### **Device Monitoring**
```env
# Devices to monitor (comma-separated IP addresses)
MONITORED_DEVICES=8.8.8.8,1.1.1.1,192.168.1.1,10.0.0.1
```

#### **Alert Configuration**
```env
# Alert behavior
ALERT_COOLDOWN_MINUTES=15           # Minimum time between same alert types
LOG_LEVEL=INFO                      # Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_FILE=logs/network_monitor.log   # Log file location
```

### **Gmail Setup for Alerts**

1. **Enable 2-Factor Authentication** in your Google Account
2. **Generate App Password**: Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. **Use App Password**: Place the generated password in `EMAIL_PASSWORD`

Example:
```env
EMAIL_USER=monitoring@yourcompany.com
EMAIL_PASSWORD=abcd efgh ijkl mnop  # 16-character app password
```

### **File Structure**
```
network/
├── main.py                    # Main monitoring application
├── dashboard.py               # Streamlit web dashboard
├── start_dashboard.py         # Integrated launcher
├── quickstart.py              # Interactive setup menu
├── utils.py                   # Command-line utilities
├── test_system.py             # System test suite
├── setup.py                   # Installation script
├── requirements.txt           # Python dependencies
├── .env.example              # Configuration template
├── README.md                 # This documentation
├── src/                      # Source modules
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration management
│   ├── network_monitor.py     # Network monitoring core
│   ├── alert_manager.py       # Alert and notification system
│   ├── data_logger.py         # Data storage and retrieval
│   └── packet_analyzer.py     # Advanced packet analysis
├── logs/                     # Log files
│   └── network_monitor.log    # Application logs
└── data/                     # Monitoring data storage
    ├── network_data.json      # Network bandwidth data
    ├── system_data.json       # System performance data
    ├── device_data.json       # Device monitoring data
    └── alert_data.json        # Alert history
```

## 🔧 Advanced Usage

### **Command Line Utilities**

```bash
# Test device connectivity
python utils.py test

# Show current system statistics
python utils.py stats

# Display network interface information
python utils.py interfaces

# Analyze historical data (last 48 hours)
python utils.py analyze --hours 48

# Export monitoring data
python utils.py export --hours 72 --output monitoring_report.json
```

### **Service Installation (Linux)**

```bash
# Install as systemd service
sudo cp network-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable network-monitor.service
sudo systemctl start network-monitor.service

# Check service status
sudo systemctl status network-monitor.service

# View service logs
journalctl -u network-monitor.service -f
```

### **Custom Monitoring Scripts**

```python
from src.network_monitor import NetworkMonitor
from src.data_logger import DataLogger

# Create custom monitoring script
monitor = NetworkMonitor()
logger = DataLogger()

# Get current system stats
stats = monitor.get_system_stats()
print(f"CPU: {stats.cpu_percent}%")

# Get bandwidth usage
network_stats = monitor.get_network_stats()
upload, download = monitor.calculate_bandwidth_usage(network_stats)
print(f"Upload: {upload:.2f} Mbps, Download: {download:.2f} Mbps")
```

## � Monitoring Features

### **Network Monitoring Capabilities**

#### **Bandwidth Tracking**
- **Real-time Speed Calculation**: Accurate upload/download speeds in Mbps
- **Interface-specific Monitoring**: Track individual network interfaces
- **Historical Trending**: Long-term bandwidth usage patterns
- **Peak Usage Detection**: Identify high-traffic periods

#### **Anomaly Detection**
```python
# Automated detection of:
- Traffic spikes > 3x recent average
- Sustained high bandwidth usage
- Unusual traffic patterns
- Interface state changes
```

#### **Network Health Metrics**
- **Packet Loss Detection**: Monitor dropped packets
- **Interface Status**: Up/down state monitoring
- **Network Errors**: Transmission error tracking
- **MTU and Speed Detection**: Interface capability assessment

### **System Performance Monitoring**

#### **CPU Monitoring**
- **Multi-core Awareness**: Per-core and aggregate CPU usage
- **Load Average Tracking**: System load assessment
- **Process Impact Analysis**: High-CPU process identification

#### **Memory Monitoring** 
- **RAM Usage Tracking**: Available vs. used memory
- **Swap Usage Detection**: Virtual memory monitoring
- **Memory Pressure Alerts**: Early warning system

#### **Disk Monitoring**
- **Multi-filesystem Support**: Monitor all mounted filesystems  
- **Free Space Tracking**: Available storage monitoring
- **I/O Performance**: Read/write operation tracking

### **Device Monitoring Features**

#### **Connectivity Assessment**
- **ICMP Ping Monitoring**: Standard ping-based reachability
- **Response Time Measurement**: Latency tracking in milliseconds
- **Packet Loss Detection**: Connection quality assessment
- **Timeout Handling**: Configurable ping timeouts

#### **Network Topology Monitoring**
```python
# Monitor critical infrastructure:
- Gateway/Router connectivity
- DNS server availability  
- External internet connectivity
- Internal server reachability
```

## 🚨 Alert System

### **Alert Types and Triggers**

#### **Network Alerts**
- **High Bandwidth Usage**: Upload/download exceeds thresholds
- **Traffic Anomalies**: Unusual traffic spike detection
- **Interface Down**: Network interface failure detection
- **Connectivity Loss**: Internet connection issues

#### **System Alerts**
- **High CPU Usage**: Processor utilization warnings
- **Memory Exhaustion**: RAM usage approaching limits
- **Disk Space Warnings**: Storage capacity alerts
- **System Performance**: Overall health degradation

#### **Device Alerts**
- **Device Unreachable**: Ping failure notifications
- **High Latency**: Response time degradation
- **Intermittent Connectivity**: Unstable connection detection

### **Alert Severity Levels**

```python
SEVERITY_LEVELS = {
    'low': {
        'color': 'green',
        'threshold': 'Warning level reached',
        'action': 'Monitor situation'
    },
    'medium': {
        'color': 'yellow', 
        'threshold': 'Attention required',
        'action': 'Investigate issue'
    },
    'high': {
        'color': 'orange',
        'threshold': 'Immediate attention needed',
        'action': 'Take corrective action'
    },
    'critical': {
        'color': 'red',
        'threshold': 'System at risk',
        'action': 'Emergency response required'
    }
}
```

### **Email Notification Features**

#### **HTML Email Templates**
- **Professional Formatting**: Clean, readable email design
- **Color-coded Severity**: Visual severity identification
- **Detailed Information**: Comprehensive alert context
- **Timestamp Tracking**: Precise alert timing

#### **Anti-spam Protection**
- **Cooldown Periods**: Prevent alert flooding (15 minutes default)
- **Duplicate Suppression**: Avoid repeated identical alerts
- **Batch Processing**: Group related alerts efficiently

#### **Multi-recipient Support**
```env
# Support for multiple notification channels
ALERT_RECIPIENTS=admin@company.com,network@company.com,oncall@company.com
```

## 📊 Data Management

### **Data Storage Architecture**

#### **JSON-based Persistence**
```json
{
  "network_data.json": {
    "purpose": "Bandwidth and traffic monitoring",
    "fields": ["timestamp", "upload_mbps", "download_mbps", "packets", "anomalies"],
    "retention": "10,000 most recent records"
  },
  "system_data.json": {
    "purpose": "System performance metrics", 
    "fields": ["timestamp", "cpu_percent", "memory_percent", "disk_percent"],
    "retention": "10,000 most recent records"
  },
  "device_data.json": {
    "purpose": "Device connectivity monitoring",
    "fields": ["timestamp", "ip_address", "is_reachable", "response_time"],
    "retention": "10,000 most recent records"
  },
  "alert_data.json": {
    "purpose": "Alert history and tracking",
    "fields": ["timestamp", "alert_type", "message", "severity", "resolved"],
    "retention": "10,000 most recent records"
  }
}
```

#### **Automatic Data Management**
- **Rolling Storage**: Automatic cleanup of old records
- **Efficient Retrieval**: Time-based data filtering
- **Export Capabilities**: Data export in multiple formats
- **Backup Friendly**: Human-readable JSON format

### **Data Analysis Features**

#### **Historical Analysis**
```python
# Available analysis functions:
- Bandwidth trend analysis
- Peak usage identification  
- System performance trending
- Device availability statistics
- Alert frequency analysis
```

#### **Time-series Capabilities**
- **Configurable Time Ranges**: 1 hour to weeks of data
- **Trend Detection**: Identify long-term patterns
- **Comparative Analysis**: Period-over-period comparisons
- **Forecasting Data**: Predict future resource needs

### **Data Export and Integration**

```python
# Export options:
python utils.py export --hours 168 --output weekly_report.json
python utils.py analyze --hours 24  # Generate analysis report
```

## 🛠️ Development

### **Project Architecture**

#### **Modular Design**
```python
src/
├── config.py           # Environment and configuration management
├── network_monitor.py  # Core monitoring functionality  
├── alert_manager.py    # Alert generation and email delivery
├── data_logger.py      # Data persistence and retrieval
└── packet_analyzer.py  # Advanced network analysis (optional)
```

#### **Design Patterns**
- **Observer Pattern**: Event-driven alert system
- **Factory Pattern**: Configurable monitoring components
- **Strategy Pattern**: Pluggable analysis algorithms
- **Singleton Pattern**: Configuration management

### **Testing Framework**

```bash
# Run comprehensive test suite
python test_system.py

# Individual component testing
python -c "from src.network_monitor import NetworkMonitor; nm = NetworkMonitor(); print(nm.get_system_stats())"
```

### **Extending the System**

#### **Custom Monitors**
```python
# Add custom monitoring capability
class CustomMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def collect_metrics(self):
        # Your custom monitoring logic
        pass
        
    def process_alerts(self, metrics):
        # Your custom alerting logic  
        pass
```

#### **Plugin Architecture**
- **Monitoring Plugins**: Add new metric collection
- **Alert Plugins**: Custom notification channels
- **Analysis Plugins**: Advanced data processing
- **Visualization Plugins**: Custom dashboard components

### **Performance Optimization**

#### **Resource Efficiency**
- **Minimal CPU Impact**: Efficient monitoring algorithms
- **Memory Management**: Bounded data structures
- **I/O Optimization**: Batched file operations
- **Network Efficiency**: Minimal network overhead

#### **Scalability Considerations**
```python
# Configuration for large deployments:
MAX_RECORDS = 50000           # Increase data retention
MONITORING_INTERVAL = 60      # Reduce frequency for scale
BATCH_SIZE = 100             # Batch operations
WORKER_THREADS = 5           # Increase parallelism
```

## 🤝 Contributing

### **Development Setup**

```bash
# Fork and clone the repository
git clone <your-fork-url>
cd network-monitoring-system

# Create development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run tests
python test_system.py
```

### **Code Quality Standards**

- **PEP 8 Compliance**: Follow Python style guidelines
- **Type Hints**: Use type annotations for better code clarity
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Robust exception management
- **Testing**: Unit tests for new functionality

### **Contributing Guidelines**

1. **Fork the Repository**: Create your own copy
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Implement your improvements
4. **Add Tests**: Ensure new functionality is tested
5. **Update Documentation**: Keep README and code docs current
6. **Submit Pull Request**: Describe your changes clearly

### **Feature Requests and Bug Reports**

- **Feature Requests**: Describe the use case and expected behavior
- **Bug Reports**: Include system information, logs, and reproduction steps
- **Security Issues**: Report privately for security-related bugs

---

## 📞 Support and Resources

### **Getting Help**
- **Documentation**: This README covers most use cases
- **Test Suite**: Run `python test_system.py` for system validation
- **Logs**: Check `logs/network_monitor.log` for troubleshooting
- **Utilities**: Use `python utils.py --help` for available tools

### **Common Issues and Solutions**

#### **Permission Errors**
```bash
# Linux/macOS: Run with appropriate permissions
sudo python main.py  # For low-level network access
```

#### **Import Errors**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

#### **Email Authentication Failures**
- Verify SMTP settings in `.env`
- Use app passwords for Gmail
- Check firewall/network restrictions

### **System Requirements**
- **Python**: 3.7 or higher
- **Memory**: 50MB minimum, 200MB recommended
- **Disk**: 100MB for application, additional for data storage
- **Network**: Internet access for device monitoring and email alerts

---

**🌐 Network Monitoring and Alert System** - Professional network monitoring made simple!

*Built with ❤️ for reliable network infrastructure management*

## 📋 Project Structure

```
network/
├── main.py                    # Main application entry point
├── dashboard.py               # Streamlit web dashboard
├── start_dashboard.py         # Integrated launcher (monitoring + dashboard)
├── quickstart.py              # Quick start menu
├── setup.py                   # Setup and installation script
├── utils.py                   # Command-line utilities
├── test_system.py             # System test suite
├── requirements.txt           # Python dependencies
├── dashboard_requirements.txt # Additional dashboard dependencies
├── .env.example              # Configuration template
├── README.md                 # This file
├── src/
│   ├── config.py             # Configuration management
│   ├── network_monitor.py     # Core network monitoring
│   ├── alert_manager.py       # Alert and notification system
│   ├── data_logger.py         # Data logging and storage
│   └── packet_analyzer.py     # Advanced packet analysis (optional)
├── logs/                     # Log files directory
└── data/                     # Monitoring data storage
```

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager
- Network access for device monitoring
- SMTP email account for alerts (Gmail recommended)

### Quick Setup

1. **Clone and Setup**:
   ```bash
   cd network
   python setup.py
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Manual Installation

If the setup script doesn't work, follow these steps:

1. **Install Dependencies**:
   ```bash
   pip install psutil scapy requests python-dotenv matplotlib schedule
   ```

2. **Create Configuration**:
   ```bash
   cp .env.example .env
   ```

3. **Create Directories**:
   ```bash
   mkdir -p logs data
   ```

## 📊 **Dashboard Features**

### Real-time Web Interface
- **📈 Live Metrics**: CPU, Memory, Disk usage with gauge charts
- **🌐 Network Charts**: Real-time bandwidth usage graphs
- **📱 Device Status**: Device uptime and latency monitoring
- **🚨 Alert Dashboard**: Visual alert management with severity levels
- **📋 Historical Analysis**: Configurable time range data visualization
- **🔄 Auto-refresh**: Real-time updates every 30 seconds
- **📊 Interactive Charts**: Plotly-based responsive visualizations

### Dashboard Views
1. **Current Status**: Real-time system metrics
2. **Network Bandwidth**: Upload/download speed trends
3. **System Performance**: CPU, memory, disk over time
4. **Device Monitoring**: Uptime percentages and response times
5. **Alert Management**: Recent alerts with severity indicators
6. **Data Summary**: Statistics and data export options

Access at: **http://localhost:8501**

## ⚙️ Configuration

Edit the `.env` file with your settings:

### Email Configuration (Required)
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ALERT_RECIPIENTS=admin@company.com,network@company.com
```

### Monitoring Thresholds
```env
BANDWIDTH_THRESHOLD_MBPS=100
CPU_THRESHOLD_PERCENT=80
MEMORY_THRESHOLD_PERCENT=85
DISK_THRESHOLD_PERCENT=90
```

### Monitored Devices
```env
MONITORED_DEVICES=8.8.8.8,1.1.1.1,192.168.1.1
```

### For Gmail Users
1. Enable 2-factor authentication
2. Generate an app password: [Google Account Settings](https://myaccount.google.com/apppasswords)
3. Use the app password in `EMAIL_PASSWORD`

### Dashboard Configuration (Optional)
```env
DASHBOARD_PORT=8501
DASHBOARD_HOST=0.0.0.0
DASHBOARD_AUTO_REFRESH=true
```

## 🚀 Usage

### 🌟 **Quick Start (Recommended)**
```bash
# Interactive menu for all options
python quickstart.py
```

### 📊 **Full System with Dashboard**
```bash
# Start both monitoring system and web dashboard
python start_dashboard.py

# Access dashboard at: http://localhost:8501
```

### 💻 **Console Monitoring Only**
```bash
# Console-only monitoring
python main.py
```

### 🌐 **Dashboard Only**
```bash
# Just the web dashboard (requires existing data)
streamlit run dashboard.py
```

### Command Line Utilities
```bash
# Test connectivity
python utils.py test

# Show current system stats
python utils.py stats

# Show network interfaces
python utils.py interfaces

# Analyze historical data
python utils.py analyze --hours 24

# Export data
python utils.py export --hours 48 --output my_data.json
```

### As a Service (Linux)

1. **Install as systemd service**:
   ```bash
   sudo cp network-monitor.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable network-monitor.service
   sudo systemctl start network-monitor.service
   ```

2. **Check service status**:
   ```bash
   sudo systemctl status network-monitor.service
   ```

## 📊 Monitoring Features

### Network Monitoring
- **Bandwidth Usage**: Real-time upload/download speed tracking
- **Traffic Anomalies**: Detects sudden spikes or unusual patterns
- **Packet Analysis**: Monitors packet counts and transmission rates
- **Interface Monitoring**: Tracks all network interfaces

### System Monitoring
- **CPU Usage**: Percentage utilization with configurable thresholds
- **Memory Usage**: RAM consumption monitoring
- **Disk Usage**: Storage space monitoring
- **Performance Alerts**: Automated notifications for resource exhaustion

### Device Monitoring
- **Ping Monitoring**: Connectivity checks for critical devices
- **Latency Tracking**: Response time measurement
- **Uptime Monitoring**: Track device availability
- **Custom Device Lists**: Monitor any IP addresses

### Alert System
- **Email Notifications**: HTML formatted alerts with severity levels
- **Alert Cooldown**: Prevents spam with configurable intervals
- **Severity Levels**: Low, Medium, High, Critical classifications
- **Alert History**: Tracking and analysis of past alerts

## 📈 Data Storage

### Monitoring Data
- **Network Data**: `data/network_data.json`
- **System Data**: `data/system_data.json`
- **Device Data**: `data/device_data.json`
- **Alert Data**: `data/alert_data.json`

### Log Files
- **Application Logs**: `logs/network_monitor.log`
- **Configurable Levels**: DEBUG, INFO, WARNING, ERROR

### Data Export
- JSON format with timestamps
- Configurable time ranges
- Automatic data cleanup (keeps last 10,000 records)

## 🔧 Advanced Configuration

### Custom Monitoring Intervals
```env
NETWORK_CHECK_INTERVAL=30    # seconds
SYSTEM_CHECK_INTERVAL=60     # seconds
DEVICE_PING_INTERVAL=120     # seconds
```

### Alert Settings
```env
ALERT_COOLDOWN_MINUTES=15    # minimum time between same alert types
LOG_LEVEL=INFO               # DEBUG, INFO, WARNING, ERROR
```

### Performance Tuning
- Adjust check intervals based on your needs
- Reduce monitored devices for lower resource usage
- Increase thresholds to reduce false positives

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Permission Errors** (Linux/Mac):
   ```bash
   sudo python main.py  # For low-level network access
   ```

3. **Email Authentication**:
   - Verify SMTP settings
   - Check app password for Gmail
   - Test with `python utils.py test`

4. **Network Interface Access**:
   - Some features require admin privileges
   - Use `sudo` if necessary

### Debug Mode
```bash
# Set debug logging in .env
LOG_LEVEL=DEBUG
```

### Testing Components
```bash
# Test individual components
python -c "from src.network_monitor import NetworkMonitor; nm = NetworkMonitor(); print(nm.get_system_stats())"
```

## 📚 API Reference

### NetworkMonitor Class
- `get_network_stats()`: Current network I/O statistics
- `calculate_bandwidth_usage()`: Real-time bandwidth calculation
- `get_system_stats()`: CPU, memory, disk usage
- `ping_device()`: Device connectivity check
- `detect_anomalies()`: Traffic pattern analysis

### AlertManager Class
- `create_alert()`: Generate new alerts
- `send_email_alert()`: Send email notifications
- `process_system_alerts()`: System threshold checking
- `process_network_alerts()`: Network threshold checking

### DataLogger Class
- `log_network_data()`: Store network metrics
- `log_system_data()`: Store system metrics
- `export_data()`: Export historical data
- `get_*_history()`: Retrieve historical data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **psutil**: System and process utilities
- **scapy**: Network packet manipulation
- **python-dotenv**: Environment variable management
- **smtplib**: Email functionality

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs in `logs/network_monitor.log`
3. Test individual components with `utils.py`
4. Open an issue with detailed error information

---

**Network Monitoring and Alert System** - Keeping your network healthy! 🌐✨
