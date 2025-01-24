from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class QuizQuestion:
    id: int
    description: str
    topic: str
    difficulty_level: Optional[str] = None
    options: List[Dict[str, Any]] = field(default_factory=list)
    detailed_solution: Optional[str] = None


@dataclass
class QuizData:
    id: int
    title: str
    description: str
    questions: List[QuizQuestion]
    duration: Optional[int] = None
    total_questions: Optional[int] = None
    difficulty_level: Optional[str] = None


@dataclass
class QuizSubmission:
    id: int
    quiz_id: int
    user_id: str
    score: float
    accuracy: float
    speed: str
    correct_answers: int
    incorrect_answers: int
    total_questions: int
    response_map: Dict[str, int]
    submitted_at: str
    duration: Optional[str] = None


@dataclass
class QuizPerformance:
    user_id: str
    quiz_id: int
    score: float
    accuracy: float
    topic_scores: Dict[str, float]
    weak_topics: List[str]
    strong_topics: List[str]
    timestamp: str

    def summary(self) -> str:
        return (
            f"Score: {self.score:.1f}%\n"
            f"Accuracy: {self.accuracy:.1f}%\n"
            f"Strong Topics: {', '.join(self.strong_topics)}\n"
            f"Topics Needing Improvement: {', '.join(self.weak_topics)}"
        )


@dataclass
class HistoricalAnalysis:
    user_id: str
    improvement_rate: float
    topic_trends: Dict[str, List[float]]
    consistent_weak_topics: List[str]
    learning_style: str

    def summary(self) -> str:
        return (
            f"Overall Improvement: {self.improvement_rate:.1f}%\n"
            f"Learning Style: {self.learning_style}\n"
            f"Consistent Challenge Areas: {', '.join(self.consistent_weak_topics)}\n"
            f"Topics Analyzed: {', '.join(self.topic_trends.keys())}"
        )
