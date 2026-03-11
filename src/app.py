"""
Application Module

This module provides the main application class that initializes and runs
the GPS Coordinate Extraction Tool.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from .ui.main_window import MainWindow


class GPSCoordinateApp:
    """
    Main application class for the GPS Coordinate Extraction Tool.
    
    This class handles application initialization, styling, and execution.
    """
    
    def __init__(self):
        """Initialize the application."""
        # Enable high DPI scaling
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        
        # Create the application
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("GPS Coordinate Extraction Tool")
        self.app.setApplicationVersion("1.0.0")
        
        # Set application style
        self._set_application_style()
        
        # Create the main window
        self.main_window = MainWindow()
    
    def _set_application_style(self):
        """Set the application-wide stylesheet."""
        style = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 13px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #45a049;
        }
        
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
        
        QLineEdit {
            padding: 6px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 13px;
        }
        
        QLineEdit:focus {
            border: 2px solid #4CAF50;
        }
        
        QListWidget {
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 12px;
        }
        
        QListWidget::item {
            padding: 5px;
        }
        
        QListWidget::item:selected {
            background-color: #4CAF50;
            color: white;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #ddd;
            border-radius: 6px;
            margin-top: 10px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
        
        QLabel {
            font-size: 13px;
        }
        
        QStatusBar {
            background-color: #e0e0e0;
            font-size: 12px;
        }
        """
        self.app.setStyleSheet(style)
    
    def run(self) -> int:
        """
        Run the application.
        
        Returns:
            Exit code
        """
        self.main_window.show()
        return self.app.exec()


def main():
    """
    Main entry point for the application.
    
    Returns:
        Exit code
    """
    app = GPSCoordinateApp()
    sys.exit(app.run())


if __name__ == '__main__':
    main()
