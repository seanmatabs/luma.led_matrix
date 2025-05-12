"""Main robot face class that coordinates facial expressions and speech."""

from typing import Optional
import time

from .display import MatrixDisplay
from .expressions import FacialExpressions
from .speech import SpeechEngine
from .face_types import ExpressionType

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
        
        # Enable/disable scroll mode
        self.display.set_scroll_mode(scroll)
        
        if scroll:
            for offset in range(self.display.device.width):
                if self.display.virtual is not None:  # Check if scroll mode is enabled
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
        print("\n=== Robot Face Demo ===")
        
        # Initial brightness setup
        print("\nSetting up display...")
        self.set_brightness(8)  # Medium brightness
        time.sleep(1)
        
        # Show all expressions with transitions
        print("\n1. Expression Showcase:")
        expressions = list(ExpressionType)
        for i in range(len(expressions)):
            current = expressions[i]
            next_expr = expressions[(i + 1) % len(expressions)]
            
            print(f"\nDisplaying {current.name} expression...")
            self.display_expression(current, duration=1.5)
            
            print(f"Transitioning to {next_expr.name}...")
            self.animate_transition(current, next_expr, steps=8, duration=0.4)
        
        # Emotional sequence
        print("\n2. Emotional Sequence:")
        emotional_sequence = [
            (ExpressionType.HAPPY, "I'm so happy to see you!"),
            (ExpressionType.SURPRISED, "Oh! What's that?"),
            (ExpressionType.NEUTRAL, "Hmm, let me think about that."),
            (ExpressionType.SAD, "That makes me a bit sad..."),
            (ExpressionType.ANGRY, "But that's not fair!"),
            (ExpressionType.WINK, "Just kidding! *wink*"),
            (ExpressionType.HAPPY, "I'm actually quite cheerful!")
        ]
        
        for expression, phrase in emotional_sequence:
            print(f"\n{expression.name}: {phrase}")
            self.say_phrase(expression, phrase, words_per_minute=120)
            time.sleep(0.5)
        
        # Sleeping sequence
        print("\n3. Sleeping Sequence:")
        print("Getting sleepy...")
        self.animate_transition(ExpressionType.NEUTRAL, ExpressionType.SLEEPING, steps=5, duration=0.5)
        self.display_expression(ExpressionType.SLEEPING, duration=2.0)
        
        # Wake up sequence
        print("Waking up!")
        self.animate_transition(ExpressionType.SLEEPING, ExpressionType.SURPRISED, steps=5, duration=0.3)
        self.display_expression(ExpressionType.SURPRISED, duration=0.5)
        self.animate_transition(ExpressionType.SURPRISED, ExpressionType.HAPPY, steps=5, duration=0.3)
        
        # Final message
        print("\n4. Final Message:")
        self.say_phrase(
            ExpressionType.HAPPY,
            "Thanks for watching my demo! I hope you enjoyed seeing all my expressions!",
            words_per_minute=130
        )
        
        # Brightness demo
        print("\n5. Brightness Demo:")
        for intensity in [4, 8, 12, 15, 12, 8, 4]:
            print(f"Setting brightness to {intensity}...")
            self.set_brightness(intensity)
            self.display_expression(ExpressionType.HAPPY, duration=0.5)
        
        # Return to neutral
        print("\nReturning to neutral expression...")
        self.animate_transition(ExpressionType.HAPPY, ExpressionType.NEUTRAL, steps=5, duration=0.3)
        self.display_expression(ExpressionType.NEUTRAL, duration=1.0)
        
        print("\n=== Demo Complete ===")

if __name__ == "__main__":
    face = RobotFace()
    try:
        face.demo()
    except KeyboardInterrupt:
        face.clear()
        print("\nDemo stopped by user") 