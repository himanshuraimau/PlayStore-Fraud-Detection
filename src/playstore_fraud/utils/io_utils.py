import json
import logging
from typing import Dict, List

logger = logging.getLogger('FraudDetectionSystem')

def load_json_data(file_path: str) -> List[Dict]:
    """Load app data from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.info(f"Loaded {len(data)} records from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {str(e)}")
        return []

def save_results(results: List[Dict], output_file: str):
    """Save analysis results to JSON file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(results, file, indent=2)
        logger.info(f"Results saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving results to {output_file}: {str(e)}")
