# API Documentation

## PlayStoreFraudDetector

The main class responsible for orchestrating fraud detection.

### Constructor

```python
PlayStoreFraudDetector(api_key: str, model_name: str = "gemini-2.0-flash")
```

- **api_key**: Google Gemini API key
- **model_name**: Name of the Gemini model to use (default: "gemini-2.0-flash")

### Methods

#### `sequential_workflow`

```python
sequential_workflow(query: str, top_n: int = 5) -> List[Dict]
```

Executes a complete workflow:
1. Scrapes app data based on query
2. Saves data to input.json
3. Analyzes data for fraud signals
4. Saves results to analysis_results.json

- **query**: Search query for Google Play Store
- **top_n**: Number of apps to scrape and analyze
- **Returns**: List of analysis results

#### `batch_analyze`

```python
batch_analyze(apps_data: List[Dict] = None, file_path: str = None) -> List[Dict]
```

Analyzes multiple apps for fraud signals.

- **apps_data**: List of app data to analyze (optional)
- **file_path**: Path to JSON file with app data (optional, used if apps_data is None)
- **Returns**: List of analysis results

#### `analyze_app`

```python
analyze_app(app_data: Dict) -> Dict
```

Analyzes a single app using LLM.

- **app_data**: App data to analyze
- **Returns**: Analysis result in the format: `{"type": "fraud"|"genuine"|"suspected", "reason": "explanation"}`

## PlayStoreClient

Client for fetching and processing data from Google Play Store.

### Constructor

```python
PlayStoreClient(query: str = "finance", country: str = "us", lang: str = "en", top_n: int = 5, review_count: int = 5)
```

- **query**: Search query string
- **country**: Country code for the search
- **lang**: Language code for the search
- **top_n**: Number of apps to fetch
- **review_count**: Number of reviews to fetch per app

### Methods

#### `fetch_all_apps`

```python
fetch_all_apps() -> List[Dict]
```

Fetches and processes all apps based on search criteria.

- **Returns**: List of processed app data

#### `save_to_json`

```python
save_to_json(filepath: str = "data/input/input.json") -> None
```

Saves the processed app data to a JSON file.

- **filepath**: Path where the JSON file will be saved

## Utility Functions

### IO Utilities

#### `load_json_data`

```python
load_json_data(file_path: str) -> Any
```

Loads data from a JSON file.

- **file_path**: Path to the JSON file
- **Returns**: Loaded JSON data

#### `save_results`

```python
save_results(data: Any, file_path: str) -> None
```

Saves data to a JSON file.

- **data**: Data to save
- **file_path**: Path where to save the data

#### `ensure_directory_exists`

```python
ensure_directory_exists(directory_path: str) -> None
```

Creates a directory if it doesn't exist.

- **directory_path**: Path to directory to create

### Metrics Utilities

#### `calculate_performance_metrics`

```python
calculate_performance_metrics(true_labels: List[int], pred_labels: List[int]) -> Dict
```

Calculates performance metrics for fraud detection.

- **true_labels**: List of true labels (0 for genuine, 1 for fraud)
- **pred_labels**: List of predicted labels (0 for genuine, 1 for fraud/suspected)
- **Returns**: Dictionary of metrics (accuracy, precision, recall, etc.)
