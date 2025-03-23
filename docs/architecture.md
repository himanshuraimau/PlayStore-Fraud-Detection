# Architecture Overview

This document provides a detailed overview of the PlayStore Fraud Detection System architecture.

## High-Level Architecture

The system uses a pipeline architecture with these major components:

```
┌─────────────────┐    ┌────────────────┐    ┌───────────────────┐
│  Data Processing │ -> │ Feature Extract │ -> │ LLM-Based Analysis │
└─────────────────┘    └────────────────┘    └───────────────────┘
         │                                            │
         ▼                                            ▼
┌─────────────────┐                         ┌───────────────────┐
│   Data Storage  │ <---------------------- │ Structured Output  │
└─────────────────┘                         └───────────────────┘
```

## Core Components

### 1. Data Processing

**Responsible for:**
- Loading app data from JSON files
- Preprocessing text data
- Extracting key app metadata

**Implementation:**
- Located in `utils/io_utils.py`
- Uses the `load_json_data()` function to parse JSON files
- Implemented in the `PlayStoreFraudDetector.preprocess_app_data()` method

### 2. Feature Extraction

**Responsible for:**
- Analyzing app permissions
- Evaluating developer information
- Processing user reviews
- Identifying suspicious patterns

**Implementation:**
- Located primarily in `detector.py`
- Key methods:
  - `_count_dangerous_permissions()` - Analyzes permission requests
  - `_analyze_developer_history()` - Evaluates developer credibility
  - `_process_reviews()` - Analyzes review patterns
  - `_extract_suspicious_indicators()` - Combines suspicious signals

### 3. LLM-Based Analysis

**Responsible for:**
- Generating contextual analysis of app data
- Identifying complex fraud patterns
- Making classification decisions

**Implementation:**
- Uses Google's Gemini 2.0 Flash model
- Located in `detector.py`
- Key methods:
  - `generate_llm_prompt()` - Creates prompts for the LLM
  - `analyze_app()` - Handles the LLM API call and response

### 4. Structured Output Generation

**Responsible for:**
- Validating LLM outputs
- Ensuring consistent format
- Providing explanations for decisions

**Implementation:**
- Located in `detector.py`
- Implements the format: `{"type": "fraud"|"genuine"|"suspected", "reason": "explanation"}`
- Uses `_validate_result_format()` to ensure output compliance

### 5. Performance Evaluation

**Responsible for:**
- Calculating detection accuracy metrics
- Providing performance insights
- Supporting model improvement

**Implementation:**
- Located in `utils/metrics.py`
- Calculates standard metrics: accuracy, precision, recall, F1 score
- Provides confusion matrix elements

## Data Flow

1. **Input Data**
   - App data loaded from JSON files in `data/input/`
   - Each app record contains metadata, permissions, developer info, and reviews

2. **Processing Pipeline**
   - Data is preprocessed to extract relevant fields
   - Feature extraction identifies initial suspicious indicators
   - LLM analyzes the data with a specialized prompt
   - Result is validated and formatted

3. **Output Data**
   - Analysis results saved to `data/output/`
   - Performance metrics calculated and displayed

## Key Design Decisions

### Hybrid Detection Approach

The system uses a hybrid approach combining:
- **Rule-based detection**: For clear violation patterns (excessive permissions, missing policies)
- **LLM-based analysis**: For complex contextual understanding and pattern recognition

This approach balances precision and recall while providing explainable results.

### Modular Design

The system is designed with modularity in mind:
- Components are loosely coupled
- Alternative implementations can be swapped in
- New detection methods can be added without changing the core architecture

### Error Handling Strategy

The system implements robust error handling:
- API failures are caught and logged
- Invalid responses from the LLM are detected and handled gracefully
- Default "suspected" classification when analysis fails

## Component Relationships

```
┌──────────────────────────┐
│    PlayStoreFraudDetector│
└───────────┬──────────────┘
            │
            │ uses
            ▼
┌──────────────────────────┐         ┌──────────────────────────┐
│     LLM (Gemini Model)   │◄────────┤   PlayStore API Client   │
└──────────────────────────┘         └──────────────────────────┘
            ▲                                    ▲
            │                                    │
            │ outputs                            │ provides data
            │                                    │
┌──────────┴──────────────┐         ┌───────────┴─────────────┐
│   Structured Output     │         │   Performance Metrics   │
└──────────────────────────┘         └──────────────────────────┘
```

## Extensibility Points

The architecture supports these key extension points:

1. **New Detection Rules**: Add new rule-based indicators in `_extract_suspicious_indicators()`
2. **Alternative LLMs**: Replace Gemini with other models by modifying the `initialize_llm()` method
3. **Additional Data Sources**: Extend `PlayStoreClient` to integrate with more data sources
4. **Custom Metrics**: Add new evaluation metrics in `metrics.py`
