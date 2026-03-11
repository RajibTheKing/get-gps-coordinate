# Developer Guide

## Architecture Overview

### Design Pattern
The application follows the **Model-View-Controller (MVC)** pattern with clear separation of concerns:

- **Models** (`src/models/`): Data structures and business logic
- **Views** (`src/ui/`): User interface components
- **Controllers** (`src/utils/`): Business logic and data processing

### Component Structure

```
┌─────────────────────────────────────────┐
│         Main Application (app.py)        │
│  - Application initialization            │
│  - Global styling                        │
│  - Event loop management                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Main Window (main_window.py)       │
│  - UI layout and controls                │
│  - User interactions                     │
│  - Coordinate management                 │
└──────┬──────────────────┬───────────────┘
       │                  │
       ▼                  ▼
┌─────────────┐    ┌─────────────────────┐
│ Map Widget  │    │  Coordinate Model   │
│ (map_widget)│    │  (coordinate.py)    │
│  - Leaflet  │    │  - Data validation  │
│  - Qt/JS    │    │  - Serialization    │
│    Bridge   │    └─────────────────────┘
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│       Map Interface (map.html)           │
│  - Leaflet.js integration                │
│  - OpenStreetMap tiles                   │
│  - Interactive markers                   │
└─────────────────────────────────────────┘
```

## Key Technologies

### Frontend (Map)
- **Leaflet.js**: Open-source JavaScript library for interactive maps
- **OpenStreetMap**: Free, editable map tiles
- **Qt WebEngine**: Renders HTML/JS within Qt application

### Backend (Application)
- **PyQt6**: Cross-platform GUI framework
- **Qt WebChannel**: JavaScript-Python bridge for communication
- **dataclasses**: Clean data modeling
- **requests**: HTTP library for geocoding API

## Key Classes

### Coordinate (`src/models/coordinate.py`)
```python
@dataclass
class Coordinate:
    latitude: float       # -90 to 90
    longitude: float      # -180 to 180
    order: int           # Selection sequence
    label: str           # Human-readable name
```

### MapWidget (`src/ui/map_widget.py`)
- Embeds Leaflet map in Qt widget
- Handles JS-Python communication via `Bridge` class
- Provides methods: `clear_all_markers()`, `set_view()`, `add_marker()`

### MainWindow (`src/ui/main_window.py`)
- Main application window
- Manages UI layout and user interactions
- Coordinates between map widget and data models
- Handles search and export functionality

## JavaScript-Python Bridge

### How It Works
1. **JavaScript → Python**: 
   - User clicks map → JS `coordinateClicked()` called
   - Qt WebChannel sends signal to Python `Bridge` object
   - Python emits `coordinate_added` signal
   - MainWindow handles the signal

2. **Python → JavaScript**:
   - Python calls `page().runJavaScript(script)`
   - JavaScript function executes in the map
   - Example: `clearAllMarkers()`, `setMapView()`

### Bridge Implementation
```python
class Bridge(QObject):
    coordinate_added = pyqtSignal(float, float, int, str)
    
    @pyqtSlot(float, float, int, str)
    def coordinateClicked(self, lat, lon, order, label):
        self.coordinate_added.emit(lat, lon, order, label)
```

## API Integration

### Nominatim Geocoding API
- **URL**: `https://nominatim.openstreetmap.org/search`
- **Rate Limit**: 1 request per second
- **Usage**: Location search functionality
- **Response**: JSON with lat/lon coordinates

## Extending the Application

### Adding New Export Formats
1. Add method to `CoordinateExporter` class
2. Add button in `MainWindow._create_right_panel()`
3. Connect button to export handler

Example:
```python
@staticmethod
def export_to_gpx(coordinates: List[Coordinate], filepath: str) -> bool:
    # GPX export implementation
    pass
```

### Adding Map Providers
Modify `assets/map.html`:
```javascript
// Add Google Maps
L.tileLayer('https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    attribution: 'Map data ©Google'
}).addTo(map);
```

### Custom Marker Styles
Modify marker icon in `map.html`:
```javascript
var customIcon = L.icon({
    iconUrl: 'path/to/icon.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
```

## Testing

### Manual Testing Checklist
- [ ] Map loads correctly
- [ ] Markers appear on click
- [ ] Search finds locations
- [ ] Export to JSON works
- [ ] Export to CSV works
- [ ] Clear all removes markers
- [ ] Window resizes properly
- [ ] Double-click removes markers

### Unit Testing (Future)
```python
# Example test structure
import unittest
from src.models.coordinate import Coordinate

class TestCoordinate(unittest.TestCase):
    def test_valid_coordinate(self):
        coord = Coordinate(40.7128, -74.0060, 1, "Test")
        self.assertEqual(coord.latitude, 40.7128)
    
    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            Coordinate(91.0, 0.0, 1, "Invalid")
```

## Performance Considerations

1. **Map Rendering**: Uses hardware acceleration via Qt WebEngine
2. **Marker Limit**: Leaflet handles 1000+ markers efficiently
3. **Memory**: Each marker ~100 bytes, scales well for typical use
4. **Network**: Only tiles and search use network; markers are client-side

## Troubleshooting

### Common Issues

**Map not loading**
- Check `assets/map.html` path in `MapWidget._load_map()`
- Verify internet connection for tiles

**JS-Python bridge not working**
- Ensure WebChannel is properly initialized
- Check JavaScript console in debug mode

**Search failing**
- Respect Nominatim rate limits (1 req/sec)
- Verify User-Agent header is set

## Building for Distribution

### Using PyInstaller
```bash
pip install pyinstaller

# Create standalone executable
pyinstaller --name="GPS-Coordinate-Tool" \
            --windowed \
            --add-data "assets:assets" \
            main.py
```

### Dependencies for Distribution
- Include Qt libraries
- Bundle OpenSSL for HTTPS requests
- Include assets folder

## License and Attribution

- **OpenStreetMap**: © OpenStreetMap contributors (ODbL)
- **Leaflet**: BSD 2-Clause License
- **PyQt6**: GPL v3 or commercial license
- **Application**: MIT License (customizable)

## Contributing Guidelines

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## Code Style

- Follow PEP 8 for Python code
- Use type hints for function signatures
- Document all public methods with docstrings
- Keep functions focused and under 50 lines
- Use meaningful variable names

## Version History

- **1.0.0** (2026-03-11): Initial release
  - Interactive map with OpenStreetMap
  - Click-to-add coordinate markers
  - Location search
  - JSON/CSV export
  - Cross-platform GUI
