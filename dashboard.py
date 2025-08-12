import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import time
from datetime import datetime, timedelta
import os
import sys

# Add the src directory to Python path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_logger import DataLogger
from src.network_monitor import NetworkMonitor
from src.config import Config

# Page configuration
st.set_page_config(
    page_title="Network Monitoring Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-high {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    .alert-medium {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .alert-low {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .status-good {
        color: #4caf50;
        font-weight: bold;
    }
    .status-warning {
        color: #ff9800;
        font-weight: bold;
    }
    .status-critical {
        color: #f44336;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=30)  # Cache for 30 seconds
def load_data(hours=24):
    """Load monitoring data with caching"""
    try:
        data_logger = DataLogger()
        
        network_data = data_logger.get_network_history(hours)
        system_data = data_logger.get_system_history(hours)
        device_data = data_logger.get_device_history(hours=hours)
        alert_data = data_logger.get_alert_history(hours)
        
        return network_data, system_data, device_data, alert_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return [], [], [], []

@st.cache_data(ttl=10)  # Cache for 10 seconds
def get_current_stats():
    """Get current system statistics"""
    try:
        monitor = NetworkMonitor()
        stats = monitor.get_system_stats()
        network_stats = monitor.get_network_stats()
        upload_mbps, download_mbps = monitor.calculate_bandwidth_usage(network_stats)
        
        return {
            'cpu_percent': stats.cpu_percent,
            'memory_percent': stats.memory_percent,
            'disk_percent': stats.disk_percent,
            'upload_mbps': upload_mbps,
            'download_mbps': download_mbps,
            'timestamp': datetime.now()
        }
    except Exception as e:
        st.error(f"Error getting current stats: {e}")
        return None

def create_gauge_chart(value, title, max_value=100, color_threshold=None):
    """Create a gauge chart for metrics"""
    if color_threshold is None:
        color_threshold = [70, 85]
    
    # Determine color based on value
    if value <= color_threshold[0]:
        color = "green"
    elif value <= color_threshold[1]:
        color = "yellow"
    else:
        color = "red"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, color_threshold[0]], 'color': "lightgray"},
                {'range': [color_threshold[0], color_threshold[1]], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': color_threshold[1]
            }
        }
    ))
    
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def create_bandwidth_chart(network_data):
    """Create bandwidth usage chart"""
    if not network_data:
        return go.Figure()
    
    df = pd.DataFrame(network_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Upload Speed', 'Download Speed'),
        vertical_spacing=0.1
    )
    
    # Upload speed
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=df['upload_mbps'],
            mode='lines',
            name='Upload',
            line=dict(color='#1f77b4', width=2),
            fill='tonexty'
        ),
        row=1, col=1
    )
    
    # Download speed
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=df['download_mbps'],
            mode='lines',
            name='Download',
            line=dict(color='#ff7f0e', width=2),
            fill='tozeroy'
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        height=400,
        title_text="Network Bandwidth Usage",
        showlegend=False
    )
    
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Mbps", row=1, col=1)
    fig.update_yaxes(title_text="Mbps", row=2, col=1)
    
    return fig

def create_system_metrics_chart(system_data):
    """Create system metrics chart"""
    if not system_data:
        return go.Figure()
    
    df = pd.DataFrame(system_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['cpu_percent'],
        mode='lines',
        name='CPU %',
        line=dict(color='#1f77b4')
    ))
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['memory_percent'],
        mode='lines',
        name='Memory %',
        line=dict(color='#ff7f0e')
    ))
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['disk_percent'],
        mode='lines',
        name='Disk %',
        line=dict(color='#2ca02c')
    ))
    
    fig.update_layout(
        title="System Resource Usage",
        xaxis_title="Time",
        yaxis_title="Percentage",
        height=400,
        legend=dict(x=0, y=1)
    )
    
    return fig

