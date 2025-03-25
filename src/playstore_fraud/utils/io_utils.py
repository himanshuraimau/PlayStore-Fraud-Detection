"""
I/O utility functions for the PlayStore Fraud Detection System
"""

import os
import json
import logging
from typing import Dict, List, Any

logger = logging.getLogger('FraudDetectionSystem')

def ensure_directory_exists(directory_path: str) -> None:
    """
    Create directory if it doesn't exist
    
    Args:
        directory_path: Path to directory to create
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.info(f"Created directory: {directory_path}")

def load_json_data(file_path: str) -> Any:
    """
    Load data from JSON file
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Loaded data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded data from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {str(e)}")
        raise

def save_results(data: Any, file_path: str) -> None:
    """
    Save data to JSON file
    
    Args:
        data: Data to save
        file_path: Path to save to
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Results saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving results to {file_path}: {str(e)}")
        raise
