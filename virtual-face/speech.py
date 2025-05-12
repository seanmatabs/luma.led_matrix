from typing import Generator
import time
import random

from .display import DisplayInterface
from .expressions import FacialExpressions
from .face_types import ExpressionType, TalkState, Expression

class SpeechEngine:
    """Handles speech animation and timing."""
    def __init__(self, display: DisplayInterface, expressions: FacialExpressions) -> None:
        self.display = display
        self.expressions = expressions
        self.states = [TalkState.OPEN, TalkState.PARTIAL, TalkState.CLOSED]
        # Adjusted weights for more natural movement
        self.weights = [0.25, 0.5, 0.25]  # More weight to PARTIAL state
        self._last_state = None
        self._state_duration = 0.0

    def _get_talk_state(self) -> Generator[TalkState, None, None]:
        """Generate a sequence of talk states for natural-looking speech."""
        while True:
            # Avoid repeating the same state too often
            available_states = [s for s in self.states if s != self._last_state]
            if not available_states:
                available_states = self.states
            
            # Adjust weights based on current state
            weights = self.weights.copy()
            if self._last_state:
                last_idx = self.states.index(self._last_state)
                weights[last_idx] *= 0.3  # Reduce chance of repeating state
            
            state = random.choices(available_states, weights=weights)[0]
            self._last_state = state
            yield state

    def _draw_talking_expression(self, expression: Expression, talk_state: TalkState) -> None:
        """Draw an expression with a specific talk state."""
        self.display.clear()
        self.display.draw_points(expression.points)
        
        if expression.talk_lines and talk_state in expression.talk_lines:
            self.display.draw_lines(expression.talk_lines[talk_state])
        elif expression.lines:
            self.display.draw_lines(expression.lines)

    def talk(
        self,
        expression_type: ExpressionType,
        duration: float = 2.0,
        words_per_minute: int = 150
    ) -> None:
        """Animate the robot face talking."""
        expression = self.expressions.get_expression(expression_type)
        if not expression.talk_lines:
            raise ValueError(f"Expression {expression_type.name} does not support talking")
        
        # Calculate timing
        states_per_second = (words_per_minute * 4) / 60  # Reduced from 5 to 4 for smoother animation
        min_state_duration = 0.1  # Minimum time per state
        state_duration = max(1.0 / states_per_second, min_state_duration)
        
        end_time = time.time() + duration
        talk_states = self._get_talk_state()
        last_draw_time = time.time()
        
        while time.time() < end_time:
            current_time = time.time()
            elapsed = current_time - last_draw_time
            
            # Only change state if enough time has passed
            if elapsed >= state_duration:
                self._draw_talking_expression(expression, next(talk_states))
                last_draw_time = current_time
                # Add a small random delay for more natural movement
                time.sleep(random.uniform(0.02, 0.05))
            else:
                # Small sleep to prevent CPU overuse
                time.sleep(0.01)

    def say_phrase(
        self,
        expression_type: ExpressionType,
        phrase: str,
        words_per_minute: int = 150
    ) -> None:
        """Say a specific phrase with appropriate timing."""
        word_count = len(phrase.split())
        # Add a small pause between words
        duration = (word_count * 65) / words_per_minute  # Increased from 60 to 65 to account for pauses
        
        print(f"Robot says: {phrase}")
        self.talk(expression_type, duration=duration, words_per_minute=words_per_minute) 