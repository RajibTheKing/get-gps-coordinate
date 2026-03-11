#!/usr/bin/env python3
"""
GPS Coordinate Extraction Tool
Main entry point for the application
"""

import sys
from pathlib import Path

# Add the src directory to the path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from src.app import main

if __name__ == '__main__':
    main()
