# 🌐 Network Monitoring and Alert System

A comprehensive, real-time network monitoring solution built with Python that tracks bandwidth usage, system performance, device uptime, and provides intelligent anomaly detection with automated email alerts and a modern web dashboard.

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

  ### **Data Flow Process**

1. **Data Collection**: Three concurrent threads collect metrics every 30-120 seconds
2. **Processing**: Raw data is processed, analyzed for anomalies, and threshold violations
3. **Storage**: All data is stored in JSON files with automatic cleanup (10,000 records max)
4. **Alerting**: Threshold violations trigger email alerts with configurable cooldown periods
5. **Visualization**: Dashboard reads stored data and presents real-time visualizations
6. **Analysis**: Historical data enables trend analysis and capacity planning


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
  
---

**Network Monitoring and Alert System** 🌐✨
