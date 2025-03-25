import json
import logging
from typing import Dict, List, Optional
from google_play_scraper import search, app, permissions, reviews, Sort
from datetime import datetime


logger = logging.getLogger('FraudDetectionSystem')


class PlayStoreClient:
    """
    A client for fetching and processing data from Google Play Store.
    """
    
    def __init__(
        self, 
        query: str = "buisness", 
        country: str = "us", 
        lang: str = "en", 
        top_n: int = 5, 
        review_count: int = 5
    ):
        """
        Initialize the PlayStoreClient with search parameters.
        
        Args:
            query: Search query string
            country: Country code for the search
            lang: Language code for the search
            top_n: Number of apps to fetch
            review_count: Number of reviews to fetch per app
        """
        self.query = query
        self.country = country
        self.lang = lang
        self.top_n = top_n
        self.review_count = review_count
        self.apps_data = []
    
    def convert_datetime(self, obj):
        """Helper function to convert datetime objects to strings."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj

    def make_json_serializable(self, data):
        """Process data to make it JSON serializable."""
        if isinstance(data, dict):
            return {k: self.make_json_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.make_json_serializable(item) for item in data]
        else:
            return self.convert_datetime(data)
    
    def search_apps(self):
        """Fetch the top search results based on query."""
        logger.info(f"Searching for '{self.query}' apps in {self.country}")
        try:
            results = search(
                self.query, 
                n_hits=self.top_n, 
                lang=self.lang, 
                country=self.country
            )
            
            # Check if we got any results
            if not results:
                logger.warning(f"No results found for query '{self.query}'. Check your spelling or try a different search term.")
                # Try with a fix for common misspellings
                if self.query == "buisness":
                    logger.info("Attempting to fix misspelling: 'buisness' -> 'business'")
                    self.query = "business"
                    return self.search_apps()  # Retry with corrected spelling
                
            return results or []  # Return empty list if None
            
        except Exception as e:
            logger.error(f"Error searching for apps: {e}")
            return []  # Return empty list on error
    
    def get_app_details(self, package_name: str):
        """Fetch detailed app information."""
        try:
            return app(package_name, lang=self.lang, country=self.country)
        except Exception as e:
            logger.error(f"Failed to get details for {package_name}: {e}")
            return {}
    
    def get_app_permissions(self, package_name: str):
        """Fetch app permissions."""
        try:
            permissions_list = permissions(
                package_name,
                lang=self.lang,
                country=self.country
            )
            return permissions_list
        except Exception as e:
            logger.error(f"Could not fetch permissions for {package_name}: {e}")
            return []
    
    def get_app_reviews(self, package_name: str):
        """Fetch app reviews."""
        try:
            reviews_list, _ = reviews(
                package_name,
                lang=self.lang,
                country=self.country,
                sort=Sort.NEWEST,
                count=self.review_count
            )
            logger.info(f"Fetched {len(reviews_list)} reviews for {package_name}")
            return reviews_list
        except Exception as e:
            logger.error(f"Could not fetch reviews for {package_name}: {e}")
            return []
    
    def process_app(self, result: dict, index: int):
        """Process a single app's data."""
        package_name = result.get("appId")
        logger.info(f"Fetching details for app {index+1}: {package_name}")
        
        details = self.get_app_details(package_name)
        permissions_list = self.get_app_permissions(package_name)
        reviews_list = self.get_app_reviews(package_name)
        
        # Make sure review data is JSON serializable
        serializable_reviews = self.make_json_serializable(reviews_list)
        
        # Structure the data
        app_data = {
            "appId": details.get("appId"),
            "categories": [
                {
                    "name": details.get("genre"),
                    "id": details.get("genreId"),
                    "_id": f"{index+1:02d}{details.get('appId', '')[:6]}"  # Simulated unique ID
                }
            ],
            "category": details.get("genre"),
            "categoryId": details.get("genreId"),
            "contentRating": details.get("contentRating"),
            "currency": details.get("priceCurrency"),
            "description": details.get("description"),
            "developer": {
                "name": details.get("developer"),
                "id": details.get("developerId"),
                "internalId": details.get("developerId"),
                "email": details.get("developerEmail"),
                "privacyPolicy": details.get("privacyPolicy"),
                "legalName": details.get("developer"),
                "legalEmail": details.get("developerEmail"),
                "legalAddress": details.get("developerAddress")
            },
            "features": {
                "isEditorChoice": details.get("editorChoice"),
                "hasAds": details.get("adSupported"),
                "isPreregister": details.get("preregister"),
                "isEarlyAccess": details.get("earlyAccess"),
                "isPlayPassAvailable": details.get("playPass"),
                "requiredFeatures": details.get("requiredFeatures", [])
            },
            "hasInAppPurchases": details.get("offersIAP"),
            "headerImage": details.get("headerImage"),
            "icon": details.get("icon"),
            "isFree": details.get("free"),
            "media": {
                "screenshots": details.get("screenshots"),
                "video": details.get("video"),
                "videoImage": details.get("videoImage"),
                "previewVideo": details.get("video"),
                "ipadScreenshots": details.get("ipadScreenshots", []),
                "appletvScreenshots": details.get("appletvScreenshots", [])
            },
            "metrics": {
                "ratings": {
                    "average": details.get("score", 0),
                    "averageText": str(details.get("score", 0.0)),
                    "total": details.get("ratings", 0),
                    "distribution": details.get("histogram", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0})
                },
                "reviews": details.get("reviews", 0),
                "installs": {
                    "text": details.get("installs"),
                    "min": details.get("minInstalls", 0),
                    "max": details.get("realInstalls", details.get("minInstalls", 0))
                }
            },
            "permissions": {
                "list": permissions_list,
                "count": len(permissions_list)
            },
            "price": details.get("price"),
            "priceText": "Free" if details.get("price") == 0 else f"${details.get('price')}",
            "summary": details.get("summary"),
            "title": details.get("title"),
            "url": f"https://play.google.com/store/apps/details?id={details.get('appId')}&hl={self.lang}&gl={self.country}",
            "version": {
                "number": details.get("version"),
                "released": details.get("released"),
                "lastUpdated": details.get("updated"),
                "minimumOsVersion": details.get("androidVersion"),
                "maximumOsVersion": "VARY",
                "osVersionText": details.get("androidVersionText", "Unknown")
            },
            "comments": [
                {
                    "id": review.get("reviewId", ""),
                    "userName": review.get("userName", "Anonymous"),
                    "text": review.get("content", ""),
                    "score": review.get("score", 0),
                    "thumbsUpCount": review.get("thumbsUpCount", 0),
                    "reviewCreatedVersion": review.get("reviewCreatedVersion", ""),
                    "at": self.convert_datetime(review.get("at", "")),
                    "replyContent": review.get("replyContent", ""),
                    "replyAt": self.convert_datetime(review.get("replyAt", ""))
                } for review in serializable_reviews
            ]
        }
        
        return app_data
    
    def fetch_all_apps(self):
        """Fetch and process all apps based on search criteria."""
        search_results = self.search_apps()
        self.apps_data = []
        
        if not search_results:
            logger.warning(f"No search results found for '{self.query}'. Check spelling or try another query.")
            return self.apps_data
        
        for i, result in enumerate(search_results):
            app_data = self.process_app(result, i)
            self.apps_data.append(app_data)
        
        # Make entire dataset JSON serializable
        self.apps_data = self.make_json_serializable(self.apps_data)
        return self.apps_data
    
    def save_to_json(self, filepath: str = "data/input/input.json"):
        """Save the processed app data to a JSON file."""
        if not self.apps_data:
            logger.warning("No app data to save. Call fetch_all_apps() first.")
            return
            
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(self.apps_data, f, indent=4, ensure_ascii=False)
            logger.info(f"App data successfully saved to {filepath}")
            print(f"Top {self.top_n} {self.query} apps saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save app data: {e}")
            raise


