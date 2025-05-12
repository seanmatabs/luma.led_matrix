#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Tuple, Optional
from dataclasses import dataclass
import time

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

@dataclass
class Point:
    x: int
    y: int

@dataclass
class FacialExpression:
    name: str
    points: List[Point]
    duration: float = 1.0  # Duration in seconds to display the expression

class RobotFace:
    def __init__(
        self,
        cascaded: int = 1,
        block_orientation: int = 0,
        rotate: int = 0,
        blocks_arranged_in_reverse_order: bool = False
    ) -> None:
        """Initialize the robot face display.
        
        Args:
            cascaded: Number of cascaded MAX7219 LED matrices
            block_orientation: Corrects block orientation (0, 90, -90)
            rotate: Rotate display (0=0°, 1=90°, 2=180°, 3=270°)
            blocks_arranged_in_reverse_order: Set to true if blocks are in reverse order
        """
        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(
            serial,
            cascaded=cascaded,
            block_orientation=block_orientation,
            rotate=rotate,
            blocks_arranged_in_reverse_order=blocks_arranged_in_reverse_order
        )
        
        # Define facial expressions
        self.expressions = {
            'happy': FacialExpression(
                name='happy',
                points=[
                    # Eyes
                    Point(2, 2), Point(5, 2),
                    # Smile
                    Point(1, 5), Point(2, 6), Point(3, 6),
                    Point(4, 6), Point(5, 6), Point(6, 5)
                ]
            ),
            'sad': FacialExpression(
                name='sad',
                points=[
                    # Eyes
                    Point(2, 2), Point(5, 2),
                    # Frown
                    Point(1, 5), Point(2, 4), Point(3, 4),
                    Point(4, 4), Point(5, 4), Point(6, 5)
                ]
            ),
            'surprised': FacialExpression(
                name='surprised',
                points=[
                    # Eyes
                    Point(2, 2), Point(5, 2),
                    # O mouth
                    Point(3, 5), Point(4, 5),
                    Point(3, 6), Point(4, 6)
                ]
            ),
            'wink': FacialExpression(
                name='wink',
                points=[
                    # Left eye (closed)
                    Point(2, 2),
                    # Right eye (open)
                    Point(5, 2),
                    # Smile
                    Point(1, 5), Point(2, 6), Point(3, 6),
                    Point(4, 6), Point(5, 6), Point(6, 5)
                ]
            ),
            'neutral': FacialExpression(
                name='neutral',
                points=[
                    # Eyes
                    Point(2, 2), Point(5, 2),
                    # Straight line mouth
                    Point(2, 5), Point(3, 5), Point(4, 5), Point(5, 5)
                ]
            )
        }

    def display_expression(self, expression_name: str, duration: Optional[float] = None) -> None:
        """Display a facial expression on the LED matrix.
        
        Args:
            expression_name: Name of the expression to display
            duration: Optional duration to display the expression (overrides default)
        """
        if expression_name not in self.expressions:
            raise ValueError(f"Unknown expression: {expression_name}")
            
        expression = self.expressions[expression_name]
        display_duration = duration if duration is not None else expression.duration
        
        with canvas(self.device) as draw:
            for point in expression.points:
                draw.point((point.x, point.y), fill="white")
                
        time.sleep(display_duration)

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
        """Run a demo of all facial expressions."""
        expressions = ['happy', 'sad', 'surprised', 'wink', 'neutral']
        for expression in expressions:
            print(f"Displaying {expression} expression...")
            self.display_expression(expression, duration=2.0)
            time.sleep(0.5)  # Brief pause between expressions

if __name__ == "__main__":
    # Example usage
    face = RobotFace()
    try:
        face.demo()
    except KeyboardInterrupt:
        face.clear()
        print("\nDemo stopped by user") 