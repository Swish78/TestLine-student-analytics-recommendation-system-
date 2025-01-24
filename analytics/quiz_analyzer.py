from typing import Dict, List, Any
from models.schemas import QuizPerformance
from utils.config import WEAK_PERFORMANCE_THRESHOLD, STRONG_PERFORMANCE_THRESHOLD
from datetime import datetime


class QuizAnalyzer:
    def analyze_quiz(self, quiz_data: Dict[str, Any], submission_data: Dict[str, Any]) -> QuizPerformance:
        questions = quiz_data['quiz']['questions']
        responses = submission_data.get('response_map', {})

        topic_scores = self._calculate_topic_scores(questions, responses)

        # Identify weak and strong topics
        weak_topics = [
            topic for topic, score in topic_scores.items()
            if score < WEAK_PERFORMANCE_THRESHOLD
        ]
        strong_topics = [
            topic for topic, score in topic_scores.items()
            if score >= STRONG_PERFORMANCE_THRESHOLD
        ]

        # Calculate overall score and accuracy
        overall_score = submission_data.get('score', 0)
        accuracy = submission_data.get('accuracy', 0)

        return QuizPerformance(
            user_id=submission_data.get('user_id', 'unknown'),
            quiz_id=submission_data.get('quiz_id', 0),
            score=overall_score,
            accuracy=accuracy,
            topic_scores=topic_scores,
            weak_topics=weak_topics,
            strong_topics=strong_topics,
            timestamp=submission_data.get('submitted_at', datetime.now().isoformat())
        )

    def _calculate_topic_scores(self, questions: List[Dict], responses: Dict) -> Dict[str, float]:
        topic_correct = {}
        topic_total = {}

        for question in questions:
            topic = question.get('topic', 'Unknown')
            topic_total[topic] = topic_total.get(topic, 0) + 1

            correct_option = next(
                (opt['id'] for opt in question['options'] if opt.get('is_correct')),
                None
            )
            if str(responses.get(str(question['id']))) == str(correct_option):
                topic_correct[topic] = topic_correct.get(topic, 0) + 1

        # Calculate percentage scores
        return {
            topic: (topic_correct.get(topic, 0) / total) * 100
            for topic, total in topic_total.items()
        }
