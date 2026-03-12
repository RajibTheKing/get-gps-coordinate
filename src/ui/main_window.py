"""
Main Window Component

This module provides the main application window with map display and controls.
"""

import requests
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QLabel, QListWidget, 
    QFileDialog, QMessageBox, QSplitter, QGroupBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QScreen
from .map_widget import MapWidget
from ..models.coordinate import Coordinate
from ..utils.exporter import CoordinateExporter


class MainWindow(QMainWindow):
    """
    Main application window.
    
    Provides the complete UI including map display, coordinate list,
    search functionality, and export controls.
    """
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Store coordinates
        self.coordinates = []
        
        # Set up the window
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
    
    def _setup_window(self):
        """Configure the main window properties."""
        self.setWindowTitle("GPS Coordinate Extraction Tool")
        
        # Get screen size and set window to 90% of screen
        screen = QScreen.availableGeometry(self.screen())
        width = int(screen.width() * 0.9)
        height = int(screen.height() * 0.9)
        
        # Center the window
        self.setGeometry(
            (screen.width() - width) // 2,
            (screen.height() - height) // 2,
            width,
            height
        )
        
        # Set minimum size
        self.setMinimumSize(QSize(800, 600))
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Apply global stylesheet for better visibility
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QLineEdit {
                padding: 6px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
                color: #2c3e50;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                color: #2c3e50;
                font-size: 11px;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QStatusBar {
                background-color: #34495e;
                color: white;
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
            }
            QStatusBar::item {
                border: none;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Search bar section
        search_layout = self._create_search_bar()
        main_layout.addLayout(search_layout)
        
        # Splitter for map and coordinate list
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Map widget
        self.map_widget = MapWidget()
        splitter.addWidget(self.map_widget)
        
        # Right panel with coordinate list and controls
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter sizes (map takes 70%, panel takes 30%)
        splitter.setSizes([700, 300])
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar().showMessage("Ready - Click on the map to add coordinates")
    
    def _create_search_bar(self) -> QHBoxLayout:
        """
        Create the search bar layout.
        
        Returns:
            QHBoxLayout containing search controls
        """
        layout = QHBoxLayout()
        
        # Search label
        search_label = QLabel("Search Location:")
        search_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #2c3e50;")
        layout.addWidget(search_label)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter location (e.g., 'New York', 'Paris, France')...")
        self.search_input.returnPressed.connect(self._search_location)
        layout.addWidget(self.search_input)
        
        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self._search_location)
        layout.addWidget(self.search_button)
        
        return layout
    
    def _create_right_panel(self) -> QWidget:
        """
        Create the right panel with coordinate list and controls.
        
        Returns:
            QWidget containing the right panel
        """
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Coordinates group box
        coords_group = QGroupBox("Selected Coordinates")
        coords_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 5px;
                background-color: white;
                color: #2c3e50;
            }
        """)
        coords_layout = QVBoxLayout(coords_group)
        
        # Coordinate list
        self.coordinate_list = QListWidget()
        self.coordinate_list.setAlternatingRowColors(False)
        coords_layout.addWidget(self.coordinate_list)
        
        # Info label
        self.info_label = QLabel("Total Points: 0")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("""
            font-weight: bold;
            font-size: 12px;
            color: #2c3e50;
            background-color: #ecf0f1;
            padding: 8px;
            border-radius: 3px;
        """)
        coords_layout.addWidget(self.info_label)
        
        layout.addWidget(coords_group)
        
        # Control buttons group
        control_group = QGroupBox("Actions")
        control_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 5px;
                background-color: white;
                color: #2c3e50;
            }
        """)
        control_layout = QVBoxLayout(control_group)
        
        # Clear button
        self.clear_button = QPushButton("Clear All Markers")
        self.clear_button.clicked.connect(self._clear_all_coordinates)
        control_layout.addWidget(self.clear_button)
        
        # Export buttons
        self.export_json_button = QPushButton("Export to JSON")
        self.export_json_button.clicked.connect(lambda: self._export_coordinates('json'))
        control_layout.addWidget(self.export_json_button)
        
        self.export_csv_button = QPushButton("Export to CSV")
        self.export_csv_button.clicked.connect(lambda: self._export_coordinates('csv'))
        control_layout.addWidget(self.export_csv_button)
        
        layout.addWidget(control_group)
        
        # Instructions
        instructions = QLabel(
            "<b>Instructions:</b><br>"
            "• Click on map to add points<br>"
            "• Double-click marker to remove<br>"
            "• Use search to find locations<br>"
            "• Scroll to zoom, drag to pan"
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("""
            padding: 12px;
            background-color: #d5dbdb;
            border: 1px solid #95a5a6;
            border-radius: 5px;
            color: #2c3e50;
            font-size: 11px;
            line-height: 1.4;
        """)
        layout.addWidget(instructions)
        
        layout.addStretch()
        
        return panel
    
    def _connect_signals(self):
        """Connect signals and slots."""
        self.map_widget.coordinate_selected.connect(self._on_coordinate_selected)
    
    def _on_coordinate_selected(self, coordinate: Coordinate):
        """
        Handle coordinate selection from the map.
        
        Args:
            coordinate: Selected coordinate
        """
        print(f"MainWindow: Received coordinate: {coordinate}")
        
        # Calculate cumulative distance
        if len(self.coordinates) == 0:
            # First point, distance is 0
            coordinate.distance = 0.0
        else:
            # Calculate distance from previous point and add to cumulative total
            previous_coord = self.coordinates[-1]
            segment_distance = Coordinate.calculate_distance(previous_coord, coordinate)
            coordinate.distance = previous_coord.distance + segment_distance
        
        self.coordinates.append(coordinate)
        print(f"MainWindow: Total coordinates: {len(self.coordinates)}, Distance: {coordinate.distance:.2f}m")
        self._update_coordinate_list()
        
        # Update status bar with distance info
        if coordinate.order == 1:
            status_msg = f"Added: {coordinate.label} - Lat: {coordinate.latitude:.6f}, Lon: {coordinate.longitude:.6f} - Distance: 0.00m"
        else:
            previous_coord = self.coordinates[-2]
            segment_distance = Coordinate.calculate_distance(previous_coord, coordinate)
            status_msg = (f"Added: {coordinate.label} - Lat: {coordinate.latitude:.6f}, Lon: {coordinate.longitude:.6f} - "
                         f"Segment: {segment_distance:.2f}m, Cumulative: {coordinate.distance:.2f}m")
        
        self.statusBar().showMessage(status_msg)
    
    def _update_coordinate_list(self):
        """Update the coordinate list display."""
        self.coordinate_list.clear()
        
        for coord in self.coordinates:
            # Format distance
            if coord.distance >= 1000:
                distance_str = f"{coord.distance / 1000:.2f} km"
            else:
                distance_str = f"{coord.distance:.2f} m"
            
            item_text = (
                f"{coord.order}. {coord.label} - "
                f"({coord.latitude:.6f}, {coord.longitude:.6f}) - "
                f"Distance: {distance_str}"
            )
            self.coordinate_list.addItem(item_text)
        
        # Calculate total distance
        total_distance = self.coordinates[-1].distance if self.coordinates else 0
        if total_distance >= 1000:
            total_distance_str = f"{total_distance / 1000:.2f} km"
        else:
            total_distance_str = f"{total_distance:.2f} m"
        
        self.info_label.setText(f"Total Points: {len(self.coordinates)} | Total Distance: {total_distance_str}")
    
    def _clear_all_coordinates(self):
        """Clear all coordinates from the list and map."""
        if self.coordinates:
            reply = QMessageBox.question(
                self,
                'Clear All',
                'Are you sure you want to clear all coordinates?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.coordinates.clear()
                self._update_coordinate_list()
                self.map_widget.clear_all_markers()
                self.statusBar().showMessage("All coordinates cleared")
    
    def _search_location(self):
        """Search for a location and center the map on it."""
        location = self.search_input.text().strip()
        
        if not location:
            QMessageBox.warning(self, "Empty Search", "Please enter a location to search.")
            return
        
        self.statusBar().showMessage(f"Searching for: {location}...")
        self.search_button.setEnabled(False)
        
        try:
            # Use Nominatim API for geocoding (OpenStreetMap)
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': location,
                'format': 'json',
                'limit': 1
            }
            headers = {
                'User-Agent': 'GPS-Coordinate-Extraction-Tool/1.0'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            results = response.json()
            
            if results:
                lat = float(results[0]['lat'])
                lon = float(results[0]['lon'])
                display_name = results[0].get('display_name', location)
                
                # Center map on the location
                self.map_widget.set_view(lat, lon, 13)
                
                self.statusBar().showMessage(f"Found: {display_name}")
            else:
                QMessageBox.information(
                    self,
                    "Location Not Found",
                    f"Could not find location: {location}\n\nTry being more specific or use a different name."
                )
                self.statusBar().showMessage("Location not found")
        
        except requests.RequestException as e:
            QMessageBox.critical(
                self,
                "Search Error",
                f"Error searching for location:\n{str(e)}\n\nPlease check your internet connection."
            )
            self.statusBar().showMessage("Search failed")
        
        finally:
            self.search_button.setEnabled(True)
    
    def _export_coordinates(self, format_type: str):
        """
        Export coordinates to file.
        
        Args:
            format_type: 'json' or 'csv'
        """
        if not self.coordinates:
            QMessageBox.warning(
                self,
                "No Coordinates",
                "No coordinates to export. Please add some points to the map first."
            )
            return
        
        # File dialog
        if format_type == 'json':
            file_filter = "JSON Files (*.json)"
            default_name = "coordinates.json"
        else:
            file_filter = "CSV Files (*.csv)"
            default_name = "coordinates.csv"
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            f"Export to {format_type.upper()}",
            str(Path.home() / default_name),
            file_filter
        )
        
        if filepath:
            # Ensure correct extension
            if format_type == 'json' and not filepath.endswith('.json'):
                filepath += '.json'
            elif format_type == 'csv' and not filepath.endswith('.csv'):
                filepath += '.csv'
            
            # Export
            if format_type == 'json':
                success = CoordinateExporter.export_to_json(self.coordinates, filepath)
            else:
                success = CoordinateExporter.export_to_csv(self.coordinates, filepath)
            
            if success:
                QMessageBox.information(
                    self,
                    "Export Successful",
                    f"Coordinates exported successfully to:\n{filepath}"
                )
                self.statusBar().showMessage(f"Exported {len(self.coordinates)} coordinates to {format_type.upper()}")
            else:
                QMessageBox.critical(
                    self,
                    "Export Failed",
                    f"Failed to export coordinates to {format_type.upper()} file."
                )
                self.statusBar().showMessage("Export failed")
