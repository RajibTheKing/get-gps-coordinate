"""
Coordinate data model

This module defines the Coordinate class that represents a geographic point
with latitude, longitude, and metadata.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Coordinate:
    """
    Represents a geographic coordinate point.
    
    Attributes:
        latitude (float): The latitude in decimal degrees (-90 to 90)
        longitude (float): The longitude in decimal degrees (-180 to 180)
        order (int): The order in which this coordinate was selected
        label (str): A human-readable label for this coordinate
    """
    
    latitude: float
    longitude: float
    order: int
    label: str = ""
    
    def __post_init__(self):
        """Validate coordinate values after initialization."""
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Latitude must be between -90 and 90, got {self.latitude}")
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Longitude must be between -180 and 180, got {self.longitude}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert coordinate to dictionary format.
        
        Returns:
            Dict containing all coordinate data
        """
        return asdict(self)
    
    def to_tuple(self) -> tuple:
        """
        Convert coordinate to (latitude, longitude) tuple.
        
        Returns:
            Tuple of (latitude, longitude)
        """
        return (self.latitude, self.longitude)
    
    def __str__(self) -> str:
        """String representation of the coordinate."""
        return f"{self.label} ({self.latitude:.6f}, {self.longitude:.6f})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Coordinate(lat={self.latitude}, lon={self.longitude}, order={self.order}, label='{self.label}')"
