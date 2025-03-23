import os
import sys
import json
from dotenv import load_dotenv
import logging
from typing import Dict, List

from src.playstore_fraud.detector import PlayStoreFraudDetector
from src.playstore_fraud.utils.io_utils import load_json_data, save_results
from src.playstore_fraud.utils.metrics import calculate_performance_metrics

load_dotenv()

def main():
    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logging.error("GEMINI_API_KEY environment variable not set")
        sys.exit(1)
    
    # Initialize detector
    detector = PlayStoreFraudDetector(api_key)
    
    # Set limit to process only 10 entries from each dataset
    SAMPLE_LIMIT = 10
    logging.info(f"Running with sample limit of {SAMPLE_LIMIT} entries per dataset")
    
    # Load data from provided JSON files
    genuine_apps = load_json_data('data/input/genuine-apps.json')
    fraud_apps = load_json_data('data/input/fraud-apps.json')
    
    genuine_results = []
    fraud_results = []
    
    # Analyze a limited subset of apps from the provided datasets
    if genuine_apps:
        # Take only the first SAMPLE_LIMIT entries
        sample_genuine_apps = genuine_apps[:SAMPLE_LIMIT]
        logging.info(f"Processing {len(sample_genuine_apps)} out of {len(genuine_apps)} genuine apps")
        genuine_results = detector.batch_analyze(sample_genuine_apps)
        save_results(genuine_results, 'data/output/genuine_analysis_results.json')
    else:
        logging.warning("No genuine app data available for analysis")
    
    if fraud_apps:
        # Take only the first SAMPLE_LIMIT entries
        sample_fraud_apps = fraud_apps[:SAMPLE_LIMIT]
        logging.info(f"Processing {len(sample_fraud_apps)} out of {len(fraud_apps)} fraud apps")
        fraud_results = detector.batch_analyze(sample_fraud_apps)
        save_results(fraud_results, 'data/output/fraud_analysis_results.json')
    else:
        logging.warning("No fraud app data available for analysis")
    
    # Calculate and display performance metrics
    if genuine_results and fraud_results:
        # True labels: genuine_apps are genuine (label 0), fraud_apps are fraud (label 1)
        true_genuine_labels = [0] * len(genuine_results)
        true_fraud_labels = [1] * len(fraud_results)
        
        # Predicted labels: convert type to numerical (0 for genuine, 1 for fraud/suspected)
        pred_genuine_labels = [0 if r['type'] == 'genuine' else 1 for r in genuine_results]
        pred_fraud_labels = [0 if r['type'] == 'genuine' else 1 for r in fraud_results]
        
        # Calculate metrics
        metrics = calculate_performance_metrics(
            true_labels=true_genuine_labels + true_fraud_labels,
            pred_labels=pred_genuine_labels + pred_fraud_labels
        )
        
        # Display metrics
        print("\nPerformance Metrics:")
        print(f"Accuracy: {metrics['accuracy']:.3f}")
        print(f"Precision: {metrics['precision']:.3f}")
        print(f"Recall: {metrics['recall']:.3f}")
        print(f"F1 Score: {metrics['f1_score']:.3f}")
        print(f"False Positive Rate: {metrics['false_positive_rate']:.3f}")
        print(f"False Negative Rate: {metrics['false_negative_rate']:.3f}")
        
        # Save metrics
        save_results(metrics, 'data/output/performance_metrics.json')

if __name__ == "__main__":
    main()
