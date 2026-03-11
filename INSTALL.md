# Installation and Usage Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (for map tiles and geocoding)

## Installation Steps

### 1. Create a Virtual Environment (Recommended)

```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python main.py
```

## Features Overview

### Map Interaction
- **Click** on the map to add coordinate markers
- **Double-click** on markers to remove them
- **Scroll** to zoom in/out
- **Click and drag** to pan the map

### Location Search
1. Type a location name in the search bar (e.g., "Eiffel Tower", "Tokyo, Japan")
2. Press Enter or click the "Search" button
3. The map will center on the found location

### Coordinate Management
- View all selected coordinates in the right panel
- Each coordinate shows its order, label, latitude, and longitude
- Use "Clear All Markers" to remove all points

### Export Options
- **Export to JSON**: Saves coordinates with metadata in JSON format
- **Export to CSV**: Saves coordinates in a spreadsheet-compatible format

## Troubleshooting

### Map Not Loading
- Check your internet connection
- Ensure the `assets/map.html` file exists

### Search Not Working
- Verify internet connection
- The app uses OpenStreetMap's Nominatim API (rate-limited to 1 request/second)

### Installation Issues
If you encounter issues installing PyQt6:

**On Linux:**
```bash
sudo apt-get install python3-pyqt6 python3-pyqt6.qtwebengine
```

**On macOS:**
```bash
brew install pyqt6
```

**On Windows:**
- Ensure you have the latest pip: `python -m pip install --upgrade pip`
- Try installing with: `pip install PyQt6 PyQt6-WebEngine --user`

## Development

### Project Structure
```
get-gps-coordinate/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── README.md              # Project documentation
├── INSTALL.md             # This file
├── assets/
│   └── map.html           # Leaflet map interface
└── src/
    ├── app.py             # Application class
    ├── models/
    │   └── coordinate.py  # Data model
    ├── ui/
    │   ├── main_window.py # Main window
    │   └── map_widget.py  # Map widget
    └── utils/
        └── exporter.py    # Export functionality
```

## License

MIT License - Feel free to modify and distribute
