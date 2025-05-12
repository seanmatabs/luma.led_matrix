"""Facial expressions manager for the robot face."""

from typing import Dict, List, Tuple, Set
import time

from .face_types import ExpressionType, Expression, TalkState
from .display import DisplayInterface

class FacialExpressions:
    """Manages facial expressions and their rendering."""
    def __init__(self, display: DisplayInterface) -> None:
        self.display = display
        # Helper functions to create different eye shapes
        def create_eye_rectangle(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create a full 3x2 rectangle eye."""
            return [((x, y), (x + 2, y + 1))]

        def create_eye_slant_left(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create a slanted eye (for angry expression)."""
            return [
                ((x, y), (x + 1, y)),  # Top left
                ((x + 1, y + 1), (x + 2, y + 1)),  # Bottom right
                ((x, y), (x + 1, y + 1)),  # Diagonal
                ((x + 1, y), (x + 2, y + 1))  # Diagonal
            ]

        def create_eye_slant_right(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create a slanted eye (for angry expression)."""
            return [
                ((x + 1, y), (x + 2, y)),  # Top right
                ((x, y + 1), (x + 1, y + 1)),  # Bottom left
                ((x + 1, y), (x, y + 1)),  # Diagonal
                ((x + 2, y), (x + 1, y + 1))  # Diagonal
            ]

        def create_eye_half(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create a half-closed eye (for happy/wink)."""
            return [
                ((x, y), (x + 2, y)),  # Top line
                ((x, y + 1), (x + 2, y + 1))  # Bottom line
            ]

        def create_eye_closed(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create a closed eye (for sleeping)."""
            return [((x, y + 1), (x + 2, y + 1))]  # Single line

        def create_eye_surprised(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create a surprised eye (round)."""
            return [
                ((x, y), (x + 2, y)),  # Top
                ((x, y + 1), (x + 2, y + 1)),  # Bottom
                ((x, y), (x, y + 1)),  # Left
                ((x + 2, y), (x + 2, y + 1))  # Right
            ]

        def create_eye_angry_left(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create an angry eye using line segments."""
            return [
                # Top line
                ((x, y), (x + 2, y)),
                # Bottom line
                ((x, y + 1), (x + 2, y + 1)),
                # Diagonal lines
                ((x, y), (x + 2, y + 1)),  # Top-left to bottom-right
                ((x + 2, y), (x, y + 1))   # Top-right to bottom-left
            ]

        def create_eye_angry_right(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create an angry eye using line segments."""
            return [
                # Top line
                ((x, y), (x + 2, y)),
                # Bottom line
                ((x, y + 1), (x + 2, y + 1)),
                # Diagonal lines
                ((x, y), (x + 2, y + 1)),  # Top-left to bottom-right
                ((x + 2, y), (x, y + 1))   # Top-right to bottom-left
            ]

        # Create eye positions with 2-LED gap
        left_pos = 0
        right_pos = 5
        y_pos = 1

        # Create different eye variations
        happy_left = create_eye_half(left_pos, y_pos)
        happy_right = create_eye_half(right_pos, y_pos)
        sad_left = create_eye_half(left_pos, y_pos)
        sad_right = create_eye_half(right_pos, y_pos)
        surprised_left = create_eye_surprised(left_pos, y_pos)
        surprised_right = create_eye_surprised(right_pos, y_pos)
        wink_left = create_eye_closed(left_pos, y_pos)
        wink_right = create_eye_half(right_pos, y_pos)
        neutral_left = create_eye_rectangle(left_pos, y_pos)
        neutral_right = create_eye_rectangle(right_pos, y_pos)
        angry_left = create_eye_angry_left(left_pos, y_pos)
        angry_right = create_eye_angry_right(right_pos, y_pos)
        sleeping_left = create_eye_closed(left_pos, y_pos)
        sleeping_right = create_eye_closed(right_pos, y_pos)

        self.expressions: Dict[ExpressionType, Expression] = {
            ExpressionType.HAPPY: Expression(
                name="happy",
                points=[],
                lines=[
                    *happy_left,  # Left eye (half-closed)
                    *happy_right,  # Right eye (half-closed)
                    ((1, 5), (6, 5)),  # Smile top
                    ((2, 6), (5, 6))   # Smile bottom
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *happy_left, *happy_right,  # Eyes
                        ((1, 5), (6, 5)),  # Mouth top
                        ((2, 6), (5, 6)),  # Mouth bottom
                        ((3, 4), (4, 4))   # Mouth middle
                    ],
                    TalkState.CLOSED: [
                        *happy_left, *happy_right,  # Eyes
                        ((1, 5), (6, 5)),  # Mouth top
                        ((2, 6), (5, 6))   # Mouth bottom
                    ],
                    TalkState.PARTIAL: [
                        *happy_left, *happy_right,  # Eyes
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
                    *sad_left,  # Left eye (half-closed)
                    *sad_right,  # Right eye (half-closed)
                    ((1, 5), (6, 5)),  # Frown top
                    ((2, 4), (5, 4))   # Frown bottom
                ],
                duration=1.0
            ),
            ExpressionType.SURPRISED: Expression(
                name="surprised",
                points=[],
                lines=[
                    *surprised_left,  # Left eye (round)
                    *surprised_right,  # Right eye (round)
                    ((3, 5), (4, 5)),  # O mouth top
                    ((3, 6), (4, 6))   # O mouth bottom
                ],
                duration=1.0
            ),
            ExpressionType.WINK: Expression(
                name="wink",
                points=[],
                lines=[
                    *wink_left,  # Left eye (closed)
                    *wink_right,  # Right eye (half-closed)
                    ((1, 5), (6, 5)),  # Smile top
                    ((2, 6), (5, 6))   # Smile bottom
                ],
                duration=1.0
            ),
            ExpressionType.NEUTRAL: Expression(
                name="neutral",
                points=[],
                lines=[
                    *neutral_left,  # Left eye (full)
                    *neutral_right,  # Right eye (full)
                    ((2, 5), (5, 5))   # Straight line mouth
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *neutral_left, *neutral_right,  # Eyes
                        ((2, 4), (5, 4))  # Mouth open
                    ],
                    TalkState.CLOSED: [
                        *neutral_left, *neutral_right,  # Eyes
                        ((2, 5), (5, 5))  # Mouth closed
                    ],
                    TalkState.PARTIAL: [
                        *neutral_left, *neutral_right,  # Eyes
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
                    *angry_left,  # Left eye (slanted)
                    *angry_right,  # Right eye (slanted)
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
                    *sleeping_left,  # Left eye (closed)
                    *sleeping_right,  # Right eye (closed)
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