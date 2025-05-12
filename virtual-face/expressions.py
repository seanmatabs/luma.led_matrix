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
        def create_eye_happy(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create a happy eye (curved like emoji)."""
            return [
                ((x, y), (x + 2, y)),  # Top line
                ((x, y + 1), (x + 2, y + 1)),  # Bottom line
                ((x, y), (x, y + 1)),  # Left side
                ((x + 2, y), (x + 2, y + 1))   # Right side
            ]

        def create_eye_sad(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create a sad eye (with tear)."""
            return [
                ((x, y), (x + 2, y)),  # Top line
                ((x, y + 1), (x + 2, y + 1)),  # Bottom line
                ((x, y), (x, y + 1)),  # Left side
                ((x + 2, y), (x + 2, y + 1)),  # Right side
                ((x + 1, y + 2), (x + 1, y + 2))  # Tear drop
            ]

        def create_eye_surprised(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create a surprised eye (round like emoji)."""
            return [
                ((x, y), (x + 2, y)),  # Top
                ((x, y + 1), (x + 2, y + 1)),  # Bottom
                ((x, y), (x, y + 1)),  # Left
                ((x + 2, y), (x + 2, y + 1)),  # Right
                ((x + 1, y + 2), (x + 1, y + 2))  # Extra dot for emphasis
            ]

        def create_eye_wink(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create a winking eye (curved line)."""
            return [((x, y + 1), (x + 2, y + 1))]  # Curved line for wink

        def create_eye_neutral(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create a neutral eye (simple dot)."""
            return [((x + 1, y + 1), (x + 1, y + 1))]  # Single dot

        def create_eye_angry(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create an angry eye (slanted like emoji)."""
            return [
                ((x, y), (x + 2, y + 1)),  # Slanted line
                ((x + 1, y), (x + 1, y + 1))  # Vertical line for emphasis
            ]

        def create_eye_sleeping(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """Create a sleeping eye (curved line with Z)."""
            return [
                ((x, y + 1), (x + 2, y + 1)),  # Curved line
                ((x + 1, y), (x + 2, y)),  # Z top
                ((x, y + 2), (x + 1, y + 2))  # Z bottom
            ]

        # Create eye positions with 2-LED gap
        left_pos = 0
        right_pos = 5
        y_pos = 1

        # Create different eye variations
        happy_left = create_eye_happy(left_pos, y_pos)
        happy_right = create_eye_happy(right_pos, y_pos)
        sad_left = create_eye_sad(left_pos, y_pos)
        sad_right = create_eye_sad(right_pos, y_pos)
        surprised_left = create_eye_surprised(left_pos, y_pos)
        surprised_right = create_eye_surprised(right_pos, y_pos)
        wink_left = create_eye_wink(left_pos, y_pos)
        wink_right = create_eye_happy(right_pos, y_pos)
        neutral_left = create_eye_neutral(left_pos, y_pos)
        neutral_right = create_eye_neutral(right_pos, y_pos)
        angry_left = create_eye_angry(left_pos, y_pos)
        angry_right = create_eye_angry(right_pos, y_pos)
        sleeping_left = create_eye_sleeping(left_pos, y_pos)
        sleeping_right = create_eye_sleeping(right_pos, y_pos)

        self.expressions: Dict[ExpressionType, Expression] = {
            ExpressionType.HAPPY: Expression(
                name="happy",
                points=[],
                lines=[
                    *happy_left,  # Left eye (happy)
                    *happy_right,  # Right eye (happy)
                    ((1, 6), (6, 6)),  # Smile top
                    ((2, 7), (5, 7)),  # Smile bottom
                    ((1, 6), (2, 7)),  # Left curve
                    ((5, 7), (6, 6))   # Right curve
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *happy_left, *happy_right,  # Eyes
                        ((1, 5), (2, 5)),  # Mouth left
                        ((5, 5), (6, 5)),  # Mouth right
                        ((1, 6), (2, 6)),  # Mouth bottom left
                        ((5, 6), (6, 6)),  # Mouth bottom right
                        ((1, 5), (2, 6)),  # Left curve
                        ((5, 6), (6, 5))   # Right curve
                    ],
                    TalkState.CLOSED: [
                        *happy_left, *happy_right,  # Eyes
                        ((1, 6), (6, 6)),  # Smile top
                        ((2, 7), (5, 7)),  # Smile bottom
                        ((1, 6), (2, 7)),  # Left curve
                        ((5, 7), (6, 6))   # Right curve
                    ],
                    TalkState.PARTIAL: [
                        *happy_left, *happy_right,  # Eyes
                        ((1, 6), (6, 6)),  # Smile top
                        ((2, 7), (5, 7)),  # Smile bottom
                        ((1, 6), (2, 7)),  # Left curve
                        ((5, 7), (6, 6)),  # Right curve
                        ((1, 5), (2, 5)),  # Mouth left
                        ((5, 5), (6, 5))   # Mouth right
                    ]
                },
                duration=1.0
            ),
            ExpressionType.SAD: Expression(
                name="sad",
                points=[],
                lines=[
                    *sad_left,  # Left eye (with tear)
                    *sad_right,  # Right eye (with tear)
                    ((1, 6), (6, 6)),  # Frown top
                    # ((2, 5), (5, 5)),  # Frown bottom
                    ((1, 6), (2, 5)),  # Left curve
                    ((5, 5), (6, 6))   # Right curve
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *sad_left, *sad_right,  # Eyes
                        ((1, 5), (2, 5)),  # Mouth left
                        ((5, 5), (6, 5)),  # Mouth right
                        ((1, 6), (2, 6)),  # Mouth bottom left
                        ((5, 6), (6, 6)),  # Mouth bottom right
                        ((1, 5), (2, 6)),  # Left curve
                        ((5, 6), (6, 5))   # Right curve
                    ],
                    TalkState.CLOSED: [
                        *sad_left, *sad_right,  # Eyes
                        ((1, 6), (6, 6)),  # Frown top
                        # ((2, 5), (5, 5)),  # Frown bottom
                        ((1, 6), (2, 5)),  # Left curve
                        ((5, 5), (6, 6))   # Right curve
                    ],
                    TalkState.PARTIAL: [
                        *sad_left, *sad_right,  # Eyes
                        ((1, 6), (6, 6)),  # Frown top
                        # ((2, 5), (5, 5)),  # Frown bottom
                        ((1, 6), (2, 5)),  # Left curve
                        ((5, 5), (6, 6)),  # Right curve
                        ((1, 5), (2, 5)),  # Mouth left
                        ((5, 5), (6, 5))   # Mouth right
                    ]
                },
                duration=1.0
            ),
            ExpressionType.SURPRISED: Expression(
                name="surprised",
                points=[],
                lines=[
                    *surprised_left,  # Left eye (round)
                    *surprised_right,  # Right eye (round)
                    ((2, 6), (5, 6)),  # O mouth top
                    ((2, 7), (5, 7)),  # O mouth bottom
                    ((2, 6), (2, 7)),  # O mouth left
                    ((5, 6), (5, 7))   # O mouth right
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *surprised_left, *surprised_right,  # Eyes
                        ((2, 5), (3, 5)),  # Mouth left
                        ((4, 5), (5, 5)),  # Mouth right
                        ((2, 6), (3, 6)),  # Mouth bottom left
                        ((4, 6), (5, 6)),  # Mouth bottom right
                        ((2, 5), (2, 6)),  # Left side
                        ((5, 5), (5, 6))   # Right side
                    ],
                    TalkState.CLOSED: [
                        *surprised_left, *surprised_right,  # Eyes
                        ((2, 6), (5, 6)),  # O mouth top
                        ((2, 7), (5, 7)),  # O mouth bottom
                        ((2, 6), (2, 7)),  # O mouth left
                        ((5, 6), (5, 7))   # O mouth right
                    ],
                    TalkState.PARTIAL: [
                        *surprised_left, *surprised_right,  # Eyes
                        ((2, 6), (5, 6)),  # O mouth top
                        ((2, 7), (5, 7)),  # O mouth bottom
                        ((2, 6), (2, 7)),  # O mouth left
                        ((5, 6), (5, 7)),  # O mouth right
                        ((2, 5), (3, 5)),  # Mouth left
                        ((4, 5), (5, 5))   # Mouth right
                    ]
                },
                duration=1.0
            ),
            ExpressionType.WINK: Expression(
                name="wink",
                points=[],
                lines=[
                    *wink_left,  # Left eye (wink)
                    *wink_right,  # Right eye (happy)
                    ((1, 6), (6, 6)),  # Smile top
                    # ((2, 7), (5, 7)),  # Smile bottom
                    ((1, 6), (2, 7)),  # Left curve
                    ((5, 7), (6, 6))   # Right curve
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *wink_left, *wink_right,  # Eyes
                        ((1, 5), (2, 5)),  # Mouth left
                        ((5, 5), (6, 5)),  # Mouth right
                        ((1, 6), (2, 6)),  # Mouth bottom left
                        ((5, 6), (6, 6)),  # Mouth bottom right
                        ((1, 5), (2, 6)),  # Left curve
                        ((5, 6), (6, 5))   # Right curve
                    ],
                    TalkState.CLOSED: [
                        *wink_left, *wink_right,  # Eyes
                        ((1, 6), (6, 6)),  # Smile top
                        # ((2, 7), (5, 7)),  # Smile bottom
                        ((1, 6), (2, 7)),  # Left curve
                        ((5, 7), (6, 6))   # Right curve
                    ],
                    TalkState.PARTIAL: [
                        *wink_left, *wink_right,  # Eyes
                        ((1, 6), (6, 6)),  # Smile top
                        ((2, 7), (5, 7)),  # Smile bottom
                        ((1, 6), (2, 7)),  # Left curve
                        ((5, 7), (6, 6)),  # Right curve
                        ((1, 5), (2, 5)),  # Mouth left
                        ((5, 5), (6, 5))   # Mouth right
                    ]
                },
                duration=1.0
            ),
            ExpressionType.NEUTRAL: Expression(
                name="neutral",
                points=[],
                lines=[
                    *neutral_left,  # Left eye (dot)
                    *neutral_right,  # Right eye (dot)
                    ((2, 6), (5, 6))   # Straight line mouth
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *neutral_left, *neutral_right,  # Eyes
                        ((2, 5), (3, 5)),  # Mouth left
                        ((4, 5), (5, 5))   # Mouth right
                    ],
                    TalkState.CLOSED: [
                        *neutral_left, *neutral_right,  # Eyes
                        ((2, 6), (5, 6))  # Mouth closed
                    ],
                    TalkState.PARTIAL: [
                        *neutral_left, *neutral_right,  # Eyes
                        ((2, 5), (3, 5)),  # Mouth left
                        ((4, 5), (5, 5)),  # Mouth right
                        ((2, 6), (5, 6))   # Mouth bottom
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
                    ((1, 6), (6, 6)),  # Angry mouth top
                    ((2, 5), (3, 5)),  # Angry mouth left
                    ((4, 5), (5, 5)),  # Angry mouth right
                    ((1, 6), (2, 5)),  # Left curve
                    ((5, 5), (6, 6))   # Right curve
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *angry_left, *angry_right,  # Eyes
                        ((1, 5), (2, 5)),  # Mouth left
                        ((5, 5), (6, 5)),  # Mouth right
                        ((1, 6), (2, 6)),  # Mouth bottom left
                        ((5, 6), (6, 6)),  # Mouth bottom right
                        ((1, 5), (2, 6)),  # Left curve
                        ((5, 6), (6, 5))   # Right curve
                    ],
                    TalkState.CLOSED: [
                        *angry_left, *angry_right,  # Eyes
                        ((1, 6), (6, 6)),  # Angry mouth top
                        ((2, 5), (3, 5)),  # Angry mouth left
                        ((4, 5), (5, 5)),  # Angry mouth right
                        ((1, 6), (2, 5)),  # Left curve
                        ((5, 5), (6, 6))   # Right curve
                    ],
                    TalkState.PARTIAL: [
                        *angry_left, *angry_right,  # Eyes
                        ((1, 6), (6, 6)),  # Angry mouth top
                        ((2, 5), (3, 5)),  # Angry mouth left
                        ((4, 5), (5, 5)),  # Angry mouth right
                        ((1, 6), (2, 5)),  # Left curve
                        ((5, 5), (6, 6)),  # Right curve
                        ((1, 5), (2, 5)),  # Mouth left
                        ((5, 5), (6, 5))   # Mouth right
                    ]
                },
                duration=1.0
            ),
            ExpressionType.SLEEPING: Expression(
                name="sleeping",
                points=[],
                lines=[
                    *sleeping_left,  # Left eye (with Z)
                    *sleeping_right,  # Right eye (with Z)
                    ((2, 6), (5, 6))   # Mouth
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *sleeping_left, *sleeping_right,  # Eyes
                        ((2, 5), (3, 5)),  # Mouth left
                        ((4, 5), (5, 5))   # Mouth right
                    ],
                    TalkState.CLOSED: [
                        *sleeping_left, *sleeping_right,  # Eyes
                        ((2, 6), (5, 6))  # Mouth closed
                    ],
                    TalkState.PARTIAL: [
                        *sleeping_left, *sleeping_right,  # Eyes
                        ((2, 5), (3, 5)),  # Mouth left
                        ((4, 5), (5, 5)),  # Mouth right
                        ((2, 6), (5, 6))   # Mouth bottom
                    ]
                },
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