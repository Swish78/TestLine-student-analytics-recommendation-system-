import os
from typing import Dict, Any
from datetime import datetime
from analytics.quiz_analyzer import QuizAnalyzer
from analytics.performance_tracker import PerformanceTracker
from analytics.recommendation_engine import RecommendationEngine
from analytics.visualization import VisualizationEngine
from utils.data_loader import DataLoader
from utils.config import QUIZ_API_URL, SUBMISSION_API_URL, HISTORY_API_URL
from analytics.llm_analyzer import LLMAnalyzer


def main():
    """Main entry point for the Student Analytics System"""
    try:
        # Initialize components
        data_loader = DataLoader()
        quiz_analyzer = QuizAnalyzer()
        performance_tracker = PerformanceTracker()
        recommendation_engine = RecommendationEngine()
        visualization_engine = VisualizationEngine()

        # Load data
        print("Loading data...")
        quiz_data = data_loader.load_quiz_data(QUIZ_API_URL)
        submission_data = data_loader.load_submission_data(SUBMISSION_API_URL)
        historical_data = data_loader.load_historical_data(HISTORY_API_URL)

        # Processinng current quiz performance
        current_performance = quiz_analyzer.analyze_quiz(
            quiz_data=quiz_data,
            submission_data=submission_data
        )

        # Tracking historical performance
        historical_analysis = performance_tracker.analyze_history(historical_data)

        # Generate recommendations
        recommendations = recommendation_engine.generate_recommendations(
            current_performance=current_performance,
            historical_analysis=historical_analysis
        )

        # Create visualizations
        visualization_engine.create_dashboard(
            current_performance=current_performance,
            historical_analysis=historical_analysis,
            output_path="dashboard.html"
        )
        llm_analyzer = LLMAnalyzer()

        # Generate personalized insights
        insights = llm_analyzer.generate_personalized_insights(
            current_performance=current_performance,
            historical_analysis=historical_analysis
        )

        # Generate study plan
        study_plan = llm_analyzer.generate_study_plan(
            current_performance=current_performance,
            historical_analysis=historical_analysis
        )

        # Output results
        print("\nAnalysis Complete!")
        print("\nCurrent Performance Summary:")
        print(current_performance.summary())

        print("\nHistorical Analysis:")
        print(historical_analysis.summary())

        print("\nRecommendations:")
        for idx, rec in enumerate(recommendations, 1):
            print(f"{idx}. {rec}")

        print("\nDashboard generated: dashboard.html")

        print("\nAI-Generated Insights:")
        print("\nLearning Patterns:")
        print(insights['learning_patterns'])
        print("\nStrengths and Areas for Improvement:")
        print(insights['strengths_and_improvements'])
        print("\nPersonalized Study Plan:")
        print(study_plan)

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
