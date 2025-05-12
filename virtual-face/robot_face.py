"""Main robot face class that coordinates facial expressions and speech."""

from typing import Optional
import time

from .display import MatrixDisplay
from .expressions import FacialExpressions
from .speech import SpeechEngine
from .types import ExpressionType

class RobotFace:
    """Main class coordinating facial expressions and speech."""
    def __init__(
        self,
        cascaded: int = 1,
        block_orientation: int = 0,
        rotate: int = 0,
        blocks_arranged_in_reverse_order: bool = False,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> None:
        self.display = MatrixDisplay(
            cascaded=cascaded,
            block_orientation=block_orientation,
            rotate=rotate,
            blocks_arranged_in_reverse_order=blocks_arranged_in_reverse_order,
            width=width,
            height=height
        )
        self.expressions = FacialExpressions(self.display)
        self.speech = SpeechEngine(self.display, self.expressions)

    def display_expression(
        self,
        expression_type: ExpressionType,
        duration: Optional[float] = None,
        scroll: bool = False
    ) -> None:
        """Display a facial expression."""
        expression = self.expressions.get_expression(expression_type)
        display_duration = duration if duration is not None else expression.duration
        
        if scroll:
            for offset in range(self.display.device.width):
                self.display.virtual.set_position((offset, 0))
                self.expressions.draw_expression(expression_type)
                time.sleep(0.1)
        else:
            self.expressions.draw_expression(expression_type)
            time.sleep(display_duration)

    def animate_transition(
        self,
        from_expression: ExpressionType,
        to_expression: ExpressionType,
        steps: int = 10,
        duration: float = 1.0
    ) -> None:
        """Animate a transition between expressions."""
        self.expressions.animate_transition(from_expression, to_expression, steps, duration)

    def talk(
        self,
        expression_type: ExpressionType,
        duration: float = 2.0,
        words_per_minute: int = 150
    ) -> None:
        """Animate talking."""
        self.speech.talk(expression_type, duration, words_per_minute)

    def say_phrase(
        self,
        expression_type: ExpressionType,
        phrase: str,
        words_per_minute: int = 150
    ) -> None:
        """Say a specific phrase."""
        self.speech.say_phrase(expression_type, phrase, words_per_minute)

    def clear(self) -> None:
        """Clear the display."""
        self.display.clear()

    def set_brightness(self, intensity: int) -> None:
        """Set the display brightness."""
        self.display.set_brightness(intensity)

    def demo(self) -> None:
        """Run a demo of all features."""
        expressions = list(ExpressionType)
        
        # Show expressions and transitions
        for i in range(len(expressions)):
            current = expressions[i]
            next_expr = expressions[(i + 1) % len(expressions)]
            
            print(f"Displaying {current.name} expression...")
            self.display_expression(current, duration=1.0)
            
            print(f"Transitioning to {next_expr.name}...")
            self.animate_transition(current, next_expr, steps=10, duration=0.5)
        
        # Demonstrate talking
        print("\nDemonstrating talking...")
        try:
            self.say_phrase(ExpressionType.HAPPY, "Hello! I am a happy robot!")
            self.say_phrase(ExpressionType.NEUTRAL, "I can talk with different expressions.")
            self.say_phrase(ExpressionType.SURPRISED, "Wow! This is so much fun!")
        except ValueError as e:
            print(f"Note: {e}")

if __name__ == "__main__":
    face = RobotFace()
    try:
        face.demo()
    except KeyboardInterrupt:
        face.clear()
        print("\nDemo stopped by user") 