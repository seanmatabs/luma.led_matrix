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

        # Eye helpers for 2x2 block and X shape
        def create_eye_block(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y), (x+1, y)), ((x, y+1), (x+1, y+1))]

        def create_eye_x(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y), (x+1, y+1)), ((x+1, y), (x, y+1))]

        # Eye positions
        left_eye_x, right_eye_x, eye_y = 1, 5, 1

        # Normal/Happy eyes: 2x2 blocks
        normal_left_eye = create_eye_block(left_eye_x, eye_y)
        normal_right_eye = create_eye_block(right_eye_x, eye_y)
        # Sad eyes: X shapes
        sad_left_eye = create_eye_x(left_eye_x, eye_y)
        sad_right_eye = create_eye_x(right_eye_x, eye_y)
        # Angry eyes: Diagonal lines
        angry_left_eye = [((left_eye_x, eye_y+1), (left_eye_x+1, eye_y))]
        angry_right_eye = [((right_eye_x, eye_y), (right_eye_x+1, eye_y+1))]

        # Mouths
        # Normal: straight line at y=6
        normal_mouth = [((1, 6), (6, 6))]
        # Happy: upward curve (corners at bottom)
        happy_mouth = [((1, 7), (2, 6)), ((2, 6), (3, 6)), ((3, 6), (4, 7)), ((4, 7), (5, 6)), ((5, 6), (6, 7))]
        # Sad: downward curve (corners at bottom)
        sad_mouth = [((1, 7), (2, 6)), ((2, 6), (3, 7)), ((3, 7), (4, 6)), ((4, 6), (5, 7)), ((5, 7), (6, 6))]
        # Angry: two stacked lines at y=6, y=7
        angry_mouth = [((1, 6), (6, 6)), ((1, 7), (6, 7))]

        self.expressions: Dict[ExpressionType, Expression] = {
            ExpressionType.HAPPY: Expression(
                name="happy",
                points=[],
                lines=[*normal_left_eye, *normal_right_eye, *happy_mouth],
                talk_lines={
                    TalkState.OPEN: [*normal_left_eye, *normal_right_eye, ((1, 7), (2, 6)), ((5, 6), (6, 7))],
                    TalkState.CLOSED: [*normal_left_eye, *normal_right_eye, *happy_mouth],
                    TalkState.PARTIAL: [*normal_left_eye, *normal_right_eye, ((1, 7), (3, 6)), ((4, 6), (6, 7))]
                },
                duration=1.0
            ),
            ExpressionType.SAD: Expression(
                name="sad",
                points=[],
                lines=[*sad_left_eye, *sad_right_eye, *sad_mouth],
                talk_lines={
                    TalkState.OPEN: [*sad_left_eye, *sad_right_eye, ((1, 7), (2, 6)), ((5, 7), (6, 6))],
                    TalkState.CLOSED: [*sad_left_eye, *sad_right_eye, *sad_mouth],
                    TalkState.PARTIAL: [*sad_left_eye, *sad_right_eye, ((1, 7), (3, 7)), ((4, 7), (6, 6))]
                },
                duration=1.0
            ),
            ExpressionType.SURPRISED: Expression(
                name="surprised",
                points=[],
                lines=[
                    *normal_left_eye,  # Left eye (normal)
                    *normal_right_eye,  # Right eye (normal)
                    ((2, 6), (5, 6)),  # O mouth top
                    ((2, 7), (5, 7)),  # O mouth bottom
                    ((2, 6), (2, 7)),  # O mouth left
                    ((5, 6), (5, 7))   # O mouth right
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *normal_left_eye, *normal_right_eye,  # Eyes
                        ((2, 5), (3, 5)),  # Mouth left
                        ((4, 5), (5, 5)),  # Mouth right
                        ((2, 6), (3, 6)),  # Mouth bottom left
                        ((4, 6), (5, 6)),  # Mouth bottom right
                        ((2, 5), (2, 6)),  # Left side
                        ((5, 5), (5, 6))   # Right side
                    ],
                    TalkState.CLOSED: [
                        *normal_left_eye, *normal_right_eye,  # Eyes
                        ((2, 6), (5, 6)),  # O mouth top
                        ((2, 7), (5, 7)),  # O mouth bottom
                        ((2, 6), (2, 7)),  # O mouth left
                        ((5, 6), (5, 7))   # O mouth right
                    ],
                    TalkState.PARTIAL: [
                        *normal_left_eye, *normal_right_eye,  # Eyes
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
                    *normal_left_eye,  # Left eye (normal)
                    *normal_right_eye,  # Right eye (normal)
                    ((1, 6), (6, 6)),  # Smile top
                    ((2, 7), (5, 7)),  # Smile bottom
                    ((1, 6), (2, 7)),  # Left curve
                    ((5, 7), (6, 6))   # Right curve
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *normal_left_eye, *normal_right_eye,  # Eyes
                        ((1, 5), (2, 5)),  # Mouth left
                        ((5, 5), (6, 5)),  # Mouth right
                        ((1, 6), (2, 6)),  # Mouth bottom left
                        ((5, 6), (6, 6)),  # Mouth bottom right
                        ((1, 5), (2, 6)),  # Left curve
                        ((5, 6), (6, 5))   # Right curve
                    ],
                    TalkState.CLOSED: [
                        *normal_left_eye, *normal_right_eye,  # Eyes
                        ((1, 6), (6, 6)),  # Smile top
                        ((2, 7), (5, 7)),  # Smile bottom
                        ((1, 6), (2, 7)),  # Left curve
                        ((5, 7), (6, 6))   # Right curve
                    ],
                    TalkState.PARTIAL: [
                        *normal_left_eye, *normal_right_eye,  # Eyes
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
                lines=[*normal_left_eye, *normal_right_eye, *normal_mouth],
                talk_lines={
                    TalkState.OPEN: [*normal_left_eye, *normal_right_eye, ((1, 6), (2, 6)), ((5, 6), (6, 6))],
                    TalkState.CLOSED: [*normal_left_eye, *normal_right_eye, *normal_mouth],
                    TalkState.PARTIAL: [*normal_left_eye, *normal_right_eye, ((1, 6), (3, 6)), ((4, 6), (6, 6))]
                },
                duration=1.0
            ),
            ExpressionType.ANGRY: Expression(
                name="angry",
                points=[],
                lines=[*angry_left_eye, *angry_right_eye, *angry_mouth],
                talk_lines={
                    TalkState.OPEN: [*angry_left_eye, *angry_right_eye, ((1, 6), (2, 6)), ((5, 7), (6, 7))],
                    TalkState.CLOSED: [*angry_left_eye, *angry_right_eye, *angry_mouth],
                    TalkState.PARTIAL: [*angry_left_eye, *angry_right_eye, ((1, 6), (3, 6)), ((4, 7), (6, 7))]
                },
                duration=1.0
            ),
            ExpressionType.SLEEPING: Expression(
                name="sleeping",
                points=[],
                lines=[
                    *normal_left_eye,  # Left eye (normal)
                    *normal_right_eye,  # Right eye (normal)
                    ((2, 6), (5, 6))   # Mouth
                ],
                talk_lines={
                    TalkState.OPEN: [
                        *normal_left_eye, *normal_right_eye,  # Eyes
                        ((2, 5), (3, 5)),  # Mouth left
                        ((4, 5), (5, 5))   # Mouth right
                    ],
                    TalkState.CLOSED: [
                        *normal_left_eye, *normal_right_eye,  # Eyes
                        ((2, 6), (5, 6))  # Mouth closed
                    ],
                    TalkState.PARTIAL: [
                        *normal_left_eye, *normal_right_eye,  # Eyes
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