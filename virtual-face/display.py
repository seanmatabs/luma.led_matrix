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
        self.virtual = None

    def draw_points(self, points: List[Tuple[int, int]], fill: str = "white") -> None:
        with canvas(self.device) as draw:
            for point in points:
                draw.point(point, fill=fill)

    def draw_lines(self, lines: List[Tuple[Tuple[int, int], Tuple[int, int]]], fill: str = "white") -> None:
        """Draw lines or rectangles. For rectangles, provide diagonal corners."""
        with canvas(self.device) as draw:
            for start, end in lines:
                # Check if this is a rectangle (diagonal corners)
                is_rectangle = (
                    abs(start[0] - end[0]) > 0 and 
                    abs(start[1] - end[1]) > 0 and
                    # Only draw as rectangle if it's a proper rectangle (not diagonal)
                    (start[0] == end[0] or start[1] == end[1] or
                     abs(start[0] - end[0]) == abs(start[1] - end[1]))
                )
                
                if is_rectangle:
                    # Ensure coordinates are in correct order for rectangle
                    x0 = min(start[0], end[0])
                    y0 = min(start[1], end[1])
                    x1 = max(start[0], end[0])
                    y1 = max(start[1], end[1])
                    draw.rectangle([(x0, y0), (x1, y1)], outline=fill, fill=fill)
                else:
                    # Draw as a line
                    draw.line([start, end], fill=fill)

    def draw_rectangle(self, top_left: Tuple[int, int], bottom_right: Tuple[int, int], fill: str = "white") -> None:
        """Draw a filled rectangle efficiently."""
        with canvas(self.device) as draw:
            # Ensure coordinates are in correct order
            x0 = min(top_left[0], bottom_right[0])
            y0 = min(top_left[1], bottom_right[1])
            x1 = max(top_left[0], bottom_right[0])
            y1 = max(top_left[1], bottom_right[1])
            draw.rectangle([(x0, y0), (x1, y1)], outline=fill, fill=fill)

    def clear(self) -> None:
        """Clear the display."""
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="black", fill="black")

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