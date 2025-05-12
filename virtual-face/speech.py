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
        self.weights = [0.3, 0.4, 0.3]

    def _get_talk_state(self) -> Generator[TalkState, None, None]:
        """Generate a sequence of talk states for natural-looking speech."""
        while True:
            yield random.choices(self.states, weights=self.weights)[0]

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
        
        states_per_second = (words_per_minute * 5) / 60
        state_duration = 1.0 / states_per_second
        
        end_time = time.time() + duration
        talk_states = self._get_talk_state()
        
        while time.time() < end_time:
            self._draw_talking_expression(expression, next(talk_states))
            time.sleep(state_duration)

    def say_phrase(
        self,
        expression_type: ExpressionType,
        phrase: str,
        words_per_minute: int = 150
    ) -> None:
        """Say a specific phrase with appropriate timing."""
        word_count = len(phrase.split())
        duration = (word_count * 60) / words_per_minute
        
        print(f"Robot says: {phrase}")
        self.talk(expression_type, duration=duration, words_per_minute=words_per_minute) 