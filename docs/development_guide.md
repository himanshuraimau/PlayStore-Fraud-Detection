# Development Guide

This guide is intended for developers who want to extend or contribute to the PlayStore Fraud Detection System.

## Table of Contents
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Core Components](#core-components)
- [Testing](#testing)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Style](#code-style)
- [Extending the System](#extending-the-system)

## Development Environment Setup

### Prerequisites

- Python 3.9 or higher
- Git
- A code editor (VS Code recommended)
- Google Gemini API key

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/playstore-fraud-detection.git
cd playstore-fraud-detection
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt  # This includes testing packages
```

4. Set up pre-commit hooks:
```bash
pre-commit install
```

5. Configure environment variables:
```bash
cp .env.example .env
# Edit .env file with your API keys
```

## Project Structure

```
playstore-fraud-detection/
│
├── main.py                         # Main execution entry point
├── README.md                       # Project documentation
├── requirements.txt                # Dependencies
│
├── data/                           # Data directory
│   ├── input/                      # Input data files
│   └── output/                     # Analysis results
│
├── src/                            # Source code
│   └── playstore_fraud/            # Main package
│       ├── __init__.py
│       ├── detector.py             # Core detection logic
│       │
│       ├── api/                    # API integration
│       │   ├── __init__.py
│       │   └── playstore_client.py # Play Store API client
│       │
│       ├── config/                 # Configuration
│       │   ├── __init__.py
│       │   └── logging_config.py   # Logging setup
│       │
│       └── utils/                  # Utilities
│           ├── __init__.py
│           ├── io_utils.py         # Input/output utilities
│           └── metrics.py          # Performance metrics calculation
│
├── tests/                          # Test directory
│   ├── __init__.py
│   └── test_detector.py            # Tests for detector
│
└── docs/                           # Documentation
    ├── index.md                    # Documentation home
    ├── getting_started.md          # Quick start guide
    ├── api_documentation.md        # API reference
    └── ...                         # Other documentation
```

## Core Components

### PlayStoreFraudDetector

The central class of the system, responsible for:
- Processing app data
- Detecting suspicious indicators
- Communicating with the LLM
- Generating structured outputs

This class is found in `src/playstore_fraud/detector.py`.

### PlayStoreClient

Handles communication with the Google Play Store. Currently a skeleton implementation but intended for future expansion to fetch app data directly.

This class is found in `src/playstore_fraud/api/playstore_client.py`.

### Utilities

Helper functions for:
- File I/O operations (`io_utils.py`)
- Metrics calculation (`metrics.py`)
- Logging configuration (`logging_config.py`)

## Testing

### Installing Testing Tools

Install the required testing packages:
```bash
# Using pip
pip install pytest pytest-cov

# Using uv
uv add pytest pytest-cov
```

### Running Tests

To run all tests:
```bash
pytest
```

To run specific test files:
```bash
pytest tests/test_detector.py
```

To run with coverage reporting:
```bash
pytest --cov=src tests/
```

### Writing Tests

When adding new features, include corresponding tests in the `tests/` directory. We use pytest as our testing framework.

Example of a test function:

```python
def test_feature_x():
    # Arrange
    test_data = {"key": "value"}
    expected_result = "expected"
    
    # Act
    actual_result = my_function(test_data)
    
    # Assert
    assert actual_result == expected_result
```

## Contributing Guidelines

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Implement your changes
4. Write tests for your changes
5. Update documentation as needed
6. Ensure all tests pass (`pytest`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to your branch (`git push origin feature/amazing-feature`)
9. Create a Pull Request to the main repository

### Commit Message Guidelines

Use clear and descriptive commit messages:
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests

Example:
```
Add permission analysis feature

- Implement dangerous permission detection
- Add permission ratio calculation
- Create tests for permission analysis

Fixes #123
```

## Code Style

We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide with some modifications:

- Line length: 88 characters (compatible with black)
- Use type annotations for function parameters and return values
- Document all public methods and classes with docstrings

### Linting

We use flake8 for linting:
```bash
flake8 src tests
```

### Formatting

We use black for code formatting:
```bash
black src tests
```

## Extending the System

### Adding New Detection Rules

To add new detection rules, modify the `_extract_suspicious_indicators()` method in `detector.py`:

```python
def _extract_suspicious_indicators(self, app_data: Dict) -> Dict:
    indicators = {}
    
    # Existing indicators code...
    
    # Add your new detection rule
    if some_condition(app_data):
        indicators["your_new_indicator"] = True
    
    return indicators
```

### Modifying LLM Prompt Engineering

To change how the system analyzes apps, modify the `generate_llm_prompt()` method in `detector.py`. Be careful to maintain the expected output format.

### Implementing a Real PlayStore Client

To fetch real data from the Play Store, update the `PlayStoreClient` class in `api/playstore_client.py`. Consider using an existing library like `google-play-scraper`.

### Adding New Metrics

To add new performance metrics, modify the `calculate_performance_metrics()` function in `utils/metrics.py`:

```python
def calculate_performance_metrics(true_labels, pred_labels):
    # Existing metrics code...
    
    # Add your new metric
    your_metric = calculate_your_metric(true_labels, pred_labels)
    
    return {
        # Existing metrics...
        "your_metric": your_metric
    }
```
