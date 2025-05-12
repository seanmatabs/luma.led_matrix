"""Shared types and enums for the robot face module."""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

class ExpressionType(Enum):
    """Enum for different types of facial expressions."""
    HAPPY = auto()
    SAD = auto()
    SURPRISED = auto()
    WINK = auto()
    NEUTRAL = auto()
    ANGRY = auto()
    SLEEPING = auto()

class TalkState(Enum):
    """Different states of mouth movement during speech."""
    OPEN = auto()
    CLOSED = auto()
    PARTIAL = auto()

@dataclass
class Expression:
    """Represents a facial expression with its drawing instructions."""
    name: str
    points: List[Tuple[int, int]]
    lines: List[Tuple[Tuple[int, int], Tuple[int, int]]] = None
    talk_lines: Dict[TalkState, List[Tuple[Tuple[int, int], Tuple[int, int]]]] = None
    duration: float = 1.0 