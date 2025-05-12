"""Facial expressions manager for the robot face."""

from typing import Dict, List, Tuple
import time

from .types import ExpressionType, Expression, TalkState
from .display import DisplayInterface

class FacialExpressions:
    """Manages facial expressions and their rendering."""
    def __init__(self, display: DisplayInterface) -> None:
        self.display = display
        self.expressions: Dict[ExpressionType, Expression] = {
            ExpressionType.HAPPY: Expression(
                name="happy",
                points=[(2, 2), (5, 2)],  # Eyes
                lines=[((1, 5), (6, 5)), ((2, 6), (5, 6))],  # Smile
                talk_lines={
                    TalkState.OPEN: [((1, 5), (6, 5)), ((2, 6), (5, 6)), ((3, 4), (4, 4))],
                    TalkState.CLOSED: [((1, 5), (6, 5)), ((2, 6), (5, 6))],
                    TalkState.PARTIAL: [((1, 5), (6, 5)), ((2, 6), (5, 6)), ((3, 5), (4, 5))]
                },
                duration=1.0
            ),
            ExpressionType.SAD: Expression(
                name="sad",
                points=[(2, 2), (5, 2)],  # Eyes
                lines=[((1, 5), (6, 5)), ((2, 4), (5, 4))],  # Frown
                duration=1.0
            ),
            ExpressionType.SURPRISED: Expression(
                name="surprised",
                points=[(2, 2), (5, 2)],  # Eyes
                lines=[((3, 5), (4, 5)), ((3, 6), (4, 6))],  # O mouth
                duration=1.0
            ),
            ExpressionType.WINK: Expression(
                name="wink",
                points=[(5, 2)],  # Right eye
                lines=[((2, 2), (2, 2)), ((1, 5), (6, 5)), ((2, 6), (5, 6))],  # Left eye (dot) and smile
                duration=1.0
            ),
            ExpressionType.NEUTRAL: Expression(
                name="neutral",
                points=[(2, 2), (5, 2)],  # Eyes
                lines=[((2, 5), (5, 5))],  # Straight line mouth
                talk_lines={
                    TalkState.OPEN: [((2, 4), (5, 4))],
                    TalkState.CLOSED: [((2, 5), (5, 5))],
                    TalkState.PARTIAL: [((2, 4), (5, 4)), ((2, 5), (5, 5))]
                },
                duration=1.0
            ),
            ExpressionType.ANGRY: Expression(
                name="angry",
                points=[(2, 2), (5, 2)],  # Eyes
                lines=[((1, 5), (6, 5)), ((2, 4), (3, 4)), ((4, 4), (5, 4))],  # Angry mouth
                duration=1.0
            ),
            ExpressionType.SLEEPING: Expression(
                name="sleeping",
                points=[(5, 2)],  # Right eye
                lines=[((1, 2), (3, 2)), ((2, 5), (5, 5))],  # Left eye (line) and mouth
                duration=1.0
            )
        }

    def draw_expression(self, expression_type: ExpressionType) -> None:
        """Draw a facial expression."""
        if expression_type not in self.expressions:
            raise ValueError(f"Unknown expression: {expression_type}")
            
        expression = self.expressions[expression_type]
        self.display.clear()
        self.display.draw_points(expression.points)
        if expression.lines:
            self.display.draw_lines(expression.lines)

    def get_expression(self, expression_type: ExpressionType) -> Expression:
        """Get an expression by type."""
        if expression_type not in self.expressions:
            raise ValueError(f"Unknown expression: {expression_type}")
        return self.expressions[expression_type]

    def animate_transition(
        self,
        from_expression: ExpressionType,
        to_expression: ExpressionType,
        steps: int = 10,
        duration: float = 1.0
    ) -> None:
        """Animate a transition between two expressions."""
        if from_expression not in self.expressions or to_expression not in self.expressions:
            raise ValueError("Invalid expression type")
            
        step_duration = duration / steps
        for i in range(steps + 1):
            progress = i / steps
            self.display.clear()
            
            # Interpolate points
            for p1, p2 in zip(
                self.expressions[from_expression].points,
                self.expressions[to_expression].points
            ):
                x = int(p1[0] + (p2[0] - p1[0]) * progress)
                y = int(p1[1] + (p2[1] - p1[1]) * progress)
                self.display.draw_points([(x, y)])
            
            # Interpolate lines
            if (self.expressions[from_expression].lines and 
                self.expressions[to_expression].lines):
                for (start1, end1), (start2, end2) in zip(
                    self.expressions[from_expression].lines,
                    self.expressions[to_expression].lines
                ):
                    start_x = int(start1[0] + (start2[0] - start1[0]) * progress)
                    start_y = int(start1[1] + (start2[1] - start1[1]) * progress)
                    end_x = int(end1[0] + (end2[0] - end1[0]) * progress)
                    end_y = int(end1[1] + (end2[1] - end1[1]) * progress)
                    self.display.draw_lines([((start_x, start_y), (end_x, end_y))])
            
            time.sleep(step_duration) 