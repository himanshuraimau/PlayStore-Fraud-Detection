# API Documentation

This document provides detailed information about the classes and methods in the PlayStore Fraud Detection System.

## Table of Contents

- [PlayStoreFraudDetector](#playstorefranddetector)
- [PlayStoreClient](#playstoreclient)
- [Utility Functions](#utility-functions)

---

## PlayStoreFraudDetector

The core class responsible for app analysis and fraud detection.

### Constructor

```python
PlayStoreFraudDetector(api_key: str, model_name: str = "gemini-2.0-flash")
```

**Parameters:**
- `api_key` (str): API key for Google Gemini or other LLM
- `model_name` (str, optional): Name of the model to use. Defaults to "gemini-2.0-flash"

**Example:**
```python
detector = PlayStoreFraudDetector(api_key="your_gemini_api_key")
```

### Methods

#### `initialize_llm()`

Configures the LLM client with the provided API key.

**Returns:** None

---

#### `preprocess_app_data(app_data: Dict) -> Dict`

Preprocesses app data for analysis.

**Parameters:**
- `app_data` (Dict): Raw app data from JSON files

**Returns:**
- Dict: Processed app data with extracted features

**Example:**
```python
processed_data = detector.preprocess_app_data(app_data)
```

---

#### `analyze_app(app_data: Dict) -> Dict`

Analyzes a single app using LLM.

**Parameters:**
- `app_data` (Dict): App data to analyze

**Returns:**
- Dict: Analysis result in the specified format: 
  ```json
  {
    "type": "fraud"|"genuine"|"suspected",
    "reason": "Concise explanation"
  }
  ```

**Example:**
```python
result = detector.analyze_app(app_data)
print(f"App is classified as: {result['type']}")
print(f"Reason: {result['reason']}")
```

---

#### `batch_analyze(apps_data: List[Dict]) -> List[Dict]`

Analyzes multiple apps.

**Parameters:**
- `apps_data` (List[Dict]): List of app data to analyze

**Returns:**
- List[Dict]: List of analysis results

**Example:**
```python
results = detector.batch_analyze(app_list)
```

---

#### `_process_reviews(reviews: List[Dict]) -> Dict`

Process and analyze app reviews.

**Parameters:**
- `reviews` (List[Dict]): List of review objects

**Returns:**
- Dict: Analysis of reviews with metrics and suspicious patterns

---

#### `_count_dangerous_permissions(app_data: Dict) -> Dict`

Count and analyze dangerous permissions.

**Parameters:**
- `app_data` (Dict): App data with permissions list

**Returns:**
- Dict: Permission analysis with counts and ratios

---

#### `_analyze_developer_history(developer_data: Dict) -> Dict`

Analyze developer information for suspicious patterns.

**Parameters:**
- `developer_data` (Dict): Developer data

**Returns:**
- Dict: Developer analysis results

---

#### `_extract_suspicious_indicators(app_data: Dict) -> Dict`

Extract potential indicators of suspicious activity.

**Parameters:**
- `app_data` (Dict): App data

**Returns:**
- Dict: Suspicious indicators found in the app data

---

#### `generate_llm_prompt(app_data: Dict) -> str`

Create a prompt for the LLM based on app data.

**Parameters:**
- `app_data` (Dict): Processed app data

**Returns:**
- str: Formatted prompt string

---

#### `_validate_result_format(result: Dict) -> bool`

Validate that the result matches the required format.

**Parameters:**
- `result` (Dict): Result from LLM

**Returns:**
- bool: True if format is valid, False otherwise

---

## PlayStoreClient

Client for interacting with the Google Play Store API.

### Constructor

```python
PlayStoreClient(api_key: Optional[str] = None)
```

**Parameters:**
- `api_key` (str, optional): Optional API key for Google Play Store API

**Example:**
```python
client = PlayStoreClient()
```

### Methods

#### `get_app_details(app_id: str) -> Dict`

Fetch app details from Play Store.

**Parameters:**
- `app_id` (str): App ID (package name) to fetch

**Returns:**
- Dict: App details as dictionary

**Example:**
```python
app_details = client.get_app_details("com.example.app")
```

---

#### `get_app_reviews(app_id: str, count: int = 100) -> List[Dict]`

Fetch app reviews from Play Store.

**Parameters:**
- `app_id` (str): App ID to fetch reviews for
- `count` (int, optional): Number of reviews to fetch. Defaults to 100.

**Returns:**
- List[Dict]: List of reviews

**Example:**
```python
reviews = client.get_app_reviews("com.example.app", count=50)
```

---

#### `get_developer_apps(developer_id: str) -> List[Dict]`

Fetch all apps by a specific developer.

**Parameters:**
- `developer_id` (str): Developer ID to fetch apps for

**Returns:**
- List[Dict]: List of apps by the developer

**Example:**
```python
developer_apps = client.get_developer_apps("ExampleDeveloper")
```

---

## Utility Functions

### IO Utilities

Located in `src.playstore_fraud.utils.io_utils`

#### `load_json_data(file_path: str) -> List[Dict]`

Load app data from JSON file.

**Parameters:**
- `file_path` (str): Path to JSON file

**Returns:**
- List[Dict]: Loaded data as list of dictionaries

**Example:**
```python
from src.playstore_fraud.utils.io_utils import load_json_data

apps = load_json_data('data/input/genuine-apps.json')
```

---

#### `save_results(results: List[Dict], output_file: str)`

Save analysis results to JSON file.

**Parameters:**
- `results` (List[Dict]): Results to save
- `output_file` (str): Path to save to

**Example:**
```python
from src.playstore_fraud.utils.io_utils import save_results

save_results(analysis_results, 'data/output/results.json')
```

---

### Metrics Utilities

Located in `src.playstore_fraud.utils.metrics`

#### `calculate_performance_metrics(true_labels: List[int], pred_labels: List[int]) -> Dict`

Calculate performance metrics for fraud detection.

**Parameters:**
- `true_labels` (List[int]): List of true labels (0 for genuine, 1 for fraud)
- `pred_labels` (List[int]): List of predicted labels (0 for genuine, 1 for fraud/suspected)

**Returns:**
- Dict: Dictionary of metrics

**Example:**
```python
from src.playstore_fraud.utils.metrics import calculate_performance_metrics

metrics = calculate_performance_metrics(true_labels, predicted_labels)
print(f"Accuracy: {metrics['accuracy']}")
print(f"F1 Score: {metrics['f1_score']}")
```
