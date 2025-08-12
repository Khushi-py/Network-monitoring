#!/usr/bin/env python3
"""
Simple Web Dashboard for Network Monitoring
Optional enhancement - requires Flask
"""

from flask import Flask, render_template, jsonify
import json
from datetime import datetime, timedelta
from src.data_logger import DataLogger
from src.config import Config

app = Flask(__name__)
data_logger = DataLogger()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/network-stats')
def network_stats():
    """API endpoint for network statistics"""
    hours = request.args.get('hours', 24, type=int)
    data = data_logger.get_network_history(hours)
    return jsonify(data)

@app.route('/api/system-stats')
def system_stats():
    """API endpoint for system statistics"""
    hours = request.args.get('hours', 24, type=int)
    data = data_logger.get_system_history(hours)
    return jsonify(data)

@app.route('/api/alerts')
def alerts():
    """API endpoint for alerts"""
    hours = request.args.get('hours', 24, type=int)
    data = data_logger.get_alert_history(hours)
    return jsonify(data)

@app.route('/api/devices')
def devices():
    """API endpoint for device status"""
    hours = request.args.get('hours', 24, type=int)
    data = data_logger.get_device_history(hours=hours)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
