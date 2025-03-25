"""
CLI utilities for the PlayStore Fraud Detection System.
Contains functions for handling user input and displaying console messages.
"""

import argparse
import os
from typing import Tuple, Union

def get_user_query() -> Union[str, Tuple[str, int]]:
    """Ask user for app category to query"""
    print("\n===== PlayStore Fraud Detection System =====")
    print("=" * 40)
    print("What type of apps would you like to analyze for potential fraud?")
    print("Examples: business, finance, games, social, education, etc.")
    query = input("Enter app category/query: ").strip()
    
    # Check for common misspellings
    if query.lower() == "buisness":
        print("Note: Using 'business' instead of 'buisness' (corrected spelling)")
        query = "business"
    
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

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='PlayStore Fraud Detection System')
    
    # Required argument for API key
    parser.add_argument('--api_key', required=False, help='Google Gemini API Key', 
                        default=os.environ.get('GEMINI_API_KEY'))
    
    # Optional arguments with defaults
    parser.add_argument('--query', help='Search query for Play Store (will still ask for input)')
    parser.add_argument('--top_n', type=int, help='Number of apps to analyze')
    parser.add_argument('--model', default="gemini-2.0-flash", help='LLM model name')
    parser.add_argument('--skip_scraping', action='store_true', help='Skip scraping and use existing input.json')
    parser.add_argument('--no-prompt', action='store_true', help='Skip interactive prompts and use default values')
    
    args = parser.parse_args()
    
    # Verify API key is provided either as argument or environment variable
    if not args.api_key:
        parser.error("API key is required. Provide it with --api_key or set GEMINI_API_KEY environment variable.")
    
    return args

def display_summary(results):
    """Display a summary of analysis results to the console."""
    if not results:
        print("\nNo results to display.")
        return
    
    # Count results by type
    fraud_count = sum(1 for r in results if r.get("type") == "fraud")
    suspected_count = sum(1 for r in results if r.get("type") == "suspected")
    genuine_count = sum(1 for r in results if r.get("type") == "genuine")
    
    print(f"\nAnalysis complete! Checked {len(results)} apps.")
    print(f"Results saved to data/output/analysis_results.json")
    
    print("\n========= ANALYSIS SUMMARY =========")
    print(f"Total apps analyzed: {len(results)}")
    print(f"- Fraud: {fraud_count}")
    print(f"- Suspected: {suspected_count}")
    print(f"- Genuine: {genuine_count}")
