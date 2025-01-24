import os
from typing import Dict, List, Any
from groq import Groq
from models.schemas import QuizPerformance, HistoricalAnalysis
import dotenv

dotenv.load_dotenv()


class LLMAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    def generate_personalized_insights(
            self,
            current_performance: QuizPerformance,
            historical_analysis: HistoricalAnalysis
    ) -> Dict[str, Any]:
        """Generate personalized insights using Groq LLM"""

        prompt = self._create_analysis_prompt(current_performance, historical_analysis)

        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in NEET exam analysis. Assess the student's performance data and deliver detailed, actionable insights, personalized recommendations, and study strategies for improvement."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=2048
        )

        insights = self._process_llm_response(response.choices[0].message.content)
        return insights

    def _create_analysis_prompt(
            self,
            current_performance: QuizPerformance,
            historical_analysis: HistoricalAnalysis
    ) -> str:
        """Create a detailed prompt for the LLM"""
        return f"""
        Analyze the following student performance data and provide detailed insights:

        Current Performance:
        - Overall Score: {current_performance.score}%
        - Accuracy: {current_performance.accuracy}%
        - Strong Topics: {', '.join(current_performance.strong_topics)}
        - Weak Topics: {', '.join(current_performance.weak_topics)}

        Historical Analysis:
        - Learning Style: {historical_analysis.learning_style}
        - Improvement Rate: {historical_analysis.improvement_rate}%
        - Consistent Challenge Areas: {', '.join(historical_analysis.consistent_weak_topics)}

        Please provide:
        1. A detailed analysis of the student's learning patterns
        2. Specific strengths and areas for improvement
        3. Personalized study recommendations
        4. Learning style adaptations
        5. Suggested resources and practice strategies
        """

    def _process_llm_response(self, response: str) -> Dict[str, Any]:
        """Process and structure the LLM response"""
        sections = response.split('\n\n')

        insights = {
            'learning_patterns': sections[0] if len(sections) > 0 else '',
            'strengths_and_improvements': sections[1] if len(sections) > 1 else '',
            'study_recommendations': sections[2] if len(sections) > 2 else '',
            'learning_style_adaptations': sections[3] if len(sections) > 3 else '',
            'suggested_resources': sections[4] if len(sections) > 4 else ''
        }

        return insights

    def generate_study_plan(
            self,
            current_performance: QuizPerformance,
            historical_analysis: HistoricalAnalysis
    ) -> str:
        """Generate a personalized study plan using Groq LLM"""

        prompt = f"""
        Create a detailed study plan for a student with the following performance profile:

        Current Performance:
        - Score: {current_performance.score}%
        - Weak Areas: {', '.join(current_performance.weak_topics)}
        - Strong Areas: {', '.join(current_performance.strong_topics)}

        Learning Style: {historical_analysis.learning_style}
        Improvement Rate: {historical_analysis.improvement_rate}%

        Create a structured weekly study plan that:
        1. Prioritizes weak areas while maintaining strong ones
        2. Matches their learning style
        3. Includes specific resources and practice strategies
        4. Sets measurable goals
        5. Suggests time allocation for each topic
        """

        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert educational analyst specializing in NEET mock test performance. Provide clear, actionable insights, improvement strategies, personalized study recommendations, and resource suggestions based on the student's performance and historical trends."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=2048
        )

        return response.choices[0].message.content
