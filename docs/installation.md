# Installation Guide

## Prerequisites

Before installing the PlayStore Fraud Detection System, ensure you have the following:

- Python 3.8 or later
- pip package manager
- Google Gemini API key (for AI-powered analysis)

## Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/playstore-fraud-detection.git
cd playstore-fraud-detection
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up API Key

You can either:

- Set the API key as an environment variable:
  ```bash
  # On Windows
  set GEMINI_API_KEY=your_api_key_here
  # On macOS/Linux
  export GEMINI_API_KEY=your_api_key_here
  ```

- Or provide it as a command line argument when running the tool:
  ```bash
  python main.py --api_key your_api_key_here
  ```

### 5. Directory Structure

Ensure the following directories exist (they will be created automatically if missing):

```
data/
├── input/     # For storing scraped app data
└── output/    # For storing analysis results
```

## Troubleshooting

### Common Issues

- **API Key Errors**: Verify that your Google Gemini API key is correctly set and has the proper permissions
- **Import Errors**: Make sure you're running from the project root directory
- **Permission Issues**: Ensure write permissions for the data directories

### Getting Help

If you encounter issues not covered in this guide, please report them on the GitHub issues page.
