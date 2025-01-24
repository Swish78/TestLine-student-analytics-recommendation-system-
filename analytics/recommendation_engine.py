from typing import List
from testline2.models.schemas import QuizPerformance, HistoricalAnalysis


class RecommendationEngine:
    def generate_recommendations(
            self,
            current_performance: QuizPerformance,
            historical_analysis: HistoricalAnalysis
    ) -> List[str]:
        recommendations = []

        # Adding performance-based recommendations
        self._add_performance_recommendations(recommendations, current_performance)

        # Adding historical trend recommendations
        self._add_historical_recommendations(recommendations, historical_analysis)

        # Adding learning style recommendations
        self._add_learning_style_recommendations(recommendations, historical_analysis)

        return recommendations

    def _add_performance_recommendations(
            self,
            recommendations: List[str],
            performance: QuizPerformance
    ) -> None:
        if performance.weak_topics:
            topics = ", ".join(performance.weak_topics)
            recommendations.append(
                f"Focus on strengthening your understanding of: {topics}"
            )

        if performance.strong_topics:
            topics = ", ".join(performance.strong_topics)
            recommendations.append(
                f"You're doing well in {topics}. Consider helping peers in these areas!"
            )

    def _add_historical_recommendations(
            self,
            recommendations: List[str],
            historical: HistoricalAnalysis
    ) -> None:
        if historical.improvement_rate < 0:
            recommendations.append(
                "Your performance has been declining. Consider reviewing fundamental concepts "
                "and increasing practice frequency."
            )
        elif historical.improvement_rate < 10:
            recommendations.append(
                "You're maintaining steady progress. Try challenging yourself with harder "
                "questions to accelerate improvement."
            )
        else:
            recommendations.append(
                "Excellent improvement rate! Keep up your current study routine and consider "
                "exploring advanced topics."
            )

    def _add_learning_style_recommendations(
            self,
            recommendations: List[str],
            historical: HistoricalAnalysis
    ) -> None:
        style_recommendations = {
            "Consistent Improver": (
                "Your consistent improvement is commendable. Consider increasing the "
                "difficulty of your practice materials."
            ),
            "Fast but Irregular Learner": (
                "Try to maintain a more regular study schedule to stabilize your "
                "performance across all topics."
            ),
            "Steady Performer": (
                "While your performance is stable, try new learning techniques to "
                "push beyond your comfort zone."
            ),
            "Needs More Structured Approach": (
                "Consider creating a structured study schedule and focusing on one "
                "topic at a time."
            )
        }

        if historical.learning_style in style_recommendations:
            recommendations.append(style_recommendations[historical.learning_style])
