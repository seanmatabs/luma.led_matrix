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

        # Create eye rectangles for all expressions
        left_eye = create_eye(1, 1)  # Left eye at (1,1) to (3,2)
        right_eye = create_eye(4, 1)  # Right eye at (4,1) to (6,2)

        self.expressions: Dict[ExpressionType, Expression] = {
            ExpressionType.HAPPY: Expression(
                name="happy",
                points=[],  # No points, using rectangles for eyes
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
                    ((1, 1), (3, 2)),  # Left eye (wink)
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
                    ((1, 1), (3, 2)),  # Left eye (sleeping)
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
        steps: int = 20,  # Increased from 10 to 20 for smoother transition
        duration: float = 0.8  # Slightly longer duration
    ) -> None:
        """Animate a transition between two expressions."""
        if from_expression not in self.expressions or to_expression not in self.expressions:
            raise ValueError("Invalid expression type")
            
        step_duration = duration / steps
        last_draw_time = time.time()
        
        for i in range(steps + 1):
            # Calculate time since last draw
            current_time = time.time()
            elapsed = current_time - last_draw_time
            
            # If we're ahead of schedule, wait
            if elapsed < step_duration:
                time.sleep(step_duration - elapsed)
            
            progress = i / steps
            self.display.clear()
            
            # Interpolate lines with easing function for smoother motion
            if (self.expressions[from_expression].lines and 
                self.expressions[to_expression].lines):
                # Use smoothstep easing function
                eased_progress = progress * progress * (3 - 2 * progress)
                
                for (start1, end1), (start2, end2) in zip(
                    self.expressions[from_expression].lines,
                    self.expressions[to_expression].lines
                ):
                    start_x = int(start1[0] + (start2[0] - start1[0]) * eased_progress)
                    start_y = int(start1[1] + (start2[1] - start1[1]) * eased_progress)
                    end_x = int(end1[0] + (end2[0] - end1[0]) * eased_progress)
                    end_y = int(end1[1] + (end2[1] - end1[1]) * eased_progress)
                    self.display.draw_lines([((start_x, start_y), (end_x, end_y))])
            
            last_draw_time = time.time() 