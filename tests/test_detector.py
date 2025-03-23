import json
import os
import pytest
import sys
import tempfile

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.playstore_fraud.detector import PlayStoreFraudDetector
from src.playstore_fraud.utils.io_utils import load_json_data

# Sample app data for testing
SAMPLE_APP = {
    "appId": "com.test.app",
    "title": "Test Finance App",
    "description": "This is a test finance app that helps you manage your money.",
    "category": "Finance",
    "contentRating": "Rated for 3+",
    "price": 0,
    "developer": {
        "privacyPolicy": "https://testapp.com/privacy"
    }
}

@pytest.fixture
def detector():
    """Create detector instance for testing"""
    api_key = os.environ.get("GEMINI_API_KEY", "dummy_key_for_testing")
    
    # Mock the LLM for testing
    detector = PlayStoreFraudDetector(api_key)
    
    # Override the analyze_app method for testing
    def mock_analyze_app(app_data):
        return {
            "type": "suspected" if "Finance" in app_data.get("category", "") else "genuine",
            "reason": "Test analysis result"
        }
    
    detector.analyze_app = mock_analyze_app
    return detector

def test_preprocess_app_data(detector):
    """Test data preprocessing"""
    processed = detector.preprocess_app_data(SAMPLE_APP)
    
    assert processed["app_id"] == "com.test.app"
    assert processed["title"] == "Test Finance App"
    assert processed["category"] == "Finance"
    assert "suspicious_indicators" in processed

def test_llm_prompt_generation(detector):
    """Test prompt generation"""
    processed = detector.preprocess_app_data(SAMPLE_APP)
    prompt = detector.generate_llm_prompt(processed)
    
    assert isinstance(prompt, str)
    assert "Test Finance App" in prompt
    assert "Finance" in prompt
    assert "JSON object" in prompt

def test_result_format_validation(detector):
    """Test result format validation"""
    # Valid format
    valid_result = {
        "type": "suspected",
        "reason": "Valid reason for suspicion"
    }
    assert detector._validate_result_format(valid_result) is True
    
    # Invalid type
    invalid_type = {
        "type": "maybe_fraud",
        "reason": "Valid reason"
    }
    assert detector._validate_result_format(invalid_type) is False
    
    # Too long reason
    too_long_reason = {
        "type": "fraud",
        "reason": "X" * 301
    }
    assert detector._validate_result_format(too_long_reason) is False

def test_batch_analyze(detector):
    """Test batch analysis"""
    apps = [SAMPLE_APP, SAMPLE_APP.copy()]
    apps[1]["category"] = "Games"
    
    results = detector.batch_analyze(apps)
    
    assert len(results) == 2
    assert results[0]["type"] == "suspected"  # Finance app
    assert results[1]["type"] == "genuine"    # Games app

def test_load_json_data():
    """Test loading JSON data"""
    # Create a temporary JSON file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp:
        test_data = [{"appId": "test1"}, {"appId": "test2"}]
        json.dump(test_data, tmp)
        tmp_name = tmp.name
    
    try:
        loaded_data = load_json_data(tmp_name)
        assert len(loaded_data) == 2
        assert loaded_data[0]["appId"] == "test1"
    finally:
        # Clean up
        os.unlink(tmp_name)

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
