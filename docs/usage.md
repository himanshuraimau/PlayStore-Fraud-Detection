# Usage Guide

## Basic Usage

The PlayStore Fraud Detection System can be used through the command line interface. The basic command structure is:

```bash
python main.py [options]
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--api_key` | Google Gemini API Key | GEMINI_API_KEY environment variable |
| `--query` | Search query for Play Store | "finance" |
| `--top_n` | Number of apps to analyze | 5 |
| `--model` | LLM model name | "gemini-2.0-flash" |
| `--skip_scraping` | Skip scraping and use existing input.json | False |

## Examples

### Basic Analysis

To analyze the top 5 finance apps:

```bash
python main.py --api_key YOUR_API_KEY --query finance --top_n 5
```

### Using Different Categories

To analyze gaming apps:

```bash
python main.py --api_key YOUR_API_KEY --query games --top_n 10
```

### Using Existing Data

If you've already scraped app data and want to re-analyze it:

```bash
python main.py --api_key YOUR_API_KEY --skip_scraping
```

### Using a Different Model

To specify a different Gemini model:

```bash
python main.py --api_key YOUR_API_KEY --model gemini-2.0-pro
```

## Understanding Results

After running the analysis, results are saved to `data/output/analysis_results.json`. Each app is classified as one of:

- **fraud**: High confidence that the app is fraudulent
- **suspected**: Some suspicious indicators found
- **genuine**: No significant fraud indicators detected

Each result includes:
- App ID and title
- Classification type
- Reason for the classification

Example result:
```json
{
  "type": "suspected",
  "reason": "Requests excessive permissions including SMS and contacts access for a simple finance calculator app",
  "app_id": "com.example.financeapp",
  "app_title": "Quick Finance Calculator"
}
```

## Workflow Diagram

```
[User Input] → [Scrape Apps] → [Preprocess Data] → [AI Analysis] → [Results Output]
```

## Tips for Better Results

- Be specific with search queries to narrow the focus
- Start with a small number of apps (5-10) to get faster results
- For financial fraud detection, search terms like "investment", "banking", "crypto", etc. yield more relevant results
- Use different models for different levels of analysis depth
