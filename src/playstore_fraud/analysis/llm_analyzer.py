"""
LLM Integration for the PlayStore Fraud Detection System.
Contains functions for interacting with LLMs and processing their responses.
"""

import json
import logging
import sys
from typing import Dict, Any
import google.generativeai as genai # type: ignore

logger = logging.getLogger('FraudDetectionSystem')

class LLMAnalyzer:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        """
        Initialize the LLM analyzer.
        
        Args:
            api_key: API key for Google Gemini or other LLM
            model_name: Name of the model to use
        """
        self.api_key = api_key
        self.model_name = model_name
        self.model = None
        self.initialize_llm()
        
    def initialize_llm(self):
        """Configure the LLM client"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logger.info("LLM configured successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            sys.exit(1)
    
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
            prompt = self.generate_llm_prompt(app_data)
            
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
            if not self.validate_result_format(result):
                logger.warning(f"Invalid result format for app {app_data['app_id']}, using fallback")
                result = {
                    "type": "suspected",
                    "reason": "Analysis produced invalid format. Manual review recommended."
                }
            
            logger.info(f"Analysis complete for {app_data['app_id']}: {result['type']}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing app {app_data.get('app_id', 'unknown')}: {str(e)}")
            return {
                "type": "suspected",
                "reason": "Error during analysis. Manual review recommended."
            }
    
    def validate_result_format(self, result: Dict) -> bool:
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
