"""
main.py
-------
Entry point for the B+ Tree Visualizer application.
Run this file to start the program.
"""

import subprocess
import sys
import importlib.util
import os

def is_package_installed(package_name):
    """Check if a Python package is installed."""
    return importlib.util.find_spec(package_name) is not None

def install_package(package_name):
    """Install a Python package using pip."""
    try:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"{package_name} installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}. Error: {e}")
        return False

def prompt_install(package_name):
    """Ask user if they want to install the package."""
    while True:
        response = input(f"{package_name} is not installed. Do you want to install it now? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def run_main_app():
    """Import and run the main GUI application."""
    try:
        from gui_pyqt6 import run
        run()
    except ImportError as e:
        print(f"Error importing gui module: {e}")
        print("Make sure gui.py exists in the same directory.")
        sys.exit(1)

def main():
    """Main entry point with PyQt6 dependency check."""
    
    # Check if PyQt6 is installed
    if not is_package_installed("PyQt6"):
        print("PyQt6 is required for this application.")
        
        if prompt_install("PyQt6"):
            if install_package("PyQt6"):
                print("PyQt6 installed. Restarting application...")
                # Restart the application
                os.execv(sys.executable, [sys.executable] + sys.argv)
            else:
                print("Failed to install PyQt6. Please install it manually: pip install PyQt6")
                sys.exit(1)
        else:
            print("PyQt6 is required to run this application. Exiting.")
            sys.exit(1)
    else:
        # PyQt6 is installed, run the app
        run_main_app()

if __name__ == "__main__":
    main()