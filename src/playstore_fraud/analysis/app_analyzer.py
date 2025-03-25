"""
App Analysis Module for the PlayStore Fraud Detection System.
Contains functions for analyzing app data and extracting features.
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger('FraudDetectionSystem')

# List of permissions considered dangerous
DANGEROUS_PERMISSIONS = [
    "android.permission.READ_CONTACTS",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.RECORD_AUDIO",
    "android.permission.CAMERA",
    "android.permission.READ_SMS",
    "android.permission.SEND_SMS",
    "android.permission.CALL_PHONE",
    "android.permission.READ_CALL_LOG",
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.GET_ACCOUNTS",
    "android.permission.READ_PHONE_STATE"
]

def extract_permissions(permissions_data: Dict) -> List[str]:
    """Extract permissions list from the structured permissions data"""
    if isinstance(permissions_data, dict) and "list" in permissions_data:
        return permissions_data.get("list", [])
    return []

def process_reviews(reviews: List[Dict]) -> Dict:
    """Process and analyze app reviews"""
    if not reviews:
        return {"available": False}
        
    total_reviews = len(reviews)
    if total_reviews == 0:
        return {"available": False}
        
    # Calculate average rating
    avg_rating = sum(r.get("score", 0) for r in reviews) / total_reviews
    
    # Check for review patterns
    five_star_count = sum(1 for r in reviews if r.get("score") == 5)
    one_star_count = sum(1 for r in reviews if r.get("score") == 1)
    
    # Calculate suspicious patterns
    suspicious_patterns = {}
    if total_reviews > 10:
        if five_star_count / total_reviews > 0.9:
            suspicious_patterns["excessive_five_stars"] = True
        if len(set(r.get("text", "")[:20] for r in reviews)) < total_reviews * 0.5:
            suspicious_patterns["similar_review_texts"] = True
            
    return {
        "available": True,
        "count": total_reviews,
        "average_rating": avg_rating,
        "five_star_percentage": five_star_count / total_reviews if total_reviews > 0 else 0,
        "one_star_percentage": one_star_count / total_reviews if total_reviews > 0 else 0,
        "suspicious_patterns": suspicious_patterns
    }

def count_dangerous_permissions(permissions: List[str]) -> Dict:
    """Count and analyze dangerous permissions"""
    dangerous_count = sum(1 for p in permissions if p in DANGEROUS_PERMISSIONS)
    
    result = {
        "total": len(permissions),
        "dangerous_count": dangerous_count,
        "dangerous_ratio": dangerous_count / len(permissions) if len(permissions) > 0 else 0
    }
    
    # Add specific dangerous permissions found
    result["dangerous_found"] = [p for p in permissions if p in DANGEROUS_PERMISSIONS]
    
    return result

def preprocess_app_data(app_data: Dict) -> Dict:
    """
    Preprocess app data for analysis
    
    Args:
        app_data: App data from JSON files
        
    Returns:
        Processed app data with extracted features
    """
    # Extract permissions
    permissions = extract_permissions(app_data.get("permissions", {}))
    
    # Process app reviews
    reviews_analysis = process_reviews(app_data.get("comments", []))
    
    # Analyze permissions
    permission_analysis = count_dangerous_permissions(permissions)
    
    # Developer analysis
    developer_data = app_data.get("developer", {})
    developer_issues = {}
    
    # Check for missing critical information
    if not developer_data.get("email"):
        developer_issues["missing_contact_email"] = True
    if not developer_data.get("privacyPolicy"):
        developer_issues["missing_privacy_policy"] = True
        
    # Extract suspicious indicators
    suspicious_indicators = {
        "dangerous_permissions": permission_analysis,
        "developer_issues": developer_issues
    }
    
    # If dangerous permissions ratio is high, flag it
    if permission_analysis["dangerous_ratio"] > 0.4:
        suspicious_indicators["excessive_dangerous_permissions"] = True
            
    # Price analysis
    if app_data.get("price", 0) > 0 and app_data.get("category") == "Finance":
        suspicious_indicators["paid_finance_app"] = True
    
    processed_data = {
        "app_id": app_data.get("appId", "unknown"),
        "title": app_data.get("title", ""),
        "description": app_data.get("description", "")[:1000] if app_data.get("description") else "",
        "category": app_data.get("category", ""),
        "price": app_data.get("price", 0),
        "developer": developer_data,
        "content_rating": app_data.get("contentRating", ""),
        "reviews": reviews_analysis,
        "permissions": permissions,
        "suspicious_indicators": suspicious_indicators
    }
    
    logger.info(f"Preprocessed data for app: {processed_data['app_id']}")
    return processed_data
