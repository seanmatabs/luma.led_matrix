"""Facial expressions manager for the robot face."""

from typing import Dict, List, Tuple, Set
import time

from .face_types import ExpressionType, Expression, TalkState
from .display import DisplayInterface

class FacialExpressions:
    """Manages facial expressions and their rendering."""
    def __init__(self, display: DisplayInterface) -> None:
        self.display = display

        # === Helper functions (all inside __init__) ===
        def round_eye(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y+1), (x+1, y+1)), ((x, y), (x+1, y)), ((x, y), (x, y+1)), ((x+1, y), (x+1, y+1)), ((x, y), (x+1, y+1)), ((x+1, y), (x, y+1))]
        def round_x_eye(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y), (x+1, y+1)), ((x+1, y), (x, y+1)), ((x, y), (x, y+1)), ((x+1, y), (x+1, y+1))]
        def round_slant_eye_left(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y+1), (x+1, y)), ((x, y), (x, y+1)), ((x+1, y), (x+1, y+1))]
        def round_slant_eye_right(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y), (x+1, y+1)), ((x, y), (x, y+1)), ((x+1, y), (x+1, y+1))]
        def round_closed_eye(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y+1), (x+1, y+1)), ((x, y), (x+1, y))]
        def round_arc_eye(x: int, y: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
            return [((x, y+1), (x+1, y)), ((x+1, y), (x+2, y+1)), ((x, y+1), (x+2, y+1))]

        # Eye positions
        left_eye_x, right_eye_x, eye_y = 1, 5, 1

        # Eyes for each expression
        round_left = round_eye(left_eye_x, eye_y)
        round_right = round_eye(right_eye_x, eye_y)
        round_x_left = round_x_eye(left_eye_x, eye_y)
        round_x_right = round_x_eye(right_eye_x, eye_y)
        round_slant_left = round_slant_eye_left(left_eye_x, eye_y)
        round_slant_right = round_slant_eye_right(right_eye_x, eye_y)
        round_closed_left = round_closed_eye(left_eye_x, eye_y)
        round_closed_right = round_closed_eye(right_eye_x, eye_y)
        round_arc_left = round_arc_eye(left_eye_x, eye_y)
        round_arc_right = round_arc_eye(right_eye_x, eye_y)

        # Mouth helpers (3 rows: 5, 6, 7)
        def smile():
            return [((1, 7), (2, 6)), ((2, 6), (3, 5)), ((3, 5), (4, 5)), ((4, 5), (5, 6)), ((5, 6), (6, 7))]
        def frown():
            return [((1, 5), (2, 6)), ((2, 6), (3, 7)), ((3, 7), (4, 7)), ((4, 7), (5, 6)), ((5, 6), (6, 5))]
        def straight():
            return [((1, 6), (6, 6)), ((2, 7), (5, 7))]
        def open_mouth():
            return [((2, 5), (2, 7)), ((5, 5), (5, 7)), ((2, 7), (5, 7)), ((2, 5), (5, 5))]
        def gritted():
            return [((1, 5), (6, 5)), ((1, 6), (6, 6)), ((1, 7), (6, 7)), ((1, 5), (1, 7)), ((3, 5), (3, 7)), ((5, 5), (5, 7))]
        def o_mouth():
            return [((3, 5), (4, 5)), ((3, 7), (4, 7)), ((3, 5), (3, 7)), ((4, 5), (4, 7)), ((2, 6), (5, 6))]
        def wink_mouth():
            return [((2, 7), (5, 7)), ((1, 6), (2, 7)), ((5, 7), (6, 6)), ((3, 6), (4, 6))]
        def sleep_mouth():
            return [((2, 7), (5, 7)), ((3, 6), (4, 6))]

        # === All assignments to self.expressions[...] here ===
        self.expressions = {}
        self.expressions[ExpressionType.NEUTRAL] = Expression(
            name="neutral",
            points=[],
            lines=[*round_left, *round_right, *straight()],
            talk_lines={
                TalkState.OPEN: [*round_left, *round_right, ((1, 6), (2, 6)), ((5, 6), (6, 6)), ((2, 7), (2, 7)), ((5, 7), (5, 7))],
                TalkState.CLOSED: [*round_left, *round_right, *straight()],
                TalkState.PARTIAL: [*round_left, *round_right, ((1, 6), (3, 6)), ((4, 6), (6, 6)), ((2, 7), (5, 7))]
            },
            duration=1.0
        )
        self.expressions[ExpressionType.HAPPY] = Expression(
            name="happy",
            points=[],
            lines=[*round_left, *round_right, *smile()],
            talk_lines={
                TalkState.OPEN: [*round_left, *round_right, ((1, 7), (2, 7)), ((5, 7), (6, 7)), ((3, 6), (4, 6))],
                TalkState.CLOSED: [*round_left, *round_right, *smile()],
                TalkState.PARTIAL: [*round_left, *round_right, ((1, 7), (3, 6)), ((4, 6), (6, 7)), ((3, 7), (4, 7))]
            },
            duration=1.0
        )
        self.expressions[ExpressionType.SAD] = Expression(
            name="sad",
            points=[],
            lines=[*round_x_left, *round_x_right, *frown()],
            talk_lines={
                TalkState.OPEN: [*round_x_left, *round_x_right, ((1, 5), (2, 5)), ((5, 5), (6, 5)), ((3, 6), (4, 6))],
                TalkState.CLOSED: [*round_x_left, *round_x_right, *frown()],
                TalkState.PARTIAL: [*round_x_left, *round_x_right, ((1, 5), (3, 6)), ((4, 6), (6, 5)), ((3, 5), (4, 5))]
            },
            duration=1.0
        )
        self.expressions[ExpressionType.ANGRY] = Expression(
            name="angry",
            points=[],
            lines=[*round_slant_left, *round_slant_right, *gritted()],
            talk_lines={
                TalkState.OPEN: [*round_slant_left, *round_slant_right, ((1, 7), (2, 7)), ((5, 7), (6, 7)), ((3, 6), (4, 6))],
                TalkState.CLOSED: [*round_slant_left, *round_slant_right, *gritted()],
                TalkState.PARTIAL: [*round_slant_left, *round_slant_right, ((1, 7), (3, 7)), ((4, 7), (6, 7)), ((3, 6), (4, 6))]
            },
            duration=1.0
        )
        self.expressions[ExpressionType.SURPRISED] = Expression(
            name="surprised",
            points=[],
            lines=[*round_left, *round_right, *o_mouth()],
            talk_lines={
                TalkState.OPEN: [*round_left, *round_right, ((3, 7), (4, 7)), ((2, 6), (2, 6)), ((5, 6), (5, 6))],
                TalkState.CLOSED: [*round_left, *round_right, *o_mouth()],
                TalkState.PARTIAL: [*round_left, *round_right, ((3, 5), (4, 5)), ((3, 7), (4, 7)), ((2, 6), (5, 6))]
            },
            duration=1.0
        )
        self.expressions[ExpressionType.WINK] = Expression(
            name="wink",
            points=[],
            lines=[*round_closed_left, *round_right, *wink_mouth()],
            talk_lines={
                TalkState.OPEN: [*round_closed_left, *round_right, ((2, 7), (3, 7)), ((4, 7), (5, 7)), ((3, 6), (4, 6))],
                TalkState.CLOSED: [*round_closed_left, *round_right, *wink_mouth()],
                TalkState.PARTIAL: [*round_closed_left, *round_right, ((2, 7), (5, 7)), ((3, 6), (4, 6))]
            },
            duration=1.0
        )
        self.expressions[ExpressionType.SLEEPING] = Expression(
            name="sleeping",
            points=[],
            lines=[*round_arc_left, *round_arc_right, *sleep_mouth()],
            talk_lines={
                TalkState.OPEN: [*round_arc_left, *round_arc_right, ((2, 7), (3, 7)), ((4, 7), (5, 7)), ((3, 6), (4, 6))],
                TalkState.CLOSED: [*round_arc_left, *round_arc_right, *sleep_mouth()],
                TalkState.PARTIAL: [*round_arc_left, *round_arc_right, ((2, 7), (5, 7)), ((3, 6), (4, 6))]
            },
            duration=1.0
        )

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