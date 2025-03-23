import json
import os
import sys
import logging
from typing import Dict, List, Any, Tuple, Optional
import google.generativeai as genai # type: ignore

# Fix the import paths to use the correct module structure
from src.playstore_fraud.utils.io_utils import load_json_data, save_results
from src.playstore_fraud.config.logging_config import setup_logging
from src.playstore_fraud.api.playstore_client import PlayStoreClient

# Setup logging
logger = setup_logging('FraudDetectionSystem')

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

class PlayStoreFraudDetector:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        """
        Initialize the fraud detection system.
        
        Args:
            api_key: API key for Google Gemini or other LLM
            model_name: Name of the model to use
        """
        self.api_key = api_key
        self.model_name = model_name
        self.initialize_llm()
        self.playstore_client = PlayStoreClient()
        logger.info(f"Fraud Detection System initialized with {model_name}")
        
    def initialize_llm(self):
        """Configure the LLM client"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logger.info("LLM configured successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            sys.exit(1)

    def preprocess_app_data(self, app_data: Dict) -> Dict:
        """
        Preprocess app data for analysis
        
        Args:
            app_data: App data from JSON files
            
        Returns:
            Processed app data with extracted features
        """
        processed_data = {
            "app_id": app_data.get("appId", "unknown"),
            "title": app_data.get("title", ""),
            "description": app_data.get("description", "")[:1000] if app_data.get("description") else "",
            "category": app_data.get("category", ""),
            "price": app_data.get("price", 0),
            "developer": app_data.get("developer", {}),
            "content_rating": app_data.get("contentRating", ""),
            "reviews": self._process_reviews(app_data.get("reviews", [])),
            "permissions": app_data.get("permissions", []),
            "suspicious_indicators": self._extract_suspicious_indicators(app_data)
        }
        
        logger.info(f"Preprocessed data for app: {processed_data['app_id']}")
        return processed_data
    
    def _process_reviews(self, reviews: List[Dict]) -> Dict:
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
    
    def _count_dangerous_permissions(self, app_data: Dict) -> Dict:
        """Count and analyze dangerous permissions"""
        permissions = app_data.get("permissions", [])
        dangerous_count = sum(1 for p in permissions if p in DANGEROUS_PERMISSIONS)
        
        result = {
            "total": len(permissions),
            "dangerous_count": dangerous_count,
            "dangerous_ratio": dangerous_count / len(permissions) if len(permissions) > 0 else 0
        }
        
        # Add specific dangerous permissions found
        result["dangerous_found"] = [p for p in permissions if p in DANGEROUS_PERMISSIONS]
        
        return result
    
    def _analyze_developer_history(self, developer_data: Dict) -> Dict:
        """Analyze developer information for suspicious patterns"""
        result = {}
        
        # Check for missing critical information
        if not developer_data.get("email"):
            result["missing_contact_email"] = True
            
        if not developer_data.get("website"):
            result["missing_website"] = True
            
        if not developer_data.get("privacyPolicy"):
            result["missing_privacy_policy"] = True
            
        # Optionally fetch developer's other apps using the PlayStore API
        # This would be implemented with real API integration
        developer_id = developer_data.get("id")
        if developer_id:
            try:
                # Mock implementation - in a real system, this would call the API
                developer_apps = self.playstore_client.get_developer_apps(developer_id)
                result["app_count"] = len(developer_apps)
                result["new_developer"] = result["app_count"] < 3
            except Exception as e:
                logger.warning(f"Failed to get developer history: {str(e)}")
                result["developer_history_available"] = False
        
        return result

    def _extract_suspicious_indicators(self, app_data: Dict) -> Dict:
        """Extract potential indicators of suspicious activity"""
        indicators = {}
        
        # Analyze permissions
        permission_analysis = self._count_dangerous_permissions(app_data)
        indicators["dangerous_permissions"] = permission_analysis
        
        # If dangerous permissions ratio is high, flag it
        if permission_analysis["dangerous_ratio"] > 0.4:
            indicators["excessive_dangerous_permissions"] = True
            
        # Developer analysis
        developer_analysis = self._analyze_developer_history(app_data.get("developer", {}))
        indicators["developer_issues"] = developer_analysis
        
        # Price analysis
        if app_data.get("price", 0) > 0 and app_data.get("category") == "Finance":
            indicators["paid_finance_app"] = True
            
        # Add more indicators based on patterns identified
        
        return indicators

    def generate_llm_prompt(self, app_data: Dict) -> str:
        """
        Create a prompt for the LLM based on app data
        
        Args:
            app_data: Processed app data
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""
        Analyze this Google Play Store app for potential fraud indicators or harmful behavior.

        App Title: {app_data['title']}
        App Category: {app_data['category']}
        Price: {app_data['price']}
        Content Rating: {app_data['content_rating']}

        Description:
        {app_data['description']}

        Developer Info:
        {json.dumps(app_data['developer'], indent=2)}

        Permissions:
        {json.dumps(app_data['permissions'], indent=2)}

        Review Analysis:
        {json.dumps(app_data['reviews'], indent=2)}

        Suspicious indicators already identified:
        {json.dumps(app_data['suspicious_indicators'], indent=2)}

        Analyze for these common fraud patterns:
        - Misleading descriptions vs. actual functionality
        - Excessive permissions relative to stated purpose
        - Developer with suspicious patterns (new account, no website, etc.)
        - Financial/crypto apps with high fees or vague value propositions
        - Clone apps mimicking popular apps with slight name variations
        - Apps requesting sensitive permissions without clear justification

        Based on this information:
        1. Evaluate the consistency between app description and category
        2. Assess if permissions requested match the stated functionality
        3. Check developer credibility indicators
        4. Identify patterns matching known financial scams or malware
        5. Analyze review patterns for authenticity

        Respond with a JSON object ONLY in this exact format:
        {{
            "type": "fraud" | "genuine" | "suspected",
            "reason": "<concise explanation in less than 300 characters>"
        }}

        Your analysis should be thorough but the output must match the exact format specified.
        """
        return prompt

    def analyze_app(self, app_data: Dict) -> Dict:
        """
        Analyze a single app using LLM
        
        Args:
            app_data: App data to analyze
            
        Returns:
            Analysis result in the required format
        """
        try:
            processed_data = self.preprocess_app_data(app_data)
            prompt = self.generate_llm_prompt(processed_data)
            
            # Call LLM API with structured output
            generation_config = {
                "temperature": 0.2,
                "top_p": 0.8,
                "top_k": 40,
                "response_mime_type": "application/json",
                "candidate_count": 1,
            }
            
            response = self.model.generate_content(
                prompt, 
                generation_config=generation_config
            )
            
            result = json.loads(response.text)
            
            # Validate result format
            if not self._validate_result_format(result):
                logger.warning(f"Invalid result format for app {processed_data['app_id']}, using fallback")
                result = {
                    "type": "suspected",
                    "reason": "Analysis produced invalid format. Manual review recommended."
                }
            
            logger.info(f"Analysis complete for {processed_data['app_id']}: {result['type']}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing app {app_data.get('appId', 'unknown')}: {str(e)}")
            return {
                "type": "suspected",
                "reason": "Error during analysis. Manual review recommended."
            }
    
    def _validate_result_format(self, result: Dict) -> bool:
        """Validate that the result matches the required format"""
        if not isinstance(result, dict):
            return False
            
        if "type" not in result or "reason" not in result:
            return False
            
        if result["type"] not in ["fraud", "genuine", "suspected"]:
            return False
            
        if not isinstance(result["reason"], str) or len(result["reason"]) > 300:
            return False
            
        return True
    
    def batch_analyze(self, apps_data: List[Dict]) -> List[Dict]:
        """
        Analyze multiple apps
        
        Args:
            apps_data: List of app data to analyze
            
        Returns:
            List of analysis results
        """
        results = []
        total = len(apps_data)
        
        for i, app_data in enumerate(apps_data):
            logger.info(f"Processing app {i+1}/{total}: {app_data.get('appId', 'unknown')}")
            result = self.analyze_app(app_data)
            
            # Add app identifier to result
            result["app_id"] = app_data.get("appId", "unknown")
            result["app_title"] = app_data.get("title", "unknown")
            
            results.append(result)
            
        return results