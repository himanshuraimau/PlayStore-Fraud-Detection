from typing import Dict, List
import logging

logger = logging.getLogger('FraudDetectionSystem')

def calculate_performance_metrics(true_labels: List[int], pred_labels: List[int]) -> Dict:
    """
    Calculate performance metrics for fraud detection
    
    Args:
        true_labels: List of true labels (0 for genuine, 1 for fraud)
        pred_labels: List of predicted labels (0 for genuine, 1 for fraud/suspected)
        
    Returns:
        Dictionary of metrics
    """
    if len(true_labels) != len(pred_labels):
        logger.error("Label lists must be the same length")
        return {}
        
    if not true_labels:
        logger.error("Label lists cannot be empty")
        return {}
    
    # Calculate confusion matrix
    true_positives = sum(1 for t, p in zip(true_labels, pred_labels) if t == 1 and p == 1)
    false_positives = sum(1 for t, p in zip(true_labels, pred_labels) if t == 0 and p == 1)
    true_negatives = sum(1 for t, p in zip(true_labels, pred_labels) if t == 0 and p == 0)
    false_negatives = sum(1 for t, p in zip(true_labels, pred_labels) if t == 1 and p == 0)
    
    # Calculate metrics
    accuracy = (true_positives + true_negatives) / len(true_labels)
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    false_positive_rate = false_positives / (false_positives + true_negatives) if (false_positives + true_negatives) > 0 else 0
    false_negative_rate = false_negatives / (false_negatives + true_positives) if (false_negatives + true_positives) > 0 else 0
    
    logger.info(f"Performance metrics calculated: Accuracy={accuracy:.3f}, F1={f1_score:.3f}")
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "false_positive_rate": false_positive_rate,
        "false_negative_rate": false_negative_rate,
        "confusion_matrix": {
            "true_positives": true_positives,
            "false_positives": false_positives,
            "true_negatives": true_negatives,
            "false_negatives": false_negatives
        }
    }