def create_device_status_chart(device_data):
    """Create device status chart"""
    if not device_data:
        return go.Figure(), pd.DataFrame()
    
    df = pd.DataFrame(device_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Calculate uptime percentage for each device
    uptime_stats = []
    for device in df['ip_address'].unique():
        device_df = df[df['ip_address'] == device]
        total_checks = len(device_df)
        successful_checks = len(device_df[device_df['is_reachable'] == True])
        uptime_percent = (successful_checks / total_checks * 100) if total_checks > 0 else 0
        
        avg_response_time = device_df[device_df['response_time'].notna()]['response_time'].mean()
        
        uptime_stats.append({
            'device': device,
            'uptime_percent': uptime_percent,
            'avg_response_time': avg_response_time,
            'total_checks': total_checks,
            'status': 'Good' if uptime_percent >= 95 else 'Warning' if uptime_percent >= 90 else 'Critical'
        })
    
    uptime_df = pd.DataFrame(uptime_stats)
    
    if not uptime_df.empty:
        fig = px.bar(
            uptime_df,
            x='device',
            y='uptime_percent',
            color='status',
            color_discrete_map={'Good': 'green', 'Warning': 'orange', 'Critical': 'red'},
            title="Device Uptime Percentage",
            labels={'uptime_percent': 'Uptime %', 'device': 'Device IP'}
        )
        fig.update_layout(height=300)
    else:
        fig = go.Figure()
    
    return fig, uptime_df

def display_alerts(alert_data):
    """Display recent alerts"""
    if not alert_data:
        st.success("✅ No recent alerts")
        return
    
    # Sort alerts by timestamp (most recent first)
    alerts_df = pd.DataFrame(alert_data)
    alerts_df['timestamp'] = pd.to_datetime(alerts_df['timestamp'])
    alerts_df = alerts_df.sort_values('timestamp', ascending=False)
    
    st.subheader(f"🚨 Recent Alerts ({len(alerts_df)})")
    
    # Group alerts by severity
    severity_counts = alerts_df['severity'].value_counts()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Critical", severity_counts.get('critical', 0))
    with col2:
        st.metric("High", severity_counts.get('high', 0))
    with col3:
        st.metric("Medium", severity_counts.get('medium', 0))
    with col4:
        st.metric("Low", severity_counts.get('low', 0))
    
    # Display recent alerts
    for _, alert in alerts_df.head(10).iterrows():
        severity_class = f"alert-{alert['severity']}" if alert['severity'] in ['high', 'medium', 'low'] else "alert-high"
        
        with st.container():
            st.markdown(f"""
            <div class="metric-card {severity_class}">
                <strong>{alert['alert_type']}</strong> - {alert['severity'].upper()}<br>
                <small>{alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</small><br>
                {alert['message']}
            </div>
            """, unsafe_allow_html=True)
            st.write("")

def main():
    """Main dashboard function"""
    st.title("🌐 Network Monitoring Dashboard")
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Time range selector
    time_range = st.sidebar.selectbox(
        "Data Time Range",
        options=[1, 6, 12, 24, 48, 72],
        index=3,  # 24 hours default
        format_func=lambda x: f"{x} hours"
    )
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=True)
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Now"):
        st.cache_data.clear()
        st.rerun()
    
    # Current status section
    st.header("📊 Current Status")
    
    current_stats = get_current_stats()
    
    if current_stats:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            cpu_color = "🟢" if current_stats['cpu_percent'] < 70 else "🟡" if current_stats['cpu_percent'] < 85 else "🔴"
            st.metric(
                f"{cpu_color} CPU Usage",
                f"{current_stats['cpu_percent']:.1f}%"
            )
        
        with col2:
            mem_color = "🟢" if current_stats['memory_percent'] < 70 else "🟡" if current_stats['memory_percent'] < 85 else "🔴"
            st.metric(
                f"{mem_color} Memory Usage",
                f"{current_stats['memory_percent']:.1f}%"
            )
        
        with col3:
            disk_color = "🟢" if current_stats['disk_percent'] < 80 else "🟡" if current_stats['disk_percent'] < 90 else "🔴"
            st.metric(
                f"{disk_color} Disk Usage",
                f"{current_stats['disk_percent']:.1f}%"
            )
        
        with col4:
            st.metric(
                "🔼 Upload Speed",
                f"{current_stats['upload_mbps']:.2f} Mbps"
            )
        
        with col5:
            st.metric(
                "🔽 Download Speed",
                f"{current_stats['download_mbps']:.2f} Mbps"
            )
        
        # Gauge charts for system metrics
        st.subheader("📈 System Metrics")
        gauge_col1, gauge_col2, gauge_col3 = st.columns(3)
        
        with gauge_col1:
            cpu_gauge = create_gauge_chart(
                current_stats['cpu_percent'],
                "CPU Usage (%)",
                color_threshold=[70, 85]
            )
            st.plotly_chart(cpu_gauge, use_container_width=True)
        
        with gauge_col2:
            mem_gauge = create_gauge_chart(
                current_stats['memory_percent'],
                "Memory Usage (%)",
                color_threshold=[70, 85]
            )
            st.plotly_chart(mem_gauge, use_container_width=True)
        
        with gauge_col3:
            disk_gauge = create_gauge_chart(
                current_stats['disk_percent'],
                "Disk Usage (%)",
                color_threshold=[80, 90]
            )
            st.plotly_chart(disk_gauge, use_container_width=True)
    
    # Load historical data
    network_data, system_data, device_data, alert_data = load_data(time_range)
    
    # Network bandwidth charts
    st.header("🌐 Network Bandwidth")
    bandwidth_chart = create_bandwidth_chart(network_data)
    st.plotly_chart(bandwidth_chart, use_container_width=True)
    
    # System metrics over time
    st.header("💻 System Performance")
    system_chart = create_system_metrics_chart(system_data)
    st.plotly_chart(system_chart, use_container_width=True)
    
    # Device monitoring
    st.header("📱 Device Monitoring")
    device_chart, device_df = create_device_status_chart(device_data)
    
    if not device_df.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.plotly_chart(device_chart, use_container_width=True)
        
        with col2:
            st.subheader("Device Status")
            for _, device in device_df.iterrows():
                status_class = "status-good" if device['status'] == 'Good' else "status-warning" if device['status'] == 'Warning' else "status-critical"
                
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{device['device']}</strong><br>
                    <span class="{status_class}">{device['status']}</span><br>
                    Uptime: {device['uptime_percent']:.1f}%<br>
                    Avg Response: {device['avg_response_time']:.1f}ms
                </div>
                """, unsafe_allow_html=True)
                st.write("")
    else:
        st.info("No device monitoring data available")
    
    # Alerts section
    st.header("🚨 Alerts")
    display_alerts(alert_data)
    
    # Data summary
    with st.expander("📊 Data Summary"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Network Records", len(network_data))
        with col2:
            st.metric("System Records", len(system_data))
        with col3:
            st.metric("Device Records", len(device_data))
        with col4:
            st.metric("Alert Records", len(alert_data))
    
    # Footer with last update time
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Auto-refresh functionality
    if auto_refresh:
        time.sleep(30)
        st.rerun()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Dashboard error: {e}")
        st.info("Make sure the monitoring system is running and data files exist.")
