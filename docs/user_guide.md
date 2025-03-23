# User Guide

This guide provides detailed instructions on using the PlayStore Fraud Detection System.

## Table of Contents
- [System Overview](#system-overview)
- [Input Data Preparation](#input-data-preparation)
- [Running the System](#running-the-system)
- [Interpreting Results](#interpreting-results)
- [Configuration Options](#configuration-options)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)

## System Overview

The PlayStore Fraud Detection System analyzes mobile applications to identify potentially fraudulent or harmful apps. It combines:

1. **Rule-based detection**: Looking for specific suspicious patterns
2. **LLM-based analysis**: Using AI to detect more complex fraud indicators
3. **Performance metrics**: Measuring detection accuracy

## Input Data Preparation

### Data Format

The system expects input data in JSON format with the following structure:

```json
[
  {
    "appId": "com.example.app",
    "title": "Example App",
    "description": "App description text",
    "category": "Tools",
    "contentRating": "Everyone",
    "price": 0,
    "developer": {
      "id": "DeveloperName",
      "email": "dev@example.com",
      "website": "https://example.com",
      "privacyPolicy": "https://example.com/privacy"
    },
    "permissions": [
      "android.permission.INTERNET",
      "android.permission.ACCESS_NETWORK_STATE"
    ],
    "reviews": [
      {
        "userName": "User1",
        "score": 5,
        "text": "Great app!"
      }
    ]
  },
  // More app entries...
]
```

### Required Fields

The following fields should be present for effective analysis:

| Field | Description | Importance |
|-------|-------------|------------|
| appId | Unique identifier for the app | Required |
| title | App name | Required |
| description | App description | Required |
| category | App category | Required |
| developer | Developer information | Required |
| permissions | List of permissions | Recommended |
| reviews | User reviews | Recommended |

### Input File Locations

Place input files in the `data/input/` directory:
- `genuine-apps.json` - Known legitimate apps
- `fraud-apps.json` - Known fraudulent apps

## Running the System

### Basic Execution

1. Ensure your environment is set up (see [Getting Started Guide](getting_started.md))
2. Place your input data files in the correct location
3. Run the main script:

```bash
python main.py
```

### Command Line Options

The current version does not support command line arguments. Configuration changes require code modifications.

### Sample Run

A typical execution will produce output similar to:

```
2023-07-15 14:30:21 - FraudDetectionSystem - INFO - Fraud Detection System initialized with gemini-2.0-flash
2023-07-15 14:30:21 - FraudDetectionSystem - INFO - LLM configured successfully
2023-07-15 14:30:21 - FraudDetectionSystem - INFO - Running with sample limit of 10 entries per dataset
2023-07-15 14:30:21 - FraudDetectionSystem - INFO - Loaded 100 records from data/input/genuine-apps.json
2023-07-15 14:30:21 - FraudDetectionSystem - INFO - Processing 10 out of 100 genuine apps
2023-07-15 14:30:22 - FraudDetectionSystem - INFO - Processing app 1/10: com.example.app1
...

Performance Metrics:
Accuracy: 0.850
Precision: 0.889
Recall: 0.800
F1 Score: 0.842
False Positive Rate: 0.100
False Negative Rate: 0.200
```

## Interpreting Results

### Output Files

The system generates these output files in the `data/output/` directory:

1. `genuine_analysis_results.json` - Results for analyzed genuine apps
2. `fraud_analysis_results.json` - Results for analyzed fraud apps
3. `performance_metrics.json` - Detection performance metrics

### Result Format

Each app analysis result has this format:

```json
{
  "app_id": "com.example.app",
  "app_title": "Example App",
  "type": "fraud|genuine|suspected",
  "reason": "Concise explanation of the classification"
}
```

### Classification Categories

- **Genuine**: The app appears legitimate with no significant suspicious indicators
- **Fraud**: The app shows strong signs of being fraudulent or harmful
- **Suspected**: The app has some suspicious indicators but not enough for a definite fraud classification

### Performance Metrics

The metrics file contains:

```json
{
  "accuracy": 0.85,
  "precision": 0.889,
  "recall": 0.8,
  "f1_score": 0.842,
  "false_positive_rate": 0.1,
  "false_negative_rate": 0.2,
  "confusion_matrix": {
    "true_positives": 8,
    "false_positives": 1,
    "true_negatives": 9,
    "false_negatives": 2
  }
}
```

#### Understanding Metrics

- **Accuracy**: Overall correctness (TP+TN)/(TP+TN+FP+FN)
- **Precision**: How many identified frauds are actually fraud (TP/(TP+FP))
- **Recall**: How many actual frauds were caught (TP/(TP+FN))
- **F1 Score**: Harmonic mean of precision and recall
- **False Positive Rate**: How many genuine apps were incorrectly flagged (FP/(FP+TN))
- **False Negative Rate**: How many fraud apps were missed (FN/(FN+TP))

## Configuration Options

### Changing Sample Size

To change how many apps are processed:

1. Open `main.py`
2. Find the `SAMPLE_LIMIT` variable
3. Change the value (default is 10)

```python
# Set limit to process only N entries from each dataset
SAMPLE_LIMIT = 25  # Changed from 10 to 25
```

### LLM Model Selection

To change the LLM model:

1. Open `main.py`
2. Modify the detector initialization:

```python
detector = PlayStoreFraudDetector(api_key, model_name="gemini-1.0-pro")
```

Available models depend on your Google API access.

### Logging Configuration

To change logging verbosity:

1. Open `src/playstore_fraud/config/logging_config.py`
2. Modify the `level` parameter in the call to `setup_logging`

## Advanced Usage

### Using Custom Datasets

You can analyze any app data as long as it follows the required JSON format.

For production use, consider:
1. Creating a pipeline to collect app data from the Play Store
2. Formatting the data according to the required structure
3. Running the system on larger datasets

### Batch Processing

For large datasets, you may want to:

1. Process in smaller batches to avoid memory issues
2. Implement checkpointing to resume interrupted runs
3. Use parallel processing for improved performance

## Troubleshooting

### LLM API Errors

If you see errors related to the LLM API:

- Verify your API key is correct in the `.env` file
- Check if you have access to the specified model
- Ensure you have not exceeded API rate limits
- Check your internet connection

### Input Data Issues

If the system cannot process your input data:

- Validate your JSON files with a JSON validator
- Ensure all required fields are present
- Check for encoding issues (the system expects UTF-8)

### Performance Issues

If the system is running slowly:

- Reduce the `SAMPLE_LIMIT` in `main.py`
- Process larger datasets in smaller batches
- Consider upgrading your hardware for better performance

### Output Format Problems

If the output doesn't match the expected format:

- Check for LLM prompt engineering issues
- Verify the validation logic in `_validate_result_format()`
- Ensure you're using a compatible LLM model
