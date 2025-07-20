# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive bridge engineering safety assessment software that calculates settlement impact ranges for bridge pile foundations based on Boussinesq theory. The software supports three main modules:

1. **Bridge Settlement Analysis** - Dual pile system settlement calculations
2. **Pipeline Crossing Analysis** - Roadbed pipeline calculations  
3. **Tower Foundation Analysis** - Power line tower foundation calculations

## Architecture

### Core Components

- **main.py** - Application entry point with splash screen and main window initialization
- **gui/multi_module_window.py** - Main GUI application with tabbed interface for the three modules
- **calculation/settlement.py** - Primary settlement calculation engine using Boussinesq theory
- **calculation/boussinesq.py** - Boussinesq stress and settlement calculations
- **calculation/correction.py** - Engineering correction factors for pile parameters
- **visualization/plotter.py** - Result visualization (contour plots, radar charts, etc.)
- **utils/exporter.py** - Excel and JSON result export functionality
- **utils/validator.py** - Input parameter validation

### Key Calculation Features

- **16 Standard Analysis Points**: 4×4 grid of measurement points under roadbed
- **Dual Pile System**: Considers interaction between two pile foundations
- **Multi-layer Soil Support**: Handles complex geological conditions
- **FLAC3D Calibration**: Numerical simulation validation
- **JTG D30-2015 Compliance**: Chinese highway design standards

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# For development environment
pip install numpy==1.19.5 pandas==1.1.5 matplotlib==3.3.4 openpyxl==3.0.9 xlsxwriter==3.0.2 Pillow==8.4.0 cx_Freeze==6.8.4
```

### Running the Application
```bash
# Development mode
python main.py

# Run specific module tests
python test_software.py
python test_excel_export_simple.py
python test_contour_fix.py
```

### Building Executables
```bash
# Build with cx_Freeze (primary method)
python setup.py build

# Alternative build method
python build_exe.py

# Build with cx_Freeze standalone
python build_with_cxfreeze.py
```

### Testing
```bash
# Run all tests
python -m pytest test_*.py

# Run specific test modules
python test_main.py
python test_software.py
python test_excel_export_fix.py
```

## Key Technical Specifications

### Settlement Calculation
- **Theory**: Boussinesq elastic theory with engineering corrections
- **Analysis Points**: 16 standard points in 4×4 grid (4 depths × 4 horizontal positions)
- **Coordinate System**: 
  - X: Roadbed transverse direction (center line = 0)
  - Y: Roadbed longitudinal direction (piles at Y=0)
  - Z: Depth below ground (positive downward)

### Safety Assessment Criteria
- **Highway**: 200mm general limit, 150mm bridge limit
- **Primary Road**: 300mm general limit, 200mm bridge limit  
- **Secondary Road**: 400mm general limit, 300mm bridge limit
- **Tertiary/Quaternary**: 500-600mm limits

### Color Coding System
- **Red**: Settlement > allowable value
- **Orange**: 60-100% of allowable value
- **Yellow**: 30-60% of allowable value  
- **Green**: <30% of allowable value

## File Structure

```
├── calculation/          # Core calculation modules
│   ├── settlement.py     # Main settlement calculator
│   ├── boussinesq.py     # Boussinesq theory implementation
│   ├── correction.py     # Parameter correction factors
│   ├── pipeline_calculator.py
│   └── tower_calculator.py
├── gui/                  # GUI components
│   ├── main_window.py    # Legacy single-module window
│   └── multi_module_window.py  # Current main interface
├── utils/                # Utility modules
│   ├── exporter.py       # Excel/JSON export
│   └── validator.py      # Input validation
├── visualization/        # Result visualization
│   └── plotter.py        # Matplotlib plotting functions
├── test_*.py            # Test files for various components
├── demo_output/         # Sample calculation results
├── resources/           # Application icons and resources
└── templates/           # Report templates
```

## Important Notes

### Input Parameters
- **Pile Parameters**: diameter (0.3-5.0m), length (3-80m), load (kN)
- **Road Parameters**: width, distance from piles (m)
- **Soil Layers**: compression modulus (MPa), Poisson's ratio, depth ranges

### Development Considerations
- **Python 3.7+** required (tested with 3.7-3.9)
- **Windows-specific** build configuration in setup.py
- **Chinese character support** configured for matplotlib
- **Memory requirements**: 4GB+ RAM recommended
- **Large datasets**: 16 points × multiple load cases

### Export Formats
- **Excel (.xlsx)**: Multi-sheet reports with calculations, charts, summaries
- **JSON**: Structured data export for integration
- **CSV**: Raw calculation data
- **PNG**: Visualization images (contour plots, radar charts)

### Testing Strategy
- **Unit tests**: Individual calculation modules
- **Integration tests**: GUI functionality and export features
- **Validation tests**: Against known engineering cases
- **Visualization tests**: Chart generation and formatting