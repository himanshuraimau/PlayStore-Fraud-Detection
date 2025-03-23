# Getting Started Guide

This guide will help you set up and run the PlayStore Fraud Detection System for the first time.

## Prerequisites

Before you begin, ensure you have:

- Python 3.9 or higher installed
- A Google Gemini API key (obtain from [Google AI Studio](https://ai.google.dev/))
- Basic familiarity with command line operations

## Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/playstore-fraud-detection.git
cd playstore-fraud-detection
```

2. **Set Up a Virtual Environment**

```bash
# Create virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure API Key**

Create a `.env` file in the project root directory:

```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

Replace `your_api_key_here` with your actual Gemini API key.

5. **Create Data Directories**

```bash
mkdir -p data/input data/output
```

## Basic Usage

### Prepare Input Data

Place your input data files in the `data/input` directory:

- `genuine-apps.json` - Known genuine apps for training and testing
- `fraud-apps.json` - Known fraudulent apps for training and testing

For your first run, you can use the sample data files provided in the repository's `sample_data` folder.

### Run the System

```bash
python main.py
```

This will:
1. Load the app data
2. Process a subset of apps (limited to 10 by default)
3. Generate analysis results
4. Calculate and display performance metrics

### Check the Results

After running the system, you can find the results in the `data/output` directory:

- `genuine_analysis_results.json` - Analysis results for genuine apps
- `fraud_analysis_results.json` - Analysis results for fraudulent apps
- `performance_metrics.json` - Detection performance metrics

## Configuration Options

The system provides several configuration options:

- **Sample Limit**: Modify the `SAMPLE_LIMIT` variable in `main.py` to change how many apps are processed
- **Model Selection**: Change the model by modifying the `model_name` parameter in the `PlayStoreFraudDetector` initialization
- **Logging Level**: Adjust logging verbosity in `logging_config.py`

## Next Steps

- Read the [User Guide](user_guide.md) for more detailed usage instructions
- Explore the [Architecture Overview](architecture.md) to understand how the system works
- Look at [Sample Outputs](samples.md) to understand the results

## Troubleshooting

**API Key Issues**
- Ensure your API key is correctly set in the `.env` file
- Verify you have permission to use the Gemini model

**Module Not Found Errors**
- Make sure you're running from the project root directory
- Ensure all dependencies are installed with `pip install -r requirements.txt`

**Memory Issues**
- Reduce the batch size by lowering the `SAMPLE_LIMIT` in `main.py`
