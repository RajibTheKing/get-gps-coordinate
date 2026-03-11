"""
Coordinate export functionality

This module handles exporting coordinates to various file formats (JSON, CSV).
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import List
from ..models.coordinate import Coordinate


class CoordinateExporter:
    """Handles exporting coordinates to different file formats."""
    
    @staticmethod
    def export_to_json(coordinates: List[Coordinate], filepath: str) -> bool:
        """
        Export coordinates to JSON format.
        
        Args:
            coordinates: List of Coordinate objects to export
            filepath: Path where the JSON file will be saved
            
        Returns:
            True if export was successful, False otherwise
        """
        try:
            data = {
                "coordinates": [coord.to_dict() for coord in coordinates],
                "total_points": len(coordinates),
                "exported_at": datetime.now().isoformat()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False
    
    @staticmethod
    def export_to_csv(coordinates: List[Coordinate], filepath: str) -> bool:
        """
        Export coordinates to CSV format.
        
        Args:
            coordinates: List of Coordinate objects to export
            filepath: Path where the CSV file will be saved
            
        Returns:
            True if export was successful, False otherwise
        """
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(['Order', 'Latitude', 'Longitude', 'Label'])
                
                # Write data
                for coord in coordinates:
                    writer.writerow([
                        coord.order,
                        f"{coord.latitude:.6f}",
                        f"{coord.longitude:.6f}",
                        coord.label
                    ])
            
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    @staticmethod
    def import_from_json(filepath: str) -> List[Coordinate]:
        """
        Import coordinates from JSON format.
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            List of Coordinate objects
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            coordinates = []
            for coord_data in data.get('coordinates', []):
                coord = Coordinate(
                    latitude=coord_data['latitude'],
                    longitude=coord_data['longitude'],
                    order=coord_data['order'],
                    label=coord_data.get('label', '')
                )
                coordinates.append(coord)
            
            return coordinates
        except Exception as e:
            print(f"Error importing from JSON: {e}")
            return []
