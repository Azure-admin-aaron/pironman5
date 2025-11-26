"""
OLED Portrait Mode Support Module

This module provides portrait mode rendering support for SSD1306 OLED displays
when used with 90° or 270° rotations. It creates a 64x128 canvas for portrait
mode and handles proper image rotation before sending to the display.

For 0° and 180° rotations, the standard landscape mode (128x64) is used.

Usage:
    from pironman5.oled_portrait import OLEDPortraitRenderer
    
    renderer = OLEDPortraitRenderer(rotation=90)
    renderer.draw_text("Hello", x, y)
    renderer.display()

Requirements:
    - PIL/Pillow for image manipulation
    - pm_auto library for underlying SSD1306 hardware communication
"""

from PIL import Image, ImageDraw, ImageFont
import io


# Standard OLED display dimensions
LANDSCAPE_WIDTH = 128
LANDSCAPE_HEIGHT = 64
PORTRAIT_WIDTH = 64
PORTRAIT_HEIGHT = 128


class OLEDPortraitRenderer:
    """
    A wrapper class that handles portrait mode rendering for SSD1306 OLED displays.
    
    This class creates the appropriate canvas size based on rotation:
    - 0° and 180°: Uses standard 128x64 landscape canvas
    - 90° and 270°: Uses 64x128 portrait canvas, rotates before display
    
    Attributes:
        rotation (int): Display rotation in degrees (0, 90, 180, 270)
        width (int): Canvas width (128 for landscape, 64 for portrait)
        height (int): Canvas height (64 for landscape, 128 for portrait)
        is_portrait (bool): True if using portrait mode (90° or 270°)
    """
    
    VALID_ROTATIONS = [0, 90, 180, 270]
    
    def __init__(self, rotation=0):
        """
        Initialize the OLED portrait renderer.
        
        Args:
            rotation (int): Display rotation in degrees. Must be 0, 90, 180, or 270.
            
        Raises:
            ValueError: If rotation is not a valid value (0, 90, 180, 270).
        """
        if rotation not in self.VALID_ROTATIONS:
            raise ValueError(
                f"Invalid rotation value: {rotation}. "
                f"Must be one of {self.VALID_ROTATIONS}"
            )
        
        self.rotation = rotation
        self.is_portrait = rotation in [90, 270]
        
        # Set canvas dimensions based on mode
        if self.is_portrait:
            self.width = PORTRAIT_WIDTH
            self.height = PORTRAIT_HEIGHT
        else:
            self.width = LANDSCAPE_WIDTH
            self.height = LANDSCAPE_HEIGHT
        
        # Create the drawing canvas
        self._image = Image.new('1', (self.width, self.height), 0)
        self._draw = ImageDraw.Draw(self._image)
        
        # Default font (can be overridden)
        self._font = None
        
    def set_rotation(self, rotation):
        """
        Update the rotation setting.
        
        Args:
            rotation (int): New rotation value (0, 90, 180, 270).
            
        Raises:
            ValueError: If rotation is not a valid value.
        """
        if rotation not in self.VALID_ROTATIONS:
            raise ValueError(
                f"Invalid rotation value: {rotation}. "
                f"Must be one of {self.VALID_ROTATIONS}"
            )
        
        old_is_portrait = self.is_portrait
        self.rotation = rotation
        self.is_portrait = rotation in [90, 270]
        
        # Recreate canvas if mode changed
        if old_is_portrait != self.is_portrait:
            if self.is_portrait:
                self.width = PORTRAIT_WIDTH
                self.height = PORTRAIT_HEIGHT
            else:
                self.width = LANDSCAPE_WIDTH
                self.height = LANDSCAPE_HEIGHT
            
            self._image = Image.new('1', (self.width, self.height), 0)
            self._draw = ImageDraw.Draw(self._image)
    
    def clear(self):
        """Clear the canvas (fill with black)."""
        self._draw.rectangle((0, 0, self.width, self.height), fill=0)
    
    def get_canvas_size(self):
        """
        Get the current canvas dimensions.
        
        Returns:
            tuple: (width, height) of the canvas
        """
        return (self.width, self.height)
    
    def get_center_x(self):
        """
        Get the horizontal center coordinate of the canvas.
        
        Returns:
            int: Center x coordinate (64 for landscape, 32 for portrait)
        """
        return self.width // 2
    
    def get_center_y(self):
        """
        Get the vertical center coordinate of the canvas.
        
        Returns:
            int: Center y coordinate (32 for landscape, 64 for portrait)
        """
        return self.height // 2
    
    def draw_text(self, text, x, y, fill=1, font=None, align='left'):
        """
        Draw text on the canvas.
        
        Args:
            text (str): Text to draw
            x (int): X coordinate
            y (int): Y coordinate
            fill (int): Fill color (1 for white, 0 for black)
            font: PIL ImageFont object (optional)
            align (str): Text alignment ('left', 'center', 'right')
        """
        use_font = font or self._font
        
        if align != 'left' and use_font:
            # Get text width for alignment
            bbox = self._draw.textbbox((0, 0), text, font=use_font)
            text_width = bbox[2] - bbox[0]
            
            if align == 'center':
                x = x - text_width // 2
            elif align == 'right':
                x = x - text_width
        
        if use_font:
            self._draw.text((x, y), text, fill=fill, font=use_font)
        else:
            self._draw.text((x, y), text, fill=fill)
    
    def draw_rectangle(self, x1, y1, x2, y2, fill=None, outline=1, width=1):
        """
        Draw a rectangle on the canvas.
        
        Args:
            x1, y1: Top-left corner coordinates
            x2, y2: Bottom-right corner coordinates
            fill: Fill color (None for no fill, 1 for white, 0 for black)
            outline: Outline color (1 for white, 0 for black)
            width: Outline width
        """
        self._draw.rectangle((x1, y1, x2, y2), fill=fill, outline=outline, width=width)
    
    def draw_line(self, x1, y1, x2, y2, fill=1, width=1):
        """
        Draw a line on the canvas.
        
        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates
            fill: Line color (1 for white, 0 for black)
            width: Line width
        """
        self._draw.line((x1, y1, x2, y2), fill=fill, width=width)
    
    def draw_bar_graph_horizontal(self, percent, y, width, x=None, height=8):
        """
        Draw a horizontal bar graph.
        
        Args:
            percent (float): Fill percentage (0-100)
            y (int): Y coordinate
            width (int): Total width of the bar
            x (int): X coordinate (default: centered)
            height (int): Height of the bar
        """
        if x is None:
            x = (self.width - width) // 2
        
        # Clamp percent to 0-100
        percent = max(0, min(100, percent))
        
        # Draw outline
        self._draw.rectangle((x, y, x + width, y + height), outline=1)
        
        # Draw fill
        fill_width = int((width - 2) * percent / 100)
        if fill_width > 0:
            self._draw.rectangle((x + 1, y + 1, x + 1 + fill_width, y + height - 1), fill=1)
    
    def draw_bar_graph_vertical(self, percent, x, height, y=None, width=8):
        """
        Draw a vertical bar graph (useful for portrait mode).
        
        Args:
            percent (float): Fill percentage (0-100)
            x (int): X coordinate
            height (int): Total height of the bar
            y (int): Y coordinate (default: centered)
            width (int): Width of the bar
        """
        if y is None:
            y = (self.height - height) // 2
        
        # Clamp percent to 0-100
        percent = max(0, min(100, percent))
        
        # Draw outline
        self._draw.rectangle((x, y, x + width, y + height), outline=1)
        
        # Draw fill (from bottom up)
        fill_height = int((height - 2) * percent / 100)
        if fill_height > 0:
            self._draw.rectangle(
                (x + 1, y + height - 1 - fill_height, x + width - 1, y + height - 1),
                fill=1
            )
    
    def get_rotated_image(self):
        """
        Get the image rotated for display.
        
        For portrait mode (90° or 270°), the image is rotated using
        image.rotate(angle, expand=True) to produce the correct output
        for the physical display orientation.
        
        For 0° rotation, returns the image as-is.
        For 180° rotation, rotates the image 180 degrees.
        
        Returns:
            PIL.Image: The rotated image ready for display
        """
        if self.rotation == 0:
            return self._image.copy()
        elif self.rotation == 180:
            return self._image.rotate(180)
        elif self.rotation == 90:
            # Portrait mode: rotate 90° clockwise
            # Note: PIL rotate is counter-clockwise, so we use -90 or 270
            return self._image.rotate(-90, expand=True)
        elif self.rotation == 270:
            # Portrait mode: rotate 270° clockwise (or 90° counter-clockwise)
            return self._image.rotate(-270, expand=True)
        else:
            return self._image.copy()
    
    def get_image(self):
        """
        Get the raw canvas image (without rotation applied).
        
        Returns:
            PIL.Image: The canvas image
        """
        return self._image.copy()
    
    def get_draw(self):
        """
        Get the ImageDraw object for direct drawing operations.
        
        Returns:
            PIL.ImageDraw: The draw object
        """
        return self._draw
    
    def set_font(self, font):
        """
        Set the default font for text drawing.
        
        Args:
            font: PIL ImageFont object
        """
        self._font = font
    
    def paste_image(self, image, position=(0, 0)):
        """
        Paste an image onto the canvas.
        
        Args:
            image: PIL Image to paste
            position: (x, y) position tuple
        """
        self._image.paste(image, position)


