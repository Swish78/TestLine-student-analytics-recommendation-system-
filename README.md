# Student Analytics and Recommendation System

A system designed to help students improve their learning by analyzing their quiz performances and providing personalized recommendations.

## Features

- Analyze quiz performance in real-time.
- Track progress over time.
- Identify strengths and weaknesses by topic.
- Provide personalized learning recommendations.
- Interactive dashboards for insights.

## Technology Stack

- **Frontend**: Dash & Plotly
- **Data Analysis**: NumPy, Pandas, Scikit-learn
- **Visualization**: Matplotlib, Seaborn
- **NLP Tools**: Stanza

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**:
   Either from `requirements.txt` (if available):
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up the `.env` File**:
   Create a `.env` file in the root directory of your project:
     ```
     touch .env
     ```
   Add your **GROQ API key** to the `.env` file in the following format:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```

5. **Run the Application**:
   ```bash
   python main.py
   ```

5. **View the Dashboard**:
   Open dashboard.html on your browser.

## Using the Conda Environment (Optional)

1. Create a Conda environment from the `environment.yml` file:
   ```bash
   conda env create -f environment.yml
   conda activate <environment_name>
   ```

2. Recreate the exact environment for cross-platform compatibility.

## Folder Structure
```
testline/
├── analytics/
│   ├── __init__.py
│   ├── quiz_analyzer.py
│   ├── performance_tracker.py
│   ├── llm_analyzer.py
│   ├── recommendation_engine.py
│   └── visualization.py
├── utils/
│   ├── __init__.py
│   ├── data_loader.py
│   └── config.py
├── models/
│   ├── __init__.py
│   └── schemas.py
├── tests/
│   ├── __init__.py
│   └── test_analytics.py
├── main.py
├── requirements.txt
└── README.md
```

Walk-through: https://testline-walkthrough.s3.us-east-1.amazonaws.com/Screen+Recording+2025-01-24+at+19.13.03.mov
