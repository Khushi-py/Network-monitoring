#!/usr/bin/env python3
"""
Quick Start Script for Network Monitoring System
Provides easy options to run different components
"""

import os
import sys
import subprocess

def main():
    print("🚀 Network Monitoring System - Quick Start")
    print("=" * 50)
    print("1. 🌐 Start Full System (Monitoring + Dashboard)")
    print("2. 💻 Start Monitoring Only (Console)")
    print("3. 📊 Start Dashboard Only")
    print("4. 🧪 Run Tests")
    print("5. ⚙️  Setup System")
    print("6. 🔧 Utilities")
    print("0. ❌ Exit")
    print("=" * 50)
    
    while True:
        choice = input("\n👉 Select an option (0-6): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            print("🚀 Starting full system...")
            subprocess.run([sys.executable, "start_dashboard.py"])
        elif choice == "2":
            print("💻 Starting monitoring only...")
            subprocess.run([sys.executable, "main.py"])
        elif choice == "3":
            print("📊 Starting dashboard only...")
            subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
        elif choice == "4":
            print("🧪 Running tests...")
            subprocess.run([sys.executable, "test_system.py"])
        elif choice == "5":
            print("⚙️ Running setup...")
            subprocess.run([sys.executable, "setup.py"])
        elif choice == "6":
            print("\n🔧 Available utilities:")
            print("  python utils.py test          # Test connectivity")
            print("  python utils.py stats         # Show current stats")
            print("  python utils.py interfaces    # Show network interfaces")
            print("  python utils.py analyze       # Analyze historical data")
            print("  python utils.py export        # Export data")
            
            util_choice = input("\n👉 Enter utility command (or press Enter to return): ").strip()
            if util_choice:
                subprocess.run(util_choice.split())
        else:
            print("❌ Invalid choice. Please select 0-6.")

if __name__ == "__main__":
    main()
