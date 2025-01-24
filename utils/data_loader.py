import requests
from typing import Dict, Any, Optional, List
import pandas as pd
from datetime import datetime
import warnings

# Suppress InsecureRequestWarning
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


class DataLoader:
    def __init__(self):
        self.session = requests.Session()

    def _parse_percentage(self, value: Any) -> float:
        """Convert percentage string to float"""
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            # Remove '%' and any whitespace, then convert to float
            cleaned = value.strip().rstrip('%').strip()
            return float(cleaned) if cleaned else 0.0
        return 0.0

    def load_quiz_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Load and validate quiz data"""
        try:
            response = self.session.get(url, verify=False)
            response.raise_for_status()
            data = response.json()

            # Validate required fields
            if 'quiz' not in data or 'questions' not in data['quiz']:
                raise ValueError("Invalid quiz data format")

            return data
        except Exception as e:
            print(f"Error loading quiz data: {str(e)}")
            return None

    def load_submission_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Load and validate submission data"""
        try:
            response = self.session.get(url, verify=False)
            response.raise_for_status()
            data = response.json()

            # Validate required fields
            required_fields = ['user_id', 'quiz_id', 'score', 'response_map']
            if not all(field in data for field in required_fields):
                raise ValueError("Invalid submission data format")

            # Parse percentage fields
            data['accuracy'] = self._parse_percentage(data.get('accuracy', 0))
            data['score'] = self._parse_percentage(data.get('score', 0))

            return data
        except Exception as e:
            print(f"Error loading submission data: {str(e)}")
            return None

    def load_historical_data(self, url: str) -> Optional[List[Dict[str, Any]]]:
        """Load and process historical data"""
        try:
            response = self.session.get(url, verify=False)
            response.raise_for_status()
            data = response.json()

            processed_data = []
            for entry in data:
                processed_entry = {
                    'user_id': entry.get('user_id'),
                    'quiz_id': entry.get('quiz_id'),
                    'score': self._parse_percentage(entry.get('score', 0)),
                    'accuracy': self._parse_percentage(entry.get('accuracy', 0)),
                    'submitted_at': entry.get('submitted_at'),
                    'response_map': entry.get('response_map', {}),
                    'correct_answers': entry.get('correct_answers', 0),
                    'incorrect_answers': entry.get('incorrect_answers', 0),
                    'total_questions': entry.get('total_questions', 0)
                }
                processed_data.append(processed_entry)

            return processed_data

        except Exception as e:
            print(f"Error loading historical data: {str(e)}")
            return None
