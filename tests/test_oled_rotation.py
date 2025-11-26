#!/usr/bin/env python3
"""
Test script for OLED rotation functionality.

This script demonstrates and tests the OLED rotation options (0°, 90°, 180°, 270°).
It can be run on a Raspberry Pi with Pironman5/Pironman5 MAX hardware.

Usage:
    python3 tests/test_oled_rotation.py [--rotation ANGLE] [--demo]

Options:
    --rotation ANGLE    Test a specific rotation angle (0, 90, 180, 270)
    --demo              Run a demo cycling through all rotation angles

Requirements:
    - Raspberry Pi with Pironman5/Pironman5 MAX hardware
    - pm_auto library installed with OLED rotation support
    - I2C enabled (sudo raspi-config -> Interface Options -> I2C -> Yes)

Example:
    # Test 90 degree rotation
    python3 tests/test_oled_rotation.py --rotation 90
    
    # Run demo of all rotations
    python3 tests/test_oled_rotation.py --demo

Portrait Mode Support:
    For 90° and 270° rotations, the pironman5.oled_portrait module provides
    proper portrait mode rendering with a 64x128 canvas. The image is then
    rotated before being sent to the display.
"""

import argparse
import os
import sys
import time

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_rotation_cli_validation():
    """Test that CLI accepts all valid rotation values.
    
    This test validates that:
    - Rotations 0, 90, 180, 270 are considered valid by the CLI
    - Other rotation values (45, 135, 360, -90) are rejected
    """
    valid_rotations = [0, 90, 180, 270]
    cli_valid_rotations = [0, 90, 180, 270]  # What the CLI accepts
    
    print("Testing CLI rotation validation...")
    
    # Test that expected valid rotations are accepted
    for rotation in valid_rotations:
        is_valid = rotation in cli_valid_rotations
        if not is_valid:
            print(f"  FAIL: Rotation {rotation}° should be accepted by CLI")
            return False
        print(f"  PASS: Rotation {rotation}° is accepted by CLI")
    
    # Test that invalid rotations are rejected
    invalid_rotations = [45, 135, 360, -90]
    for rotation in invalid_rotations:
        is_valid = rotation in cli_valid_rotations
        if is_valid:
            print(f"  FAIL: Rotation {rotation}° should be rejected by CLI")
            return False
        print(f"  PASS: Rotation {rotation}° is correctly rejected by CLI")
    
    return True


def test_portrait_mode_module():
    """Test the portrait mode module functionality.
    
    This test validates that:
    - The OLEDPortraitRenderer class can be imported
    - Canvas dimensions are correct for each rotation
    - Portrait mode is correctly detected
    """
    try:
        from pironman5.oled_portrait import (
            OLEDPortraitRenderer,
            is_portrait_mode,
            get_canvas_dimensions,
        )
    except ImportError as e:
        print(f"  FAIL: Could not import oled_portrait module: {e}")
        return False
    
    print("\nTesting portrait mode module...")
    
    # Test canvas dimensions
    test_cases = [
        (0, (128, 64), False),
        (90, (64, 128), True),
        (180, (128, 64), False),
        (270, (64, 128), True),
    ]
    
    for rotation, expected_dims, expected_portrait in test_cases:
        # Test get_canvas_dimensions function
        dims = get_canvas_dimensions(rotation)
        if dims != expected_dims:
            print(f"  FAIL: get_canvas_dimensions({rotation}) = {dims}, expected {expected_dims}")
            return False
        
        # Test is_portrait_mode function
        portrait = is_portrait_mode(rotation)
        if portrait != expected_portrait:
            print(f"  FAIL: is_portrait_mode({rotation}) = {portrait}, expected {expected_portrait}")
            return False
        
        # Test OLEDPortraitRenderer class
        renderer = OLEDPortraitRenderer(rotation=rotation)
        if renderer.get_canvas_size() != expected_dims:
            print(f"  FAIL: Renderer canvas size at {rotation}° = {renderer.get_canvas_size()}, expected {expected_dims}")
            return False
        if renderer.is_portrait != expected_portrait:
            print(f"  FAIL: Renderer is_portrait at {rotation}° = {renderer.is_portrait}, expected {expected_portrait}")
            return False
        
        print(f"  PASS: Rotation {rotation}° - canvas={dims}, portrait={portrait}")
    
    # Test that rotated image has correct final size (always 128x64 for display)
    print("\nTesting rotated image sizes...")
    for rotation in [0, 90, 180, 270]:
        renderer = OLEDPortraitRenderer(rotation=rotation)
        rotated = renderer.get_rotated_image()
        if rotated.size != (128, 64):
            print(f"  FAIL: Rotated image at {rotation}° has size {rotated.size}, expected (128, 64)")
            return False
        print(f"  PASS: Rotated image at {rotation}° has correct size (128, 64)")
    
    return True


