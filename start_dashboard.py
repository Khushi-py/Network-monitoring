#!/usr/bin/env python3
"""
Network Monitoring Dashboard Launcher
Starts both the monitoring system and the Streamlit dashboard
"""

import subprocess
import threading
import time
import signal
import sys
import os
from datetime import datetime

class DashboardLauncher:
    """Manages both the monitoring system and dashboard"""
    
    def __init__(self):
        self.monitoring_process = None
        self.dashboard_process = None
        self.running = False
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n📡 Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)
    
    def start_monitoring_system(self):
        """Start the main monitoring system"""
        try:
            print("🚀 Starting Network Monitoring System...")
            self.monitoring_process = subprocess.Popen(
                [sys.executable, "main.py", "--dashboard"],
                cwd=os.path.dirname(__file__),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("✅ Monitoring system started")
            return True
        except Exception as e:
            print(f"❌ Failed to start monitoring system: {e}")
            return False
    
    def start_dashboard(self):
        """Start the Streamlit dashboard"""
        try:
            print("🌐 Starting Streamlit Dashboard...")
            
            # Wait a moment for monitoring system to initialize
            time.sleep(3)
            
            self.dashboard_process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", "dashboard.py",
                "--server.headless", "true",
                "--server.port", "8501",
                "--server.address", "0.0.0.0"
            ], cwd=os.path.dirname(__file__))
            
            print("✅ Dashboard started")
            print("🌐 Dashboard URL: http://localhost:8501")
            return True
        except Exception as e:
            print(f"❌ Failed to start dashboard: {e}")
            return False
    
    def start(self):
        """Start both systems"""
        self.running = True
        
        print("🚀 Network Monitoring & Dashboard System")
        print("=" * 50)
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # Start monitoring system
        if not self.start_monitoring_system():
            print("❌ Failed to start monitoring system")
            return False
        
        # Start dashboard
        if not self.start_dashboard():
            print("❌ Failed to start dashboard")
            self.stop()
            return False
        
        print("\n✅ Both systems started successfully!")
        print("📊 Console monitoring: Check terminal output")
        print("🌐 Web dashboard: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop both systems")
        print("=" * 50)
        
        # Monitor processes
        try:
            while self.running:
                # Check if processes are still running
                if self.monitoring_process and self.monitoring_process.poll() is not None:
                    print("⚠️ Monitoring system stopped unexpectedly")
                    break
                
                if self.dashboard_process and self.dashboard_process.poll() is not None:
                    print("⚠️ Dashboard stopped unexpectedly")
                    break
                
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n👋 Received keyboard interrupt")
        finally:
            self.stop()
        
        return True
    
    def stop(self):
        """Stop both systems"""
        self.running = False
        
        print("\n🛑 Stopping systems...")
        
        # Stop dashboard
        if self.dashboard_process:
            try:
                self.dashboard_process.terminate()
                self.dashboard_process.wait(timeout=5)
                print("✅ Dashboard stopped")
            except subprocess.TimeoutExpired:
                self.dashboard_process.kill()
                print("🔪 Dashboard force stopped")
            except Exception as e:
                print(f"⚠️ Error stopping dashboard: {e}")
        
        # Stop monitoring system
        if self.monitoring_process:
            try:
                self.monitoring_process.terminate()
                self.monitoring_process.wait(timeout=10)
                print("✅ Monitoring system stopped")
            except subprocess.TimeoutExpired:
                self.monitoring_process.kill()
                print("🔪 Monitoring system force stopped")
            except Exception as e:
                print(f"⚠️ Error stopping monitoring system: {e}")
        
        print("✅ All systems stopped")

def main():
    """Main entry point"""
    # Check if Streamlit is installed
    try:
        import streamlit
        import plotly
        import pandas
    except ImportError as e:
        print("❌ Missing required dependencies for dashboard")
        print("📦 Install with: pip install -r requirements.txt")
        print(f"   Missing: {e}")
        
        response = input("\n❓ Start monitoring system only? (y/N): ")
        if response.lower() == 'y':
            print("🚀 Starting monitoring system only...")
            subprocess.run([sys.executable, "main.py"])
        return
    
    # Check if configuration exists
    if not os.path.exists('.env'):
        print("⚠️ Configuration file (.env) not found")
        print("📝 Please copy .env.example to .env and configure your settings")
        
        response = input("❓ Continue with default settings? (y/N): ")
        if response.lower() != 'y':
            print("👋 Setup your .env file first, then run again")
            return
    
    # Start the integrated system
    launcher = DashboardLauncher()
    launcher.start()

if __name__ == "__main__":
    main()
