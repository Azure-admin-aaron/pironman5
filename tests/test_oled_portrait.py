#!/usr/bin/env python3
"""
Unit tests for the OLED portrait mode module.

These tests verify the canvas size logic, rotation behavior, and drawing functions
for the OLEDPortraitRenderer class. They do not require actual OLED hardware.

Usage:
    python3 -m pytest tests/test_oled_portrait.py
    # or
    python3 tests/test_oled_portrait.py
"""

import sys
import os
import unittest

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pironman5.oled_portrait import (
    OLEDPortraitRenderer,
    is_portrait_mode,
    get_canvas_dimensions,
    rotate_image_for_display,
    LANDSCAPE_WIDTH,
    LANDSCAPE_HEIGHT,
    PORTRAIT_WIDTH,
    PORTRAIT_HEIGHT,
)


class TestCanvasDimensions(unittest.TestCase):
    """Tests for canvas dimension logic."""
    
    def test_landscape_dimensions_at_0_degrees(self):
        """Canvas should be 128x64 at 0° rotation."""
        renderer = OLEDPortraitRenderer(rotation=0)
        self.assertEqual(renderer.width, LANDSCAPE_WIDTH)
        self.assertEqual(renderer.height, LANDSCAPE_HEIGHT)
        self.assertEqual(renderer.get_canvas_size(), (128, 64))
    
    def test_landscape_dimensions_at_180_degrees(self):
        """Canvas should be 128x64 at 180° rotation."""
        renderer = OLEDPortraitRenderer(rotation=180)
        self.assertEqual(renderer.width, LANDSCAPE_WIDTH)
        self.assertEqual(renderer.height, LANDSCAPE_HEIGHT)
        self.assertEqual(renderer.get_canvas_size(), (128, 64))
    
    def test_portrait_dimensions_at_90_degrees(self):
        """Canvas should be 64x128 at 90° rotation."""
        renderer = OLEDPortraitRenderer(rotation=90)
        self.assertEqual(renderer.width, PORTRAIT_WIDTH)
        self.assertEqual(renderer.height, PORTRAIT_HEIGHT)
        self.assertEqual(renderer.get_canvas_size(), (64, 128))
    
    def test_portrait_dimensions_at_270_degrees(self):
        """Canvas should be 64x128 at 270° rotation."""
        renderer = OLEDPortraitRenderer(rotation=270)
        self.assertEqual(renderer.width, PORTRAIT_WIDTH)
        self.assertEqual(renderer.height, PORTRAIT_HEIGHT)
        self.assertEqual(renderer.get_canvas_size(), (64, 128))


class TestPortraitModeDetection(unittest.TestCase):
    """Tests for portrait mode detection."""
    
    def test_is_portrait_mode_0(self):
        """0° should not be portrait mode."""
        self.assertFalse(is_portrait_mode(0))
        renderer = OLEDPortraitRenderer(rotation=0)
        self.assertFalse(renderer.is_portrait)
    
    def test_is_portrait_mode_90(self):
        """90° should be portrait mode."""
        self.assertTrue(is_portrait_mode(90))
        renderer = OLEDPortraitRenderer(rotation=90)
        self.assertTrue(renderer.is_portrait)
    
    def test_is_portrait_mode_180(self):
        """180° should not be portrait mode."""
        self.assertFalse(is_portrait_mode(180))
        renderer = OLEDPortraitRenderer(rotation=180)
        self.assertFalse(renderer.is_portrait)
    
    def test_is_portrait_mode_270(self):
        """270° should be portrait mode."""
        self.assertTrue(is_portrait_mode(270))
        renderer = OLEDPortraitRenderer(rotation=270)
        self.assertTrue(renderer.is_portrait)


class TestRotationValidation(unittest.TestCase):
    """Tests for rotation value validation."""
    
    def test_valid_rotations(self):
        """Valid rotations should not raise errors."""
        for rotation in [0, 90, 180, 270]:
            renderer = OLEDPortraitRenderer(rotation=rotation)
            self.assertEqual(renderer.rotation, rotation)
    
    def test_invalid_rotation_45(self):
        """45° should raise ValueError."""
        with self.assertRaises(ValueError):
            OLEDPortraitRenderer(rotation=45)
    
    def test_invalid_rotation_negative(self):
        """-90° should raise ValueError."""
        with self.assertRaises(ValueError):
            OLEDPortraitRenderer(rotation=-90)
    
    def test_invalid_rotation_360(self):
        """360° should raise ValueError."""
        with self.assertRaises(ValueError):
            OLEDPortraitRenderer(rotation=360)
    
    def test_invalid_rotation_135(self):
        """135° should raise ValueError."""
        with self.assertRaises(ValueError):
            OLEDPortraitRenderer(rotation=135)