# Example usage
if __name__ == "__main__":
    def get_user_query():
        """Ask user for app category to query"""
        print("Welcome to PlayStore App Analyzer")
        print("-" * 35)
        print("What type of apps would you like to analyze?")
        print("Examples: business, finance, games, social, education, etc.")
        query = input("Enter app category/query: ").strip()
        
        if not query:
            print("Using default query 'business'")
            return "business"
        
        # Ask for number of apps to fetch
        try:
            top_n = int(input("How many apps would you like to analyze? [5]: ") or "5")
        except ValueError:
            print("Invalid input. Using default (5 apps)")
            top_n = 5
            
        # Ask for number of reviews per app
        try:
            review_count = int(input("How many reviews per app would you like to fetch? [5]: ") or "5")
        except ValueError:
            print("Invalid input. Using default (5 reviews)")
            review_count = 5
            
        return query, top_n, review_count

    # Get user input
    query_input = get_user_query()
    
    # Check if we got a tuple (with all parameters) or just a string (query only)
    if isinstance(query_input, tuple):
        query, top_n, review_count = query_input
    else:
        query, top_n, review_count = query_input, 5, 5
    
    client = PlayStoreClient(query=query, top_n=top_n, review_count=review_count)
    client.fetch_all_apps()
    client.save_to_json()
    print(f"\nAnalysis complete! Data saved to data/input/input.json")
