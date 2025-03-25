# PlayStore Fraud Detection System

## Overview

The PlayStore Fraud Detection System is a comprehensive tool designed to identify potentially fraudulent or malicious applications on the Google Play Store. Using a combination of data scraping, analysis, and machine learning, the system evaluates apps based on multiple risk factors and provides actionable insights.

## Key Features

- **Automated App Scraping**: Fetches app data from Google Play Store based on search queries
- **Comprehensive Analysis**: Evaluates apps based on permissions, developer info, reviews, and descriptions
- **AI-Powered Detection**: Uses Google's Gemini LLM models to analyze for fraud patterns
- **Batch Processing**: Ability to analyze multiple apps in sequence
- **Detailed Reporting**: Generates comprehensive reports of findings

## Documentation Contents

- [Installation Guide](installation.md) - Setup and dependencies
- [Usage Guide](usage.md) - How to use the system
- [Architecture Overview](architecture.md) - System design and components
- [API Documentation](api_docs.md) - Documentation for key modules and classes

## Project Structure

```
/home/himanshu/Desktop/PLAYSTORE/
├── data/                  # Data storage directory
│   ├── input/             # Input data (scraped app information)
│   └── output/            # Analysis results
├── docs/                  # Documentation
├── src/                   # Source code
│   └── playstore_fraud/   # Main package
│       ├── api/           # API clients (PlayStore scraping)
│       ├── config/        # Configuration files
│       └── utils/         # Utility functions
└── tests/                 # Test files
```

## License

[License information would go here]

## Contributors

[Contributor information would go here]
