"""
Map Widget Component

This module provides an interactive map widget using Leaflet.js and OpenStreetMap.
"""

import os
from pathlib import Path
from PyQt6.QtCore import QUrl, pyqtSignal, pyqtSlot, QObject, QByteArray
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineUrlRequestInterceptor, QWebEngineProfile
from PyQt6.QtWebChannel import QWebChannel
from ..models.coordinate import Coordinate


class UrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    """
    Intercepts URL requests to add custom headers for tile servers.
    This fixes the OpenStreetMap Referer requirement issue.
    """
    
    def interceptRequest(self, info):
        """
        Intercept and modify URL requests.
        
        Args:
            info: QWebEngineUrlRequestInfo object
        """
        url = info.requestUrl().toString()
        
        # Add Referer header for OpenStreetMap tile requests
        if 'tile.openstreetmap.org' in url:
            info.setHttpHeader(QByteArray(b'Referer'), QByteArray(b'https://www.openstreetmap.org/'))
            info.setHttpHeader(QByteArray(b'User-Agent'), 
                             QByteArray(b'GPS Coordinate Picker Application'))
        
        # Also add headers for other tile providers if needed
        elif 'basemaps.cartocdn.com' in url or 'arcgisonline.com' in url:
            info.setHttpHeader(QByteArray(b'User-Agent'), 
                             QByteArray(b'GPS Coordinate Picker Application'))


class Bridge(QObject):
    """
    Bridge class to enable communication between JavaScript and Python.
    
    Signals:
        coordinate_added: Emitted when a coordinate is clicked on the map
    """
    
    coordinate_added = pyqtSignal(float, float, int, str)
    
    @pyqtSlot(float, float, int, str)
    def coordinateClicked(self, lat: float, lon: float, order: int, label: str):
        """
        Called from JavaScript when a coordinate is clicked.
        
        Args:
            lat: Latitude
            lon: Longitude
            order: Order of selection
            label: Label for the coordinate
        """
        print(f"Bridge received coordinate: {label} - Lat: {lat}, Lon: {lon}, Order: {order}")
        self.coordinate_added.emit(lat, lon, order, label)


class MapWidget(QWebEngineView):
    """
    Interactive map widget for displaying and selecting GPS coordinates.
    
    Signals:
        coordinate_selected: Emitted when a coordinate is selected on the map
    """
    
    coordinate_selected = pyqtSignal(Coordinate)
    
    def __init__(self, parent=None):
        """
        Initialize the map widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Set up URL request interceptor to fix tile server access
        self.interceptor = UrlRequestInterceptor()
        profile = QWebEngineProfile.defaultProfile()
        profile.setUrlRequestInterceptor(self.interceptor)
        
        # Enable web settings to allow loading external resources
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        
        # Enable JavaScript console messages
        self.page().javaScriptConsoleMessage = self._js_console_message
        
        # Set up the bridge for JS-Python communication
        self.bridge = Bridge()
        self.bridge.coordinate_added.connect(self._on_coordinate_added)
        
        # Set up web channel
        self.channel = QWebChannel()
        self.channel.registerObject('qtBridge', self.bridge)
        self.page().setWebChannel(self.channel)
        
        # Load the map HTML
        self._load_map()
    
    def _load_map(self):
        """Load the map HTML file."""
        # Get the path to the map.html file
        current_dir = Path(__file__).parent.parent.parent
        map_file = current_dir / 'assets' / 'map.html'
        
        if map_file.exists():
            url = QUrl.fromLocalFile(str(map_file.absolute()))
            self.load(url)
        else:
            print(f"Error: Map file not found at {map_file}")
    
    @pyqtSlot(float, float, int, str)
    def _on_coordinate_added(self, lat: float, lon: float, order: int, label: str):
        """
        Handle coordinate addition from the map.
        
        Args:
            lat: Latitude
            lon: Longitude
            order: Order of selection
            label: Label for the coordinate
        """
        print(f"MapWidget: Creating coordinate object for {label}")
        coordinate = Coordinate(
            latitude=lat,
            longitude=lon,
            order=order,
            label=label
        )
        print(f"MapWidget: Emitting coordinate_selected signal")
        self.coordinate_selected.emit(coordinate)
    
    def _js_console_message(self, level, message, line_number, source_id):
        """
        Handle JavaScript console messages for debugging.
        
        Args:
            level: Message level
            message: Console message
            line_number: Line number in source
            source_id: Source identifier
        """
        print(f"JS Console [{level}]: {message} (line {line_number})")
    
    def clear_all_markers(self):
        """Remove all markers from the map."""
        self.page().runJavaScript("clearAllMarkers();")
    
    def set_view(self, lat: float, lon: float, zoom: int = 13):
        """
        Set the map view to specific coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            zoom: Zoom level (default: 13)
        """
        script = f"setMapView({lat}, {lon}, {zoom});"
        self.page().runJavaScript(script)
    
    def add_marker(self, coordinate: Coordinate):
        """
        Add a marker to the map programmatically.
        
        Args:
            coordinate: Coordinate object to add
        """
        script = f"addMarker({coordinate.latitude}, {coordinate.longitude}, {coordinate.order}, '{coordinate.label}', {coordinate.distance});"
        self.page().runJavaScript(script)
    
    def get_all_markers(self):
        """
        Get all markers from the map.
        
        Note: This is asynchronous and uses a callback.
        """
        self.page().runJavaScript("getAllMarkers();", self._handle_markers_result)
    
    def _handle_markers_result(self, result):
        """
        Handle the result from getAllMarkers JavaScript function.
        
        Args:
            result: List of marker data from JavaScript
        """
        if result:
            print(f"Retrieved {len(result)} markers from map")