class TestSetRotation(unittest.TestCase):
    """Tests for changing rotation after initialization."""
    
    def test_change_from_landscape_to_portrait(self):
        """Changing from 0° to 90° should update canvas dimensions."""
        renderer = OLEDPortraitRenderer(rotation=0)
        self.assertEqual(renderer.get_canvas_size(), (128, 64))
        
        renderer.set_rotation(90)
        self.assertEqual(renderer.get_canvas_size(), (64, 128))
        self.assertTrue(renderer.is_portrait)
    
    def test_change_from_portrait_to_landscape(self):
        """Changing from 90° to 180° should update canvas dimensions."""
        renderer = OLEDPortraitRenderer(rotation=90)
        self.assertEqual(renderer.get_canvas_size(), (64, 128))
        
        renderer.set_rotation(180)
        self.assertEqual(renderer.get_canvas_size(), (128, 64))
        self.assertFalse(renderer.is_portrait)
    
    def test_change_within_landscape(self):
        """Changing from 0° to 180° should keep canvas dimensions."""
        renderer = OLEDPortraitRenderer(rotation=0)
        renderer.set_rotation(180)
        self.assertEqual(renderer.get_canvas_size(), (128, 64))
        self.assertFalse(renderer.is_portrait)
    
    def test_change_within_portrait(self):
        """Changing from 90° to 270° should keep canvas dimensions."""
        renderer = OLEDPortraitRenderer(rotation=90)
        renderer.set_rotation(270)
        self.assertEqual(renderer.get_canvas_size(), (64, 128))
        self.assertTrue(renderer.is_portrait)
    
    def test_set_rotation_invalid_value(self):
        """Setting invalid rotation should raise ValueError."""
        renderer = OLEDPortraitRenderer(rotation=0)
        with self.assertRaises(ValueError):
            renderer.set_rotation(45)


class TestCenterCoordinates(unittest.TestCase):
    """Tests for center coordinate calculations."""
    
    def test_landscape_center(self):
        """Landscape mode should have center at (64, 32)."""
        renderer = OLEDPortraitRenderer(rotation=0)
        self.assertEqual(renderer.get_center_x(), 64)
        self.assertEqual(renderer.get_center_y(), 32)
    
    def test_portrait_center(self):
        """Portrait mode should have center at (32, 64)."""
        renderer = OLEDPortraitRenderer(rotation=90)
        self.assertEqual(renderer.get_center_x(), 32)
        self.assertEqual(renderer.get_center_y(), 64)


class TestGetCanvasDimensionsFunction(unittest.TestCase):
    """Tests for the get_canvas_dimensions utility function."""
    
    def test_dimensions_0(self):
        """0° should return landscape dimensions."""
        self.assertEqual(get_canvas_dimensions(0), (128, 64))
    
    def test_dimensions_90(self):
        """90° should return portrait dimensions."""
        self.assertEqual(get_canvas_dimensions(90), (64, 128))
    
    def test_dimensions_180(self):
        """180° should return landscape dimensions."""
        self.assertEqual(get_canvas_dimensions(180), (128, 64))
    
    def test_dimensions_270(self):
        """270° should return portrait dimensions."""
        self.assertEqual(get_canvas_dimensions(270), (64, 128))
    
    def test_invalid_rotation(self):
        """Invalid rotation should raise ValueError."""
        with self.assertRaises(ValueError):
            get_canvas_dimensions(45)


class TestImageRotation(unittest.TestCase):
    """Tests for image rotation functionality."""
    
    def test_rotated_image_size_landscape(self):
        """Rotated image at 0° should maintain 128x64 size."""
        renderer = OLEDPortraitRenderer(rotation=0)
        rotated = renderer.get_rotated_image()
        self.assertEqual(rotated.size, (128, 64))
    
    def test_rotated_image_size_landscape_180(self):
        """Rotated image at 180° should maintain 128x64 size."""
        renderer = OLEDPortraitRenderer(rotation=180)
        rotated = renderer.get_rotated_image()
        self.assertEqual(rotated.size, (128, 64))
    
    def test_rotated_image_size_portrait_90(self):
        """Rotated image at 90° should be 128x64 after rotation."""
        renderer = OLEDPortraitRenderer(rotation=90)
        # Canvas is 64x128, after rotation becomes 128x64 for display
        rotated = renderer.get_rotated_image()
        self.assertEqual(rotated.size, (128, 64))
    
    def test_rotated_image_size_portrait_270(self):
        """Rotated image at 270° should be 128x64 after rotation."""
        renderer = OLEDPortraitRenderer(rotation=270)
        # Canvas is 64x128, after rotation becomes 128x64 for display
        rotated = renderer.get_rotated_image()
        self.assertEqual(rotated.size, (128, 64))


