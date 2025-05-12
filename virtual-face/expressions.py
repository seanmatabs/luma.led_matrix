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

        # Eye helpers
        def block_eye(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y), (x+1, y)), ((x, y+1), (x+1, y+1))]
        def x_eye(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y), (x+1, y+1)), ((x+1, y), (x, y+1))]
        def slant_eye_left(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y+1), (x+1, y))]
        def slant_eye_right(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y), (x+1, y+1))]
        def closed_eye(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y+1), (x+1, y+1))]
        def arc_eye(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y+1), (x+1, y)), ((x+1, y), (x+2, y+1))]

        # Eye positions
        left_eye_x, right_eye_x, eye_y = 1, 5, 1

        # Eyes for each expression
        block_left = block_eye(left_eye_x, eye_y)
        block_right = block_eye(right_eye_x, eye_y)
        x_left = x_eye(left_eye_x, eye_y)
        x_right = x_eye(right_eye_x, eye_y)
        slant_left = slant_eye_left(left_eye_x, eye_y)
        slant_right = slant_eye_right(right_eye_x, eye_y)
        closed_left = closed_eye(left_eye_x, eye_y)
        closed_right = closed_eye(right_eye_x, eye_y)
        arc_left = arc_eye(left_eye_x, eye_y)
        arc_right = arc_eye(right_eye_x, eye_y)

        # Mouth helpers
        def smile():
            return [((1, 6), (2, 7)), ((2, 7), (5, 7)), ((5, 7), (6, 6))]
        def frown():
            return [((1, 7), (2, 6)), ((2, 6), (5, 6)), ((5, 6), (6, 7))]
        def straight():
            return [((1, 7), (6, 7))]
        def open_mouth():
            return [((2, 6), (2, 7)), ((5, 6), (5, 7)), ((2, 7), (5, 7)), ((2, 6), (5, 6))]
        def gritted():
            return [((1, 6), (6, 6)), ((1, 7), (6, 7)), ((1, 6), (1, 7)), ((3, 6), (3, 7)), ((5, 6), (5, 7))]
        def o_mouth():
            return [((3, 6), (4, 6)), ((3, 7), (4, 7)), ((3, 6), (3, 7)), ((4, 6), (4, 7))]
        def wink_mouth():
            return [((2, 7), (5, 7)), ((1, 6), (2, 7)), ((5, 7), (6, 6))]
        def sleep_mouth():
            return [((2, 7), (5, 7))]

        self.expressions: Dict[ExpressionType, Expression] = {
            ExpressionType.HAPPY: Expression(
                name="happy",
                points=[],
                lines=[*block_left, *block_right, *smile()],
                talk_lines={
                    TalkState.OPEN: [*block_left, *block_right, ((1, 7), (2, 7)), ((5, 7), (6, 7))],
                    TalkState.CLOSED: [*block_left, *block_right, *smile()],
                    TalkState.PARTIAL: [*block_left, *block_right, ((1, 7), (3, 7)), ((4, 7), (6, 7))]
                },
                duration=1.0
            ),
            ExpressionType.SAD: Expression(
                name="sad",
                points=[],
                lines=[*x_left, *x_right, *frown()],
                talk_lines={
                    TalkState.OPEN: [*x_left, *x_right, ((1, 6), (2, 6)), ((5, 6), (6, 6))],
                    TalkState.CLOSED: [*x_left, *x_right, *frown()],
                    TalkState.PARTIAL: [*x_left, *x_right, ((1, 6), (3, 6)), ((4, 6), (6, 6))]
                },
                duration=1.0
            ),
            ExpressionType.SURPRISED: Expression(
                name="surprised",
                points=[],
                lines=[*block_left, *block_right, *o_mouth()],
                talk_lines={
                    TalkState.OPEN: [*block_left, *block_right, ((3, 7), (4, 7))],
                    TalkState.CLOSED: [*block_left, *block_right, *o_mouth()],
                    TalkState.PARTIAL: [*block_left, *block_right, ((3, 6), (4, 6)), ((3, 7), (4, 7))]
                },
                duration=1.0
            ),
            ExpressionType.WINK: Expression(
                name="wink",
                points=[],
                lines=[*closed_left, *block_right, *wink_mouth()],
                talk_lines={
                    TalkState.OPEN: [*closed_left, *block_right, ((2, 7), (3, 7)), ((4, 7), (5, 7))],
                    TalkState.CLOSED: [*closed_left, *block_right, *wink_mouth()],
                    TalkState.PARTIAL: [*closed_left, *block_right, ((2, 7), (5, 7))]
                },
                duration=1.0
            ),
            ExpressionType.NEUTRAL: Expression(
                name="neutral",
                points=[],
                lines=[*block_left, *block_right, *straight()],
                talk_lines={
                    TalkState.OPEN: [*block_left, *block_right, ((1, 7), (2, 7)), ((5, 7), (6, 7))],
                    TalkState.CLOSED: [*block_left, *block_right, *straight()],
                    TalkState.PARTIAL: [*block_left, *block_right, ((1, 7), (3, 7)), ((4, 7), (6, 7))]
                },
                duration=1.0
            ),
            ExpressionType.ANGRY: Expression(
                name="angry",
                points=[],
                lines=[*slant_left, *slant_right, *gritted()],
                talk_lines={
                    TalkState.OPEN: [*slant_left, *slant_right, ((1, 7), (2, 7)), ((5, 7), (6, 7))],
                    TalkState.CLOSED: [*slant_left, *slant_right, *gritted()],
                    TalkState.PARTIAL: [*slant_left, *slant_right, ((1, 7), (3, 7)), ((4, 7), (6, 7))]
                },
                duration=1.0
            ),
            ExpressionType.SLEEPING: Expression(
                name="sleeping",
                points=[],
                lines=[*arc_left, *arc_right, *sleep_mouth()],
                talk_lines={
                    TalkState.OPEN: [*arc_left, *arc_right, ((2, 7), (3, 7)), ((4, 7), (5, 7))],
                    TalkState.CLOSED: [*arc_left, *arc_right, *sleep_mouth()],
                    TalkState.PARTIAL: [*arc_left, *arc_right, ((2, 7), (5, 7))]
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