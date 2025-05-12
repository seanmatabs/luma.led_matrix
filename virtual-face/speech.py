from typing import Generator, Dict, List, Tuple
import time
import random

from .display import DisplayInterface
from .expressions import FacialExpressions
from .face_types import ExpressionType, TalkState, Expression

# Viseme mouth shapes for 8x8 matrix (3 rows: 5, 6, 7)
VISEME_MOUTHS: Dict[str, List[Tuple[Tuple[int, int], Tuple[int, int]]]] = {
    # Closed (M, B, P)
    "closed": [((2, 7), (5, 7)), ((2, 6), (5, 6))],
    # Wide (A, E, I)
    "wide": [((1, 7), (2, 6)), ((2, 6), (3, 5)), ((3, 5), (4, 5)), ((4, 5), (5, 6)), ((5, 6), (6, 7)), ((2, 7), (5, 7))],
    # Round (O, U, W)
    "round": [((3, 5), (4, 5)), ((3, 7), (4, 7)), ((3, 5), (3, 7)), ((4, 5), (4, 7)), ((2, 6), (5, 6))],
    # Teeth (F, V)
    "teeth": [((2, 6), (5, 6)), ((2, 7), (5, 7)), ((2, 5), (5, 5))],
    # Open (C, D, G, K, N, S, T, Y, Z, L, Q, X, H, J, R)
    "open": [((2, 5), (2, 7)), ((5, 5), (5, 7)), ((2, 7), (5, 7)), ((2, 5), (5, 5))],
    # Neutral (default)
    "neutral": [((2, 6), (5, 6))],
}

# Map letters to viseme keys
LETTER_TO_VISEME: Dict[str, str] = {
    **{k: "closed" for k in "MBPmbp"},
    **{k: "wide" for k in "AEIaei"},
    **{k: "round" for k in "OUWouw"},
    **{k: "teeth" for k in "FVfv"},
    **{k: "open" for k in "CDGKNSZLQXHJRTcdgknszlqxhjrt"},
}

class SpeechEngine:
    """Handles speech animation and timing."""
    def __init__(self, display: DisplayInterface, expressions: FacialExpressions) -> None:
        self.display = display
        self.expressions = expressions
        self.states = [TalkState.OPEN, TalkState.PARTIAL, TalkState.CLOSED]
        self.weights = [0.3, 0.4, 0.3]  # Back to original weights
        self._last_state = None
        self._state_duration = 0.0

    def _get_talk_state(self) -> Generator[TalkState, None, None]:
        """Generate a sequence of talk states for natural-looking speech."""
        while True:
            yield random.choices(self.states, weights=self.weights)[0]

    def _draw_viseme(self, expression: Expression, viseme: str) -> None:
        """Draw an expression with a specific viseme mouth shape."""
        self.display.clear()
        # Draw eyes from the current expression (use lines above y=5)
        eye_lines = [line for line in (expression.lines or []) if line[0][1] < 5 and line[1][1] < 5]
        mouth_lines = VISEME_MOUTHS.get(viseme, VISEME_MOUTHS["neutral"])
        self.display.draw_lines(eye_lines + mouth_lines)

    def talk(
        self,
        expression_type: ExpressionType,
        duration: float = 2.0,
        words_per_minute: int = 150
    ) -> None:
        """Animate the robot face talking using visemes."""
        expression = self.expressions.get_expression(expression_type)
        phrase = None  # No phrase, just animate random visemes
        self._talk_with_visemes(expression, duration, words_per_minute, phrase)

    def say_phrase(
        self,
        expression_type: ExpressionType,
        phrase: str,
        words_per_minute: int = 150
    ) -> None:
        """Say a specific phrase with appropriate timing using visemes."""
        expression = self.expressions.get_expression(expression_type)
        self._talk_with_visemes(expression, None, words_per_minute, phrase)

    def _talk_with_visemes(
        self,
        expression: Expression,
        duration: float,
        words_per_minute: int,
        phrase: str = None
    ) -> None:
        """Core viseme animation logic."""
        if phrase:
            # Parse phrase into viseme sequence
            viseme_seq = [LETTER_TO_VISEME.get(c, "neutral") for c in phrase if c.isalnum()]
            if not viseme_seq:
                viseme_seq = ["neutral"]
            # Calculate timing per viseme
            total_visemes = len(viseme_seq)
            total_time = (len(phrase.split()) * 60) / words_per_minute if words_per_minute else 2.0
            viseme_time = total_time / total_visemes
            for viseme in viseme_seq:
                self._draw_viseme(expression, viseme)
                time.sleep(viseme_time)
        else:
            # No phrase: animate random visemes for the given duration
            visemes = list(VISEME_MOUTHS.keys())
            end_time = time.time() + (duration if duration else 2.0)
            while time.time() < end_time:
                viseme = random.choice(visemes)
                self._draw_viseme(expression, viseme)
                time.sleep(0.15) 