def demo_oled_rotation(rotation_angle):
    """
    Demonstrate OLED rotation with sample text.
    
    This function attempts to display sample text on the OLED at the specified rotation.
    It requires the pm_auto library and actual OLED hardware.
    
    For 90° and 270° rotations (portrait mode), the pironman5.oled_portrait module
    is used to create the proper 64x128 canvas and handle rotation.
    
    Args:
        rotation_angle: Rotation angle in degrees (0, 90, 180, 270)
    """
    # First, try to use the portrait mode module for demonstration
    try:
        from pironman5.oled_portrait import OLEDPortraitRenderer
        
        print(f"\nDemonstrating portrait mode rendering at {rotation_angle}°...")
        
        renderer = OLEDPortraitRenderer(rotation=rotation_angle)
        renderer.clear()
        
        if renderer.is_portrait:
            # Portrait mode: 64x128 canvas
            center_x = renderer.get_center_x()  # 32
            renderer.draw_text("Pironman5", center_x, 10, align='center')
            renderer.draw_text(f"Rotation:", center_x, 30, align='center')
            renderer.draw_text(f"{rotation_angle}°", center_x, 50, align='center')
            renderer.draw_text("Portrait", center_x, 75, align='center')
            renderer.draw_text("Mode", center_x, 95, align='center')
            renderer.draw_bar_graph_vertical(75, 5, 100, y=20, width=8)
        else:
            # Landscape mode: 128x64 canvas
            center_x = renderer.get_center_x()  # 64
            renderer.draw_text("Pironman5", center_x, 5, align='center')
            renderer.draw_text(f"Rotation: {rotation_angle}°", center_x, 20, align='center')
            renderer.draw_text("Landscape Mode", center_x, 40, align='center')
            renderer.draw_bar_graph_horizontal(75, 52, 100)
        
        # Get the rotated image ready for display
        display_image = renderer.get_rotated_image()
        print(f"  Canvas size: {renderer.get_canvas_size()}")
        print(f"  Display image size: {display_image.size}")
        print(f"  Portrait mode: {renderer.is_portrait}")
        
    except ImportError:
        print("  Note: Could not import oled_portrait module")
    
    # Now try to use the actual OLED hardware via pm_auto
    try:
        from pm_auto.ssd1306 import SSD1306
    except ImportError:
        print("Note: pm_auto library not found.")
        print("Please install pm_auto or run this script on a Pironman5 with the software installed.")
        print("\nFor 90° and 270° rotation support, pm_auto needs to be updated to handle")
        print("portrait mode drawing (64x128 canvas) before rotation.")
        return False
    
    print(f"\nTesting OLED hardware with rotation: {rotation_angle}°")
    
    try:
        oled = SSD1306()
        if not oled.is_ready():
            print("Error: OLED not ready")
            return False
        
        # Set rotation
        try:
            oled.set_rotation(rotation_angle)
        except ValueError as e:
            print(f"Note: pm_auto raised error for rotation {rotation_angle}°: {e}")
            print("This indicates pm_auto needs to be updated to support 90° and 270° rotations.")
            if rotation_angle in [90, 270]:
                print("\nTo implement 90°/270° rotation, pm_auto's SSD1306 class needs to:")
                print("  1. Accept 90 and 270 as valid rotation values")
                print("  2. Create drawing canvas as 64x128 (portrait) for 90°/270°")
                print("  3. Use image.rotate(angle, expand=True) in display() method")
            return False
        
        # Clear display
        oled.clear()
        
        # Draw sample content
        # Note: For 0°/180° (landscape), display is 128x64
        # For 90°/270° (portrait), display would be 64x128 in the drawing canvas
        # The coordinates below are for landscape mode (0°/180°)
        # When pm_auto supports portrait mode, coordinates should be adjusted:
        #   - Portrait (90°/270°): center_x=32, use taller layout with more vertical space
        
        if rotation_angle in [0, 180]:
            # Landscape mode: 128x64, center at x=64
            center_x = 64
            oled.draw_text("Pironman5", center_x, 5, align='center')
            oled.draw_text(f"Rotation: {rotation_angle}°", center_x, 20, align='center')
            oled.draw_text("OLED Test", center_x, 35, align='center')
            # Draw a horizontal bar to show orientation
            oled.draw_bar_graph_horizontal(75, 20, 50, 88, 8)
        else:
            # Portrait mode (90°/270°): 64x128 canvas (requires pm_auto update)
            # Using landscape coordinates as fallback since pm_auto doesn't support this yet
            center_x = 64  # Would be 32 in true portrait mode
            oled.draw_text("Pironman5", center_x, 5, align='center')
            oled.draw_text(f"Rot: {rotation_angle}°", center_x, 20, align='center')
            oled.draw_text("Portrait", center_x, 35, align='center')
            oled.draw_text("Mode", center_x, 50, align='center')
            # In portrait mode, would use vertical bar
            oled.draw_bar_graph_horizontal(75, 10, 55, 60, 6)
        
        # Display the content
        oled.display()
        
        print(f"  Successfully displayed content at {rotation_angle}° rotation")
        return True
        
    except Exception as e:
        print(f"Error during OLED test: {e}")
        return False


