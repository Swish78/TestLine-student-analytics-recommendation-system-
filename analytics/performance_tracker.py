from typing import Dict, List, Any
from models.schemas import HistoricalAnalysis
from utils.config import WEAK_PERFORMANCE_THRESHOLD
import numpy as np
from datetime import datetime

class PerformanceTracker:
    def analyze_history(self, historical_data: List[Dict[str, Any]]) -> HistoricalAnalysis:
        if not historical_data:
            return self._create_empty_analysis()

        # Sort data by submission date
        sorted_data = sorted(
            historical_data,
            key=lambda x: x.get('submitted_at', ''),
            reverse=True
        )
        
        # Extract performance metrics
        scores = [entry.get('score', 0) for entry in sorted_data]
        accuracy = [float(entry.get('accuracy', 0)) for entry in sorted_data]
        
        # Calculate metrics
        improvement_rate = self._calculate_improvement_rate(scores)
        topic_trends = self._analyze_topic_performance(sorted_data)
        weak_topics = self._identify_weak_topics(sorted_data)
        learning_style = self._determine_learning_style(sorted_data)
        
        return HistoricalAnalysis(
            user_id=sorted_data[0].get('user_id', 'unknown'),
            improvement_rate=improvement_rate,
            topic_trends=topic_trends,
            consistent_weak_topics=weak_topics,
            learning_style=learning_style
        )
    
    def _create_empty_analysis(self) -> HistoricalAnalysis:
        return HistoricalAnalysis(
            user_id="unknown",
            improvement_rate=0.0,
            topic_trends={},
            consistent_weak_topics=[],
            learning_style="New Learner"
        )
    
    def _calculate_improvement_rate(self, scores: List[float]) -> float:
        if len(scores) < 2:
            return 0.0
        
        # Calculate improvement rate using first and last scores
        first_score = float(scores[-1])  # Oldest score
        last_score = float(scores[0])    # Most recent score
        
        if first_score == 0:
            return 0.0
            
        return ((last_score - first_score) / first_score) * 100
    
    def _analyze_topic_performance(self, data: List[Dict[str, Any]]) -> Dict[str, List[float]]:
        topic_performance = {}
        
        for entry in data:
            # Calculate performance metrics per quiz
            correct = entry.get('correct_answers', 0)
            total = entry.get('total_questions', 1)
            accuracy = (correct / total) * 100 if total > 0 else 0
            
            # For now, we'll use a general topic since topic info isn't directly available
            topic = "Overall"
            if topic not in topic_performance:
                topic_performance[topic] = []
            topic_performance[topic].append(accuracy)
        
        return topic_performance
    
    def _identify_weak_topics(self, data: List[Dict[str, Any]]) -> List[str]:
        weak_topics = []
        topic_averages = {}
        
        for entry in data:
            correct = entry.get('correct_answers', 0)
            total = entry.get('total_questions', 1)
            accuracy = (correct / total) * 100 if total > 0 else 0
            
            # For now, we'll use a general assessment
            topic = "Overall"
            if topic not in topic_averages:
                topic_averages[topic] = []
            topic_averages[topic].append(accuracy)
        
        # Calculate average performance per topic
        for topic, scores in topic_averages.items():
            avg_score = sum(scores) / len(scores) if scores else 0
            if avg_score < WEAK_PERFORMANCE_THRESHOLD:
                weak_topics.append(topic)
        
        return weak_topics
    
    def _determine_learning_style(self, data: List[Dict[str, Any]]) -> str:
        if len(data) < 3:
            return "New Learner"
        
        # Calculate key metrics
        recent_scores = [float(entry.get('score', 0)) for entry in data[:3]]
        avg_score = sum(recent_scores) / len(recent_scores)
        
        # Calculate consistency using accuracy
        accuracies = [float(entry.get('accuracy', 0)) for entry in data]
        score_variance = np.var(accuracies) if accuracies else 0
        
        # Determine learning style based on patterns
        if avg_score >= 80 and score_variance < 100:
            return "Consistent High Performer"
        elif avg_score >= 70:
            return "Strong Learner"
        elif score_variance < 100:
            return "Steady Learner"
        elif avg_score < 50 and score_variance > 200:
            return "Needs Structured Approach"
        else:
            return "Developing Learner"