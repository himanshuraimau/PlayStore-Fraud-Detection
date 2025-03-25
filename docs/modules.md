# Modules Documentation

## Main Modules

### `main.py`

The entry point for the application that handles command-line arguments and initializes the main workflow.

**Key functions:**
- `parse_args()`: Parses command line arguments
- `main()`: Main entry point for the application

### `src.playstore_fraud.detector`

The core module containing the `PlayStoreFraudDetector` class that orchestrates the fraud detection process.

**Key features:**
- LLM integration for fraud analysis
- App data preprocessing
- Result validation and formatting
- Sequential workflow management

### `src.playstore_fraud.api.playstore_client`

Module for interacting with the Google Play Store to fetch app data.

**Key features:**
- App search functionality
- App details retrieval
- Permissions and reviews fetching
- Data formatting and serialization

## Utility Modules

### `src.playstore_fraud.utils.io_utils`

Utilities for file I/O operations.

**Key functions:**
- `load_json_data()`: Loads data from JSON files
- `save_results()`: Saves analysis results to JSON files
- `ensure_directory_exists()`: Creates directories if they don't exist

### `src.playstore_fraud.utils.metrics`

Utilities for calculating performance metrics.

**Key functions:**
- `calculate_performance_metrics()`: Calculates metrics like accuracy, precision, recall

### `src.playstore_fraud.config.logging_config`

Configuration for the logging system.

**Key functions:**
- `setup_logging()`: Configures and returns a logger instance

## Directory Structure

```
src/
└── playstore_fraud/
    ├── __init__.py
    ├── detector.py         # Main detector class
    ├── api/
    │   ├── __init__.py
    │   └── playstore_client.py  # Google Play Store API client
    ├── config/
    │   ├── __init__.py
    │   └── logging_config.py    # Logging configuration
    └── utils/
        ├── __init__.py
        ├── io_utils.py          # I/O utility functions
        └── metrics.py           # Metrics calculation functions
```

## Class Relationships

- `main.py` uses `PlayStoreFraudDetector` to run the fraud detection workflow
- `PlayStoreFraudDetector` uses `PlayStoreClient` to fetch app data
- Both modules use utilities from `io_utils` and `logging_config`
- `PlayStoreFraudDetector` processes data through a sequential pipeline:
  1. Data collection (via PlayStoreClient)
  2. Data preprocessing
  3. LLM analysis
  4. Results storage

## Extensibility

The modular design allows for easy extension:

1. **New Data Sources**: Add new clients in the `api/` directory
2. **New Analysis Methods**: Extend the detector or add new detector classes
3. **Custom Metrics**: Add new metrics functions in `metrics.py`
4. **Additional Output Formats**: Extend the I/O utilities for different formats
