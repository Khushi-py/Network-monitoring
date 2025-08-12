import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Alert:
    """Data class for alerts"""
    alert_type: str
    message: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    timestamp: datetime
    resolved: bool = False

class AlertManager:
    """Manages alerts and notifications"""
    
    def __init__(self, smtp_server: str, smtp_port: int, email_user: str, 
                 email_password: str, recipients: List[str], cooldown_minutes: int = 15):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_user = email_user
        self.email_password = email_password
        self.recipients = [r.strip() for r in recipients if r.strip()]
        self.cooldown_minutes = cooldown_minutes
        self.logger = logging.getLogger(__name__)
        
        # Track last alert times to implement cooldown
        self.last_alert_times = {}
        self.active_alerts = []
        
    def should_send_alert(self, alert_type: str) -> bool:
        """Check if enough time has passed since last alert of this type"""
        last_alert_time = self.last_alert_times.get(alert_type)
        
        if last_alert_time is None:
            return True
        
        time_since_last = datetime.now() - last_alert_time
        return time_since_last.total_seconds() >= (self.cooldown_minutes * 60)
    
    def create_alert(self, alert_type: str, message: str, severity: str = 'medium') -> Alert:
        """Create a new alert"""
        alert = Alert(
            alert_type=alert_type,
            message=message,
            severity=severity,
            timestamp=datetime.now()
        )
        
        self.active_alerts.append(alert)
        self.logger.info(f"Alert created: [{severity.upper()}] {alert_type}: {message}")
        
        return alert
    
    def send_email_alert(self, alert: Alert) -> bool:
        """Send email notification for an alert"""
        if not self.recipients:
            self.logger.warning("No email recipients configured")
            return False
        
        if not self.should_send_alert(alert.alert_type):
            self.logger.info(f"Alert {alert.alert_type} is in cooldown period, skipping email")
            return False
        
        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = ', '.join(self.recipients)
            msg['Subject'] = f"[{alert.severity.upper()}] Network Alert: {alert.alert_type}"
            
            # Create email body
            body = self._create_email_body(alert)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            # Update last alert time
            self.last_alert_times[alert.alert_type] = datetime.now()
            self.logger.info(f"Email alert sent successfully for {alert.alert_type}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")
            return False
    
    def _create_email_body(self, alert: Alert) -> str:
        """Create HTML email body for alert"""
        severity_colors = {
            'low': '#28a745',      # Green
            'medium': '#ffc107',   # Yellow
            'high': '#fd7e14',     # Orange
            'critical': '#dc3545'  # Red
        }
        
        color = severity_colors.get(alert.severity, '#6c757d')
        
        return f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: {color}; color: white; padding: 20px; text-align: center;">
                    <h1 style="margin: 0;">Network Monitoring Alert</h1>
                </div>
                
                <div style="padding: 20px; background-color: #f8f9fa;">
                    <h2 style="color: {color}; margin-top: 0;">{alert.alert_type}</h2>
                    
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #dee2e6; font-weight: bold;">Severity:</td>
                            <td style="padding: 8px; border-bottom: 1px solid #dee2e6; color: {color}; font-weight: bold;">{alert.severity.upper()}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #dee2e6; font-weight: bold;">Timestamp:</td>
                            <td style="padding: 8px; border-bottom: 1px solid #dee2e6;">{alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #dee2e6; font-weight: bold;">Message:</td>
                            <td style="padding: 8px; border-bottom: 1px solid #dee2e6;">{alert.message}</td>
                        </tr>
                    </table>
                </div>
                
                <div style="padding: 20px; background-color: #e9ecef; text-align: center; font-size: 12px; color: #6c757d;">
                    This alert was generated by the Network Monitoring System.<br>
                    Please investigate and take appropriate action if necessary.
                </div>
            </div>
        </body>
        </html>
        """
    
    def process_system_alerts(self, system_stats, thresholds: Dict[str, float]) -> List[Alert]:
        """Process system statistics and create alerts if thresholds are exceeded"""
        alerts = []
        
        # CPU Usage Alert
        if system_stats.cpu_percent > thresholds.get('cpu', 80):
            alert = self.create_alert(
                alert_type="High CPU Usage",
                message=f"CPU usage is {system_stats.cpu_percent:.1f}% (threshold: {thresholds.get('cpu', 80)}%)",
                severity='high' if system_stats.cpu_percent > 90 else 'medium'
            )
            alerts.append(alert)
        
        # Memory Usage Alert
        if system_stats.memory_percent > thresholds.get('memory', 85):
            alert = self.create_alert(
                alert_type="High Memory Usage",
                message=f"Memory usage is {system_stats.memory_percent:.1f}% (threshold: {thresholds.get('memory', 85)}%)",
                severity='high' if system_stats.memory_percent > 95 else 'medium'
            )
            alerts.append(alert)
        
        # Disk Usage Alert
        if system_stats.disk_percent > thresholds.get('disk', 90):
            alert = self.create_alert(
                alert_type="High Disk Usage",
                message=f"Disk usage is {system_stats.disk_percent:.1f}% (threshold: {thresholds.get('disk', 90)}%)",
                severity='critical' if system_stats.disk_percent > 95 else 'high'
            )
            alerts.append(alert)
        
        return alerts
    
    def process_network_alerts(self, upload_mbps: float, download_mbps: float, 
                             anomalies: List[str], threshold: float) -> List[Alert]:
        """Process network statistics and create alerts"""
        alerts = []
        
        # Bandwidth threshold alerts
        if upload_mbps > threshold:
            alert = self.create_alert(
                alert_type="High Upload Bandwidth",
                message=f"Upload bandwidth is {upload_mbps:.2f} Mbps (threshold: {threshold} Mbps)",
                severity='high' if upload_mbps > threshold * 1.5 else 'medium'
            )
            alerts.append(alert)
        
        if download_mbps > threshold:
            alert = self.create_alert(
                alert_type="High Download Bandwidth",
                message=f"Download bandwidth is {download_mbps:.2f} Mbps (threshold: {threshold} Mbps)",
                severity='high' if download_mbps > threshold * 1.5 else 'medium'
            )
            alerts.append(alert)
        
        # Anomaly alerts
        for anomaly in anomalies:
            alert = self.create_alert(
                alert_type="Network Traffic Anomaly",
                message=anomaly,
                severity='medium'
            )
            alerts.append(alert)
        
        return alerts
    
    def process_device_alerts(self, device_statuses: List) -> List[Alert]:
        """Process device ping results and create alerts for unreachable devices"""
        alerts = []
        
        for status in device_statuses:
            if not status.is_reachable:
                alert = self.create_alert(
                    alert_type="Device Unreachable",
                    message=f"Device {status.ip_address} is not responding to ping",
                    severity='high'
                )
                alerts.append(alert)
            elif status.response_time and status.response_time > 1000:  # > 1 second
                alert = self.create_alert(
                    alert_type="High Latency",
                    message=f"Device {status.ip_address} has high latency: {status.response_time:.1f}ms",
                    severity='medium'
                )
                alerts.append(alert)
        
        return alerts
    
    def send_all_alerts(self, alerts: List[Alert]) -> Dict[str, int]:
        """Send all alerts via email"""
        results = {'sent': 0, 'failed': 0}
        
        for alert in alerts:
            if self.send_email_alert(alert):
                results['sent'] += 1
            else:
                results['failed'] += 1
        
        return results
    
    def get_alert_summary(self) -> Dict:
        """Get summary of active alerts"""
        summary = {
            'total_alerts': len(self.active_alerts),
            'by_severity': {},
            'by_type': {},
            'recent_alerts': []
        }
        
        # Count by severity
        for alert in self.active_alerts:
            summary['by_severity'][alert.severity] = summary['by_severity'].get(alert.severity, 0) + 1
            summary['by_type'][alert.alert_type] = summary['by_type'].get(alert.alert_type, 0) + 1
        
        # Get recent alerts (last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        summary['recent_alerts'] = [
            alert for alert in self.active_alerts 
            if alert.timestamp >= cutoff_time
        ]
        
        return summary
