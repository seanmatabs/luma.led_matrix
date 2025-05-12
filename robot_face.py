#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import time
from enum import Enum, auto

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219

class ExpressionType(Enum):
    """Enum for different types of facial expressions."""
    HAPPY = auto()
    SAD = auto()
    SURPRISED = auto()
    WINK = auto()
    NEUTRAL = auto()
    ANGRY = auto()
    SLEEPING = auto()

@dataclass
class Expression:
    """Represents a facial expression with its drawing instructions."""
    name: str
    points: List[Tuple[int, int]]
    lines: List[Tuple[Tuple[int, int], Tuple[int, int]]] = None
    duration: float = 1.0

class RobotFace:
    def __init__(
        self,
        cascaded: int = 1,
        block_orientation: int = 0,
        rotate: int = 0,
        blocks_arranged_in_reverse_order: bool = False,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> None:
        """Initialize the robot face display.
        
        Args:
            cascaded: Number of cascaded MAX7219 LED matrices
            block_orientation: Corrects block orientation (0, 90, -90)
            rotate: Rotate display (0=0°, 1=90°, 2=180°, 3=270°)
            blocks_arranged_in_reverse_order: Set to true if blocks are in reverse order
            width: Optional width for custom matrix arrangement
            height: Optional height for custom matrix arrangement
        """
        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(
            serial,
            cascaded=cascaded,
            block_orientation=block_orientation,
            rotate=rotate,
            blocks_arranged_in_reverse_order=blocks_arranged_in_reverse_order,
            width=width,
            height=height
        )
        
        # Create a virtual viewport for smooth animations
        self.virtual = viewport(self.device, width=self.device.width, height=self.device.height)
        
        # Define facial expressions
        self.expressions: Dict[ExpressionType, Expression] = {
            ExpressionType.HAPPY: Expression(
                name="happy",
                points=[(2, 2), (5, 2)],  # Eyes
                lines=[((1, 5), (6, 5)), ((2, 6), (5, 6))],  # Smile
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

    def _draw_expression(self, expression: Expression) -> None:
        """Draw an expression on the virtual viewport.
        
        Args:
            expression: The expression to draw
        """
        with canvas(self.virtual) as draw:
            # Clear the display
            draw.rectangle(self.device.bounding_box, outline="black", fill="black")
            
            # Draw points (eyes)
            for point in expression.points:
                draw.point(point, fill="white")
            
            # Draw lines (mouth, etc.)
            if expression.lines:
                for start, end in expression.lines:
                    draw.line([start, end], fill="white")

    def display_expression(
        self,
        expression_type: ExpressionType,
        duration: Optional[float] = None,
        scroll: bool = False
    ) -> None:
        """Display a facial expression on the LED matrix.
        
        Args:
            expression_type: Type of expression to display
            duration: Optional duration to display the expression
            scroll: Whether to scroll the expression
        """
        if expression_type not in self.expressions:
            raise ValueError(f"Unknown expression: {expression_type}")
            
        expression = self.expressions[expression_type]
        display_duration = duration if duration is not None else expression.duration
        
        if scroll:
            # Create a scrolling animation
            for offset in range(self.device.width):
                self.virtual.set_position((offset, 0))
                self._draw_expression(expression)
                time.sleep(0.1)
        else:
            self._draw_expression(expression)
            time.sleep(display_duration)

    def animate_transition(
        self,
        from_expression: ExpressionType,
        to_expression: ExpressionType,
        steps: int = 10,
        duration: float = 1.0
    ) -> None:
        """Animate a transition between two expressions.
        
        Args:
            from_expression: Starting expression
            to_expression: Ending expression
            steps: Number of animation steps
            duration: Total duration of animation
        """
        if from_expression not in self.expressions or to_expression not in self.expressions:
            raise ValueError("Invalid expression type")
            
        step_duration = duration / steps
        for i in range(steps + 1):
            # Calculate intermediate position
            progress = i / steps
            with canvas(self.virtual) as draw:
                draw.rectangle(self.device.bounding_box, outline="black", fill="black")
                
                # Draw points with interpolation
                for p1, p2 in zip(
                    self.expressions[from_expression].points,
                    self.expressions[to_expression].points
                ):
                    x = int(p1[0] + (p2[0] - p1[0]) * progress)
                    y = int(p1[1] + (p2[1] - p1[1]) * progress)
                    draw.point((x, y), fill="white")
                
                # Draw lines with interpolation
                if self.expressions[from_expression].lines and self.expressions[to_expression].lines:
                    for (start1, end1), (start2, end2) in zip(
                        self.expressions[from_expression].lines,
                        self.expressions[to_expression].lines
                    ):
                        start_x = int(start1[0] + (start2[0] - start1[0]) * progress)
                        start_y = int(start1[1] + (start2[1] - start1[1]) * progress)
                        end_x = int(end1[0] + (end2[0] - end1[0]) * progress)
                        end_y = int(end1[1] + (end2[1] - end1[1]) * progress)
                        draw.line([(start_x, start_y), (end_x, end_y)], fill="white")
            
            time.sleep(step_duration)

    def clear(self) -> None:
        """Clear the display."""
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="black", fill="black")

    def set_brightness(self, intensity: int) -> None:
        """Set the brightness of the display.
        
        Args:
            intensity: Brightness level (0-15)
        """
        if not 0 <= intensity <= 15:
            raise ValueError("Intensity must be between 0 and 15")
        self.device.contrast(intensity * 16)

    def demo(self) -> None:
        """Run a demo of all facial expressions with transitions."""
        expressions = list(ExpressionType)
        for i in range(len(expressions)):
            current = expressions[i]
            next_expr = expressions[(i + 1) % len(expressions)]
            
            print(f"Displaying {current.name} expression...")
            self.display_expression(current, duration=1.0)
            
            print(f"Transitioning to {next_expr.name}...")
            self.animate_transition(current, next_expr, steps=10, duration=0.5)

if __name__ == "__main__":
    # Example usage
    face = RobotFace()
    try:
        face.demo()
    except KeyboardInterrupt:
        face.clear()
        print("\nDemo stopped by user") 