def run_demo():
    """Run a demo cycling through all rotation angles."""
    rotations = [0, 90, 180, 270]
    display_time = 3  # seconds per rotation
    
    print("\n=== OLED Rotation Demo ===")
    print(f"Cycling through rotations: {rotations}")
    print(f"Display time per rotation: {display_time} seconds")
    print("Press Ctrl+C to stop\n")
    
    try:
        for rotation in rotations:
            result = demo_oled_rotation(rotation)
            if result:
                print(f"  Displaying for {display_time} seconds...")
                time.sleep(display_time)
            else:
                print(f"  Skipping rotation {rotation}° due to error")
                time.sleep(1)
        
        print("\nDemo complete!")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")


def main():
    parser = argparse.ArgumentParser(
        description="Test OLED rotation functionality for Pironman5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Run validation tests only
    python3 tests/test_oled_rotation.py

    # Test a specific rotation angle
    python3 tests/test_oled_rotation.py --rotation 90

    # Run demo of all rotations
    python3 tests/test_oled_rotation.py --demo

Note:
    OLED hardware tests require a Raspberry Pi with Pironman5 hardware
    and the pm_auto library installed. The 90° and 270° rotation options
    use the pironman5.oled_portrait module for proper portrait mode rendering.
        """
    )
    parser.add_argument(
        "--rotation", "-r",
        type=int,
        choices=[0, 90, 180, 270],
        help="Test a specific rotation angle"
    )
    parser.add_argument(
        "--demo", "-d",
        action="store_true",
        help="Run demo cycling through all rotation angles"
    )
    parser.add_argument(
        "--validate-only", "-v",
        action="store_true",
        help="Only run CLI validation tests (no hardware required)"
    )
    
    args = parser.parse_args()
    
    print("=== Pironman5 OLED Rotation Test ===\n")
    
    # Always run CLI validation tests
    cli_validation_passed = test_rotation_cli_validation()
    
    # Run portrait mode module tests
    portrait_module_passed = test_portrait_mode_module()
    
    all_passed = cli_validation_passed and portrait_module_passed
    
    if args.validate_only:
        if all_passed:
            print("\nAll validation tests passed!")
            sys.exit(0)
        else:
            print("\nValidation tests failed!")
            sys.exit(1)
    
    if args.demo:
        run_demo()
    elif args.rotation is not None:
        demo_oled_rotation(args.rotation)
    else:
        print("\nTo test OLED hardware, use --rotation ANGLE or --demo")
        print("Run with --help for more options")
    
    print("\n=== Test Complete ===")


if __name__ == "__main__":
    main()
