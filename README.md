# PlayStore Fraud Detection System

A system for automated detection of potentially fraudulent or harmful applications on the Google Play Store using rule-based patterns and Large Language Models.

## Overview

The PlayStore Fraud Detection System analyzes mobile applications to identify suspicious patterns including:

- Excessive or dangerous permission requests
- Suspicious developer information
- Fake or manipulated reviews
- Misleading descriptions and claims
- Other fraud indicators

The system combines rule-based detection with advanced LLM-based analysis (using Google's Gemini models) to provide comprehensive fraud detection with explainable results.

## Features

- **Data Collection**: Automated scraping of app data from Google Play Store
- **Hybrid Detection**: Combines traditional rule-based detection with LLM-powered analysis
- **Structured Output**: Consistent classification format with explanations
- **Performance Metrics**: Comprehensive evaluation metrics for accuracy assessment
- **Batch Processing**: Support for analyzing multiple apps efficiently
- **Detailed Documentation**: Extensive guides and API references

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (for LLM analysis)
- Required Python packages (see requirements.txt)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/playstore-fraud-detection
cd playstore-fraud-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
```bash
# Create a .env file in the project root
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Or set environment variable
export GEMINI_API_KEY=your_api_key_here
```

## Quick Start

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--api_key` | Google Gemini API Key | GEMINI_API_KEY environment variable |
| `--query` | Search query for Play Store | "finance" |
| `--top_n` | Number of apps to analyze | 5 |
| `--model` | LLM model name | "gemini-2.0-flash" |
| `--skip_scraping` | Skip scraping and use existing input.json | False |

### Examples

To analyze the top 5 finance apps:
```bash
python main.py --api_key YOUR_API_KEY --query finance --top_n 5
```

To analyze gaming apps:
```bash
python main.py --api_key YOUR_API_KEY --query games --top_n 10
```

To use existing data for reanalysis:
```bash
python main.py --api_key YOUR_API_KEY --skip_scraping
```

## System Architecture

```
┌────────────────────┐     ┌────────────────────┐     ┌────────────────────┐
│                    │     │                    │     │                    │
│  PlayStoreClient   │──-->│   Preprocessing    │──-->│  LLM Analysis      │
│  (Data Collection) │     │   (Feature         │     │  (Fraud Detection) │
│                    │     │    Extraction)     │     │                    │
└────────────────────┘     └────────────────────┘     └────────────────────┘
                                                                │
                                                                ▼
                                                      ┌────────────────────┐
                                                      │                    │
                                                      │  Result Analysis   │
                                                      │  & Reporting       │
                                                      │                    │
                                                      └────────────────────┘
```

## Sample Results

The system produces structured outputs for each analyzed app:

```json
{
  "app_id": "com.example.app",
  "app_title": "Example App",
  "type": "fraud|genuine|suspected",
  "reason": "Concise explanation of the classification"
}
```

## Directory Structure

```
/home/himanshu/Desktop/PLAYSTORE/
├── data/                  # Data storage directory
│   ├── input/             # Input data (scraped app information)
│   └── output/            # Analysis results
├── docs/                  # Documentation
│   ├── README.md          # Documentation index
│   ├── installation.md    # Installation guide
│   ├── usage.md           # Usage guide
│   ├── architecture.md    # Architecture documentation
│   ├── api_docs.md        # API documentation
│   └── modules.md         # Module documentation
├── src/                   # Source code
│   └── playstore_fraud/   # Main package
│       ├── api/           # API clients (PlayStore scraping)
│       ├── config/        # Configuration files
│       └── utils/         # Utility functions
├── tests/                 # Test files
├── main.py                # Main entry point
└── README.md              # This file
```

## Performance Metrics

The system calculates comprehensive performance metrics including:

- **Accuracy**: Overall correctness of classifications
- **Precision**: How many identified frauds are actually fraud
- **Recall**: How many actual frauds were caught
- **F1 Score**: Harmonic mean of precision and recall
- **False Positive Rate**: How many genuine apps were incorrectly flagged
- **False Negative Rate**: How many fraud apps were missed

## Documentation

Full documentation is available in the `docs` directory:

- [Documentation Home](docs/README.md) - Overview and index
- [Installation Guide](docs/installation.md) - Setup and dependencies
- [Usage Guide](docs/usage.md) - How to use the system
- [Architecture Overview](docs/architecture.md) - System design and components
- [API Documentation](docs/api_docs.md) - Documentation for key modules and classes
- [Modules Documentation](docs/modules.md) - Detailed module information

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
