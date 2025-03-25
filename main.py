"""
PlayStore Fraud Detection - Main Entry Point

This script runs the sequential fraud detection workflow that:
1. Scrapes app data from Google Play Store using PlayStoreClient
2. Saves the data to input.json
3. Loads this data for fraud analysis
4. Saves analysis results to output file
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.playstore_fraud.detector import PlayStoreFraudDetector
from src.playstore_fraud.config.logging_config import setup_logging
from src.playstore_fraud.utils.io_utils import ensure_directory_exists
from src.playstore_fraud.utils.cli_utils import get_user_query, parse_args, display_summary

# Setup basic logging
logger = setup_logging('FraudDetectionSystem')

def main():
    """Main entry point for the PlayStore Fraud Detection System."""
    # Create necessary directories
    ensure_directory_exists('data/input')
    ensure_directory_exists('data/output')
    
    # Parse arguments
    args = parse_args()
    
    # ALWAYS prompt for app type unless --no-prompt is explicitly specified
    if args.no_prompt:
        query = args.query or "finance"
        top_n = args.top_n or 5
        print(f"Using query: {query} with {top_n} apps (--no-prompt specified)")
    else:
        # Always ask for input, even if query was provided in command line
        query_input = get_user_query()
        
        # Check if we got a tuple (with all parameters) or just a string (query only)
        if isinstance(query_input, tuple):
            query, top_n = query_input
        else:
            query = query_input
            top_n = args.top_n or 5
    
    try:
        # Initialize the detector
        detector = PlayStoreFraudDetector(api_key=args.api_key, model_name=args.model)
        
        # Run sequential workflow or skip scraping if flagged
        if args.skip_scraping:
            logger.info("Skipping scraping, using existing data from input.json")
            input_path = "data/input/input.json"
            
            # Check if input file exists
            if not Path(input_path).exists():
                logger.error(f"Input file {input_path} not found. Cannot skip scraping.")
                return 1
                
            results = detector.batch_analyze(file_path=input_path)
            
            # Save results
            output_path = "data/output/analysis_results.json"
            from src.playstore_fraud.utils.io_utils import save_results
            save_results(results, output_path)
            logger.info(f"Analysis complete. Results saved to {output_path}")
        else:
            # Run the full sequential workflow
            logger.info(f"Running full scraping and analysis workflow for '{query}'")
            results = detector.sequential_workflow(query=query, top_n=top_n)
            
            # Check if we got any results
            if not results:
                print("\n⚠️ No apps were found for your search query.")
                print("Please try again with a different search term or check your spelling.")
                return 1
        
        # Display summary of results
        display_summary(results)
        
        return 0
    
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully...")
        return 0
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        print(f"\n⚠️ Error: {str(e)}")
        print("If you're searching for apps, try a different query or check spelling.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