class TestRotateImageForDisplayFunction(unittest.TestCase):
    """Tests for the rotate_image_for_display utility function."""
    
    def test_rotate_0_degrees(self):
        """Image should not change at 0° rotation."""
        from PIL import Image
        img = Image.new('1', (128, 64), 0)
        rotated = rotate_image_for_display(img, 0)
        self.assertEqual(rotated.size, (128, 64))
    
    def test_rotate_180_degrees(self):
        """Image should maintain size at 180° rotation."""
        from PIL import Image
        img = Image.new('1', (128, 64), 0)
        rotated = rotate_image_for_display(img, 180)
        self.assertEqual(rotated.size, (128, 64))
    
    def test_rotate_90_degrees(self):
        """Portrait canvas should become landscape after 90° rotation."""
        from PIL import Image
        img = Image.new('1', (64, 128), 0)  # Portrait canvas
        rotated = rotate_image_for_display(img, 90)
        self.assertEqual(rotated.size, (128, 64))
    
    def test_rotate_270_degrees(self):
        """Portrait canvas should become landscape after 270° rotation."""
        from PIL import Image
        img = Image.new('1', (64, 128), 0)  # Portrait canvas
        rotated = rotate_image_for_display(img, 270)
        self.assertEqual(rotated.size, (128, 64))
    
    def test_rotate_invalid(self):
        """Invalid rotation should raise ValueError."""
        from PIL import Image
        img = Image.new('1', (128, 64), 0)
        with self.assertRaises(ValueError):
            rotate_image_for_display(img, 45)


class TestDrawingFunctions(unittest.TestCase):
    """Tests for drawing functions."""
    
    def test_clear_canvas(self):
        """Clear should reset the canvas."""
        renderer = OLEDPortraitRenderer(rotation=0)
        renderer.draw_rectangle(0, 0, 10, 10, fill=1)
        renderer.clear()
        # After clear, the image should be all black (0)
        img = renderer.get_image()
        # Check that it's a valid image
        self.assertEqual(img.size, (128, 64))
    
    def test_draw_text(self):
        """Text drawing should not raise errors."""
        renderer = OLEDPortraitRenderer(rotation=0)
        renderer.draw_text("Test", 10, 10)
        # Should complete without error
        img = renderer.get_image()
        self.assertIsNotNone(img)
    
    def test_draw_rectangle(self):
        """Rectangle drawing should not raise errors."""
        renderer = OLEDPortraitRenderer(rotation=0)
        renderer.draw_rectangle(10, 10, 50, 30, outline=1)
        img = renderer.get_image()
        self.assertIsNotNone(img)
    
    def test_draw_line(self):
        """Line drawing should not raise errors."""
        renderer = OLEDPortraitRenderer(rotation=0)
        renderer.draw_line(0, 0, 127, 63, fill=1)
        img = renderer.get_image()
        self.assertIsNotNone(img)
    
    def test_draw_bar_graph_horizontal(self):
        """Horizontal bar graph should not raise errors."""
        renderer = OLEDPortraitRenderer(rotation=0)
        renderer.draw_bar_graph_horizontal(50, 20, 100)
        img = renderer.get_image()
        self.assertIsNotNone(img)
    
    def test_draw_bar_graph_vertical(self):
        """Vertical bar graph should not raise errors."""
        renderer = OLEDPortraitRenderer(rotation=90)
        renderer.draw_bar_graph_vertical(75, 20, 80)
        img = renderer.get_image()
        self.assertIsNotNone(img)
    
    def test_bar_graph_clamp_percent(self):
        """Bar graph should clamp percent values to 0-100."""
        renderer = OLEDPortraitRenderer(rotation=0)
        # These should not raise errors
        renderer.draw_bar_graph_horizontal(150, 20, 100)  # Over 100
        renderer.draw_bar_graph_horizontal(-50, 30, 100)  # Negative
        img = renderer.get_image()
        self.assertIsNotNone(img)


class TestPortraitModeLayout(unittest.TestCase):
    """Tests for portrait mode specific layout concerns."""
    
    def test_portrait_has_more_vertical_space(self):
        """Portrait mode should have more vertical than horizontal space."""
        renderer = OLEDPortraitRenderer(rotation=90)
        self.assertGreater(renderer.height, renderer.width)
    
    def test_landscape_has_more_horizontal_space(self):
        """Landscape mode should have more horizontal than vertical space."""
        renderer = OLEDPortraitRenderer(rotation=0)
        self.assertGreater(renderer.width, renderer.height)
    
    def test_portrait_center_x_is_half_of_landscape_center_x(self):
        """Portrait center X should be half of landscape center X."""
        landscape = OLEDPortraitRenderer(rotation=0)
        portrait = OLEDPortraitRenderer(rotation=90)
        self.assertEqual(portrait.get_center_x(), landscape.get_center_x() // 2)
    
    def test_portrait_center_y_is_double_landscape_center_y(self):
        """Portrait center Y should be double landscape center Y."""
        landscape = OLEDPortraitRenderer(rotation=0)
        portrait = OLEDPortraitRenderer(rotation=90)
        self.assertEqual(portrait.get_center_y(), landscape.get_center_y() * 2)


def run_tests():
    """Run all unit tests."""
    # Use unittest's test runner
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