def is_portrait_mode(rotation):
    """
    Check if the given rotation value corresponds to portrait mode.
    
    Args:
        rotation (int): Rotation angle in degrees
        
    Returns:
        bool: True if rotation is 90° or 270° (portrait mode)
    """
    return rotation in [90, 270]


def get_canvas_dimensions(rotation):
    """
    Get the appropriate canvas dimensions for a given rotation.
    
    Args:
        rotation (int): Rotation angle in degrees (0, 90, 180, 270)
        
    Returns:
        tuple: (width, height) - (128, 64) for landscape, (64, 128) for portrait
        
    Raises:
        ValueError: If rotation is not a valid value
    """
    if rotation not in [0, 90, 180, 270]:
        raise ValueError(
            f"Invalid rotation value: {rotation}. "
            f"Must be one of [0, 90, 180, 270]"
        )
    
    if is_portrait_mode(rotation):
        return (PORTRAIT_WIDTH, PORTRAIT_HEIGHT)
    else:
        return (LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT)


def rotate_image_for_display(image, rotation):
    """
    Rotate an image for display at the specified rotation.
    
    This function handles the rotation transformation needed to display
    content correctly at each supported rotation angle:
    - 0°: No rotation
    - 90°: Rotate 90° clockwise (content drawn on 64x128 canvas)
    - 180°: Rotate 180°
    - 270°: Rotate 270° clockwise (content drawn on 64x128 canvas)
    
    Args:
        image: PIL Image object
        rotation (int): Target rotation angle in degrees
        
    Returns:
        PIL.Image: Rotated image ready for display
        
    Raises:
        ValueError: If rotation is not a valid value
    """
    if rotation not in [0, 90, 180, 270]:
        raise ValueError(
            f"Invalid rotation value: {rotation}. "
            f"Must be one of [0, 90, 180, 270]"
        )
    
    if rotation == 0:
        return image.copy()
    elif rotation == 180:
        return image.rotate(180)
    elif rotation == 90:
        # For 90° display rotation, rotate canvas content
        return image.rotate(-90, expand=True)
    elif rotation == 270:
        return image.rotate(-270, expand=True)
    
    return image.copy()
