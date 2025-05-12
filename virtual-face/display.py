"""Display interface and implementation for the robot face."""

from typing import List, Tuple, Protocol, Optional
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219

class DisplayInterface(Protocol):
    """Protocol defining the interface for display operations."""
    def draw_points(self, points: List[Tuple[int, int]], fill: str = "white") -> None: ...
    def draw_lines(self, lines: List[Tuple[Tuple[int, int], Tuple[int, int]]], fill: str = "white") -> None: ...
    def draw_rectangle(self, top_left: Tuple[int, int], bottom_right: Tuple[int, int], fill: str = "white") -> None: ...
    def clear(self) -> None: ...
    def set_brightness(self, intensity: int) -> None: ...

class MatrixDisplay(DisplayInterface):
    """Handles the actual display operations on the LED matrix."""
    def __init__(
        self,
        cascaded: int = 1,
        block_orientation: int = 0,
        rotate: int = 0,
        blocks_arranged_in_reverse_order: bool = False,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> None:
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
        # Only create virtual viewport if needed for scrolling
        self.virtual = None
        self._needs_clear = True

    def draw_points(self, points: List[Tuple[int, int]], fill: str = "white") -> None:
        with canvas(self.device) as draw:
            if self._needs_clear:
                draw.rectangle(self.device.bounding_box, outline="black", fill="black")
                self._needs_clear = False
            for point in points:
                draw.point(point, fill=fill)

    def draw_lines(self, lines: List[Tuple[Tuple[int, int], Tuple[int, int]]], fill: str = "white") -> None:
        with canvas(self.device) as draw:
            if self._needs_clear:
                draw.rectangle(self.device.bounding_box, outline="black", fill="black")
                self._needs_clear = False
            for start, end in lines:
                # If the line forms a rectangle (start and end are diagonal corners)
                if abs(start[0] - end[0]) > 0 and abs(start[1] - end[1]) > 0:
                    self.draw_rectangle(start, end, fill)
                else:
                    draw.line([start, end], fill=fill)

    def draw_rectangle(self, top_left: Tuple[int, int], bottom_right: Tuple[int, int], fill: str = "white") -> None:
        """Draw a filled rectangle efficiently."""
        with canvas(self.device) as draw:
            if self._needs_clear:
                draw.rectangle(self.device.bounding_box, outline="black", fill="black")
                self._needs_clear = False
            draw.rectangle([top_left, bottom_right], outline=fill, fill=fill)

    def clear(self) -> None:
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="black", fill="black")
        self._needs_clear = True

    def set_brightness(self, intensity: int) -> None:
        if not 0 <= intensity <= 15:
            raise ValueError("Intensity must be between 0 and 15")
        self.device.contrast(intensity * 16)

    def set_scroll_mode(self, enable: bool) -> None:
        """Enable or disable scroll mode by creating/destroying virtual viewport."""
        if enable and self.virtual is None:
            self.virtual = viewport(self.device, width=self.device.width, height=self.device.height)
        elif not enable and self.virtual is not None:
            self.virtual = None 