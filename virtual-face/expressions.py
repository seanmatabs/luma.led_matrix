"""Facial expressions manager for the robot face."""

from typing import Dict, List, Tuple, Set
import time

from .face_types import ExpressionType, Expression, TalkState
from .display import DisplayInterface

class FacialExpressions:
    """Manages facial expressions and their rendering."""
    def __init__(self, display: DisplayInterface) -> None:
        self.display = display
        # Helper function to create eye rectangles
        def create_eye(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y), (x + 2, y + 1))]  # 3x2 rectangle for each eye

        # Create eye rectangles for all expressions with 2-LED gap between eyes
        # Left eye at (0,1) to (2,2), right eye at (5,1) to (7,2)
        left_eye = create_eye(0, 1)  # Left eye at (0,1) to (2,2)
        right_eye = create_eye(5, 1)  # Right eye at (5,1) to (7,2)

        self.expressions: Dict[ExpressionType, Expression] = {
            ExpressionType.HAPPY: Expression(
                name="happy",
                points=[],
                lines=[
                    *left_eye,  # Left eye rectangle
                    *right_eye,  # Right eye rectangle
                    ((1, 5), (6, 5)),  # Smile top
                    ((2, 6), (5, 6))   # Smile bottom
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *left_eye, *right_eye,  # Eyes
                        ((1, 5), (6, 5)),  # Mouth top
                        ((2, 6), (5, 6)),  # Mouth bottom
                        ((3, 4), (4, 4))   # Mouth middle
                    ],
                    TalkState.CLOSED: [
                        *left_eye, *right_eye,  # Eyes
                        ((1, 5), (6, 5)),  # Mouth top
                        ((2, 6), (5, 6))   # Mouth bottom
                    ],
                    TalkState.PARTIAL: [
                        *left_eye, *right_eye,  # Eyes
                        ((1, 5), (6, 5)),  # Mouth top
                        ((2, 6), (5, 6)),  # Mouth bottom
                        ((3, 5), (4, 5))   # Mouth middle
                    ]
                },
                duration=1.0
            ),
            ExpressionType.SAD: Expression(
                name="sad",
                points=[],
                lines=[
                    *left_eye,  # Left eye rectangle
                    *right_eye,  # Right eye rectangle
                    ((1, 5), (6, 5)),  # Frown top
                    ((2, 4), (5, 4))   # Frown bottom
                ],
                duration=1.0
            ),
            ExpressionType.SURPRISED: Expression(
                name="surprised",
                points=[],
                lines=[
                    *left_eye,  # Left eye rectangle
                    *right_eye,  # Right eye rectangle
                    ((3, 5), (4, 5)),  # O mouth top
                    ((3, 6), (4, 6))   # O mouth bottom
                ],
                duration=1.0
            ),
            ExpressionType.WINK: Expression(
                name="wink",
                points=[],
                lines=[
                    *right_eye,  # Right eye rectangle
                    ((0, 1), (2, 2)),  # Left eye (wink)
                    ((1, 5), (6, 5)),  # Smile top
                    ((2, 6), (5, 6))   # Smile bottom
                ],
                duration=1.0
            ),
            ExpressionType.NEUTRAL: Expression(
                name="neutral",
                points=[],
                lines=[
                    *left_eye,  # Left eye rectangle
                    *right_eye,  # Right eye rectangle
                    ((2, 5), (5, 5))   # Straight line mouth
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *left_eye, *right_eye,  # Eyes
                        ((2, 4), (5, 4))  # Mouth open
                    ],
                    TalkState.CLOSED: [
                        *left_eye, *right_eye,  # Eyes
                        ((2, 5), (5, 5))  # Mouth closed
                    ],
                    TalkState.PARTIAL: [
                        *left_eye, *right_eye,  # Eyes
                        ((2, 4), (5, 4)),  # Mouth top
                        ((2, 5), (5, 5))   # Mouth bottom
                    ]
                },
                duration=1.0
            ),
            ExpressionType.ANGRY: Expression(
                name="angry",
                points=[],
                lines=[
                    *left_eye,  # Left eye rectangle
                    *right_eye,  # Right eye rectangle
                    ((1, 5), (6, 5)),  # Angry mouth top
                    ((2, 4), (3, 4)),  # Angry mouth left
                    ((4, 4), (5, 4))   # Angry mouth right
                ],
                duration=1.0
            ),
            ExpressionType.SLEEPING: Expression(
                name="sleeping",
                points=[],
                lines=[
                    *right_eye,  # Right eye rectangle
                    ((0, 1), (2, 2)),  # Left eye (sleeping)
                    ((2, 5), (5, 5))   # Mouth
                ],
                duration=1.0
            )
        }

    def draw_expression(self, expression_type: ExpressionType) -> None:
        """Draw a facial expression."""
        if expression_type not in self.expressions:
            raise ValueError(f"Unknown expression: {expression_type}")
            
        expression = self.expressions[expression_type]
        self.display.clear()
        
        # Draw all lines in a single canvas operation
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
        steps: int = 5,
        duration: float = 0.5
    ) -> None:
        """Animate a transition between two expressions."""
        if from_expression not in self.expressions or to_expression not in self.expressions:
            raise ValueError("Invalid expression type")
            
        # Draw each expression in sequence for a simple transition
        for i in range(steps):
            if i % 2 == 0:
                self.draw_expression(from_expression)
            else:
                self.draw_expression(to_expression)
            time.sleep(duration / steps)
        
        # Always end with the target expression
        self.draw_expression(to_expression) 