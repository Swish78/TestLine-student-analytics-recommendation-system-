from typing import Dict, List
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from models.schemas import QuizPerformance, HistoricalAnalysis


class VisualizationEngine:
    def create_dashboard(
            self,
            current_performance: QuizPerformance,
            historical_analysis: HistoricalAnalysis,
            output_path: str
    ) -> None:
        fig = make_subplots(
            rows=2, cols=2,
            specs=[
                [{"type": "polar"}, {"type": "xy"}],
                [{"type": "xy"}, {"type": "indicator"}]
            ],
            subplot_titles=(
                'Current Topic Performance',
                'Historical Progress',
                'Topic Trends',
                'Learning Style Analysis'
            )
        )

        # Add current performance radar chart
        self._add_topic_radar(fig, current_performance)

        # Add historical progress line chart
        self._add_historical_progress(fig, historical_analysis)

        # Add topic trends heatmap
        self._add_topic_trends(fig, historical_analysis)

        # Add learning style analysis
        self._add_learning_style(fig, historical_analysis)

        # Update layout
        fig.update_layout(
            height=800,
            width=1200,
            showlegend=True,
            title_text="Student Performance Dashboard",
            title_x=0.5,
            title_font_size=20
        )

        # Save to HTML file
        fig.write_html(output_path)

    def _add_topic_radar(self, fig, performance: QuizPerformance) -> None:
        """Add radar chart for current topic performance"""
        fig.add_trace(
            go.Scatterpolar(
                r=list(performance.topic_scores.values()),
                theta=list(performance.topic_scores.keys()),
                fill='toself',
                name='Topic Performance'
            ),
            row=1, col=1
        )

        fig.update_polars(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        )

    def _add_historical_progress(self, fig, historical: HistoricalAnalysis) -> None:
        """Add line chart for historical progress"""
        for topic, scores in historical.topic_trends.items():
            fig.add_trace(
                go.Scatter(
                    y=scores,
                    mode='lines+markers',
                    name=f'{topic} Progress',
                    hovertemplate='Score: %{y:.1f}%'
                ),
                row=1, col=2
            )

        fig.update_xaxes(title_text="Quiz Number", row=1, col=2)
        fig.update_yaxes(title_text="Score (%)", row=1, col=2)

    def _add_topic_trends(self, fig, historical: HistoricalAnalysis) -> None:
        """Add line chart for topic trends"""
        for topic, scores in historical.topic_trends.items():
            fig.add_trace(
                go.Scatter(
                    y=scores,
                    mode='lines+markers',
                    name=topic,
                    showlegend=False
                ),
                row=2, col=1
            )

        fig.update_xaxes(title_text="Attempt", row=2, col=1)
        fig.update_yaxes(title_text="Score (%)", row=2, col=1)

    def _add_learning_style(self, fig, historical: HistoricalAnalysis) -> None:
        """Add indicator for learning style and improvement rate"""
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=historical.improvement_rate,
                title={'text': f"Learning Style:<br>{historical.learning_style}"},
                delta={'reference': 0},
                gauge={
                    'axis': {'range': [-50, 100]},
                    'steps': [
                        {'range': [-50, 0], 'color': "lightgray"},
                        {'range': [0, 50], 'color': "lightblue"},
                        {'range': [50, 100], 'color': "cyan"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 80
                    }
                }
            ),
            row=2, col=2
        )
