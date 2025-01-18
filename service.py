import mss
import mss.tools

def capture_screen(output_path="screenshot.png", region=None):
    """
    Captures the screen and saves the screenshot as an image.

    Parameters:
    - output_path (str): Path to save the screenshot.
    - region (dict or None): A dictionary specifying the region to capture. 
      Keys are 'top', 'left', 'width', 'height'.
      If None, captures the entire screen.

    Returns:
    - str: Path to the saved screenshot.
    """
    with mss.mss() as sct:
        # Capture the entire screen if region is not provided
        if region is None:
            screenshot = sct.shot(output=output_path)
        else:
            # Validate the region keys
            if not all(key in region for key in ('top', 'left', 'width', 'height')):
                raise ValueError("Region must have 'top', 'left', 'width', and 'height' keys.")
            # Capture the specified region
            screenshot = sct.grab(region)
            # Save the image
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_path)
        
        print(f"Screenshot saved at: {output_path}")
        return output_path
