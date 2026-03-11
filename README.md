# GPS Coordinate Extraction Application

A professional desktop application for extracting GPS coordinates from interactive maps.

## Features

- Interactive map powered by OpenStreetMap
- Click to select coordinates on the map
- Search for locations worldwide
- Zoom and pan controls
- Export coordinates to JSON or CSV
- Maintains order of selected coordinates
- Resizable window with full-screen support

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## How to Use

1. **Search Location**: Enter a location in the search bar and press Enter or click Search
2. **Select Coordinates**: Click anywhere on the map to add coordinate markers
3. **Remove Markers**: Double-click on a marker to remove it
4. **Export Data**: Click "Export to JSON" or "Export to CSV" to save your coordinates
5. **Clear All**: Click "Clear All" to remove all markers

## Export Format

### JSON
```json
{
  "coordinates": [
    {"order": 1, "latitude": 40.7128, "longitude": -74.0060, "label": "Point 1"},
    {"order": 2, "latitude": 34.0522, "longitude": -118.2437, "label": "Point 2"}
  ],
  "total_points": 2,
  "exported_at": "2026-03-11T10:30:00"
}
```

### CSV
```csv
Order,Latitude,Longitude,Label
1,40.7128,-74.0060,Point 1
2,34.0522,-118.2437,Point 2
```

## License

MIT
