# PlayStore Fraud Detection System

A system for automated detection of potentially fraudulent or harmful applications on the Google Play Store using rule-based patterns and Large Language Models.

## Overview

The PlayStore Fraud Detection System analyzes mobile applications to identify suspicious patterns including:

- Excessive or dangerous permission requests
- Suspicious developer information
- Fake or manipulated reviews
- Misleading descriptions and claims
- Other fraud indicators

The system combines rule-based detection with advanced LLM-based analysis to provide comprehensive fraud detection with explainable results.

## Features

- **Hybrid Detection**: Combines traditional rule-based detection with LLM-powered analysis
- **Structured Output**: Consistent classification format with explanations
- **Performance Metrics**: Comprehensive evaluation metrics for accuracy assessment
- **Batch Processing**: Support for analyzing multiple apps efficiently
- **Detailed Documentation**: Extensive guides and API references

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key or equivalent LLM API access

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
```

## Quick Start

1. Prepare your app data in JSON format as specified in the [User Guide](docs/user_guide.md#input-data-preparation)

2. Place input files in the `data/input/` directory:
   - `genuine-apps.json` - Known legitimate apps
   - `fraud-apps.json` - Known fraudulent apps

3. Run the analysis:
```bash
python main.py
```

4. Review results in the `data/output/` directory

## Documentation

Full documentation is available in the `docs` directory:

- [Getting Started Guide](docs/getting_started.md) - Quick setup and first steps
- [User Guide](docs/user_guide.md) - Detailed instructions on using the system
- [API Documentation](docs/api_documentation.md) - Technical reference for the system's APIs
- [Architecture Overview](docs/architecture.md) - System design and component information
- [Development Guide](docs/development_guide.md) - Guidelines for contributors
- [Sample Outputs](docs/samples.md) - Example outputs and interpretations
- [Performance Metrics](docs/metrics.md) - Understanding the system's evaluation metrics

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

## Performance

The system calculates comprehensive performance metrics including:

- Accuracy - Overall correctness
- Precision - How many identified frauds are actually fraud
- Recall - How many actual frauds were caught
- F1 Score - Harmonic mean of precision and recall
- False Positive Rate - How many genuine apps were incorrectly flagged
- False Negative Rate - How many fraud apps were missed

See [Performance Metrics](docs/metrics.md) for detailed explanation of each metric.

## Contributing

Please see our [Development Guide](docs/development_guide.md) for information on contributing to this project.
