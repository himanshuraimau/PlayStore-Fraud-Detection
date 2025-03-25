import json
import os
import sys
import logging
import time
from typing import Dict, List, Any, Tuple, Optional

# Import our modular components
from src.playstore_fraud.utils.io_utils import load_json_data, save_results
from src.playstore_fraud.config.logging_config import setup_logging
from src.playstore_fraud.api.playstore_client import PlayStoreClient
from src.playstore_fraud.analysis.app_analyzer import preprocess_app_data
from src.playstore_fraud.analysis.llm_analyzer import LLMAnalyzer

# Setup logging
logger = setup_logging('FraudDetectionSystem')

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
        self.llm_analyzer = LLMAnalyzer(api_key, model_name)
        self.playstore_client = None  # Initialize only when needed
        logger.info(f"Fraud Detection System initialized with {model_name}")
    
    def load_app_data(self, file_path: str = "data/input/input.json") -> List[Dict]:
        """
        Load app data from a JSON file
        
        Args:
            file_path: Path to the JSON file with app data
            
        Returns:
            List of app data dictionaries
        """
        try:
            full_path = os.path.join(os.getcwd(), file_path)
            if not os.path.exists(full_path):
                logger.error(f"File not found: {full_path}")
                return []
                
            logger.info(f"Loading app data from {full_path}")
            data = load_json_data(full_path)
            logger.info(f"Loaded {len(data)} apps from {file_path}")
            return data
        except Exception as e:
            logger.error(f"Error loading app data: {str(e)}")
            return []

    def analyze_app(self, app_data: Dict) -> Dict:
        """
        Analyze a single app
        
        Args:
            app_data: App data to analyze
            
        Returns:
            Analysis result in the required format
        """
        try:
            # Preprocess the app data
            processed_data = preprocess_app_data(app_data)
            
            # Use the LLM analyzer to get fraud assessment
            result = self.llm_analyzer.analyze_app(processed_data)
            
            logger.info(f"Analysis complete for {processed_data['app_id']}: {result['type']}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing app {app_data.get('appId', 'unknown')}: {str(e)}")
            return {
                "type": "suspected",
                "reason": "Error during analysis. Manual review recommended."
            }
    
    def batch_analyze(self, apps_data: List[Dict] = None, file_path: str = None) -> List[Dict]:
        """
        Analyze multiple apps
        
        Args:
            apps_data: List of app data to analyze or None to load from file
            file_path: Path to JSON file with app data (if apps_data is None)
            
        Returns:
            List of analysis results
        """
        if apps_data is None:
            if file_path is None:
                file_path = "data/input/input.json"
            apps_data = self.load_app_data(file_path)
            
        if not apps_data:
            logger.error("No app data available for analysis")
            return []
            
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
    
    def sequential_workflow(self, query: str, top_n: int = 5):
        """
        Executes a clear sequential workflow:
        1. First uses PlayStoreClient to scrape data and save to input.json
        2. Then loads that data and performs fraud detection analysis
        
        Args:
            query: Search query for app scraping
            top_n: Number of apps to scrape and analyze
            
        Returns:
            Analysis results
        """
        logger.info(f"Starting sequential workflow for query: '{query}'")
        
        # STEP 1: Data Collection
        logger.info("====== STEP 1: SCRAPING DATA ======")
        self.playstore_client = PlayStoreClient(query=query, top_n=top_n)
        apps_data = self.playstore_client.fetch_all_apps()
        
        # Check if we found any apps
        if not apps_data:
            logger.error(f"No apps found for query '{query}'. Please try a different search term.")
            return []
            
        input_path = "data/input/input.json"
        self.playstore_client.save_to_json(input_path)
        logger.info(f"Data collection complete. {len(apps_data)} apps saved to {input_path}")
        
        # Add a small delay to ensure file is completely written
        time.sleep(2)
        
        # STEP 2: Fraud Detection
        logger.info("====== STEP 2: PERFORMING FRAUD DETECTION ======")
        # Load fresh data from the file to ensure we're using exactly what was saved
        logger.info(f"Loading saved data from {input_path}")
        results = self.batch_analyze(file_path=input_path)
        
        # Save results
        output_path = "data/output/analysis_results.json"
        save_results(results, output_path)
        logger.info(f"Analysis complete. Results saved to {output_path}")
        
        # Print summary
        fraud_count = sum(1 for r in results if r.get("type") == "fraud")
        suspected_count = sum(1 for r in results if r.get("type") == "suspected")
        genuine_count = sum(1 for r in results if r.get("type") == "genuine")
        
        logger.info("====== WORKFLOW COMPLETE ======")
        logger.info(f"Summary of {len(results)} apps analyzed:")
        logger.info(f"- Fraud: {fraud_count}")
        logger.info(f"- Suspected: {suspected_count}")
        logger.info(f"- Genuine: {genuine_count}")
        
        return results

# Add a simple command-line interface to run the sequential workflow
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='PlayStore Fraud Detection System')
    parser.add_argument('--api_key', required=True, help='API Key for Google Gemini')
    parser.add_argument('--query', help='Search query for Play Store (if not provided, will prompt for input)')
    parser.add_argument('--top_n', type=int, help='Number of apps to analyze')
    parser.add_argument('--model', default="gemini-2.0-flash", help='LLM model name')
    
    args = parser.parse_args()
    
    # If query not provided, ask user for input
    if not args.query:
        from src.playstore_fraud.api.playstore_client import PlayStoreClient
        
        # Reuse the query input function from PlayStoreClient
        def get_user_query():
            """Ask user for app category to query"""
            print("Welcome to PlayStore Fraud Detection System")
            print("-" * 40)
            print("What type of apps would you like to analyze for potential fraud?")
            print("Examples: business, finance, games, social, education, etc.")
            query = input("Enter app category/query: ").strip()
            
            if not query:
                print("Using default query 'finance'")
                return "finance"
            
            # Ask for number of apps to fetch
            try:
                top_n = int(input("How many apps would you like to analyze? [5]: ") or "5")
            except ValueError:
                print("Invalid input. Using default (5 apps)")
                top_n = 5
                
            return query, top_n
        
        # Get user input
        query_input = get_user_query()
        
        # Check if we got a tuple (with all parameters) or just a string (query only)
        if isinstance(query_input, tuple):
            query, top_n = query_input
        else:
            query, top_n = query_input, 5
    else:
        query = args.query
        top_n = args.top_n or 5
    
    # Create detector and run sequential workflow
    detector = PlayStoreFraudDetector(api_key=args.api_key, model_name=args.model)
    results = detector.sequential_workflow(query=query, top_n=top_n)
    
    print(f"\nAnalysis complete! Checked {len(results)} apps.")
    print(f"Results saved to data/output/analysis_results.json")