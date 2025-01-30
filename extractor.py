import cv2
import os
from typing import Dict
import pytesseract
import numpy as np
from collections import Counter
import math

class Extractor:
  """
    players
                  5
              4       6
              3       7
                2   1
  """
  PLAYER_ZONES: Dict = {
    1: {
      "dealer": (600, 600, 700, 680),
      "first_card": (770, 600, 820, 655),
      "second_card": (825, 600, 870, 655),
      "pot": (788, 690, 870, 710)
      },
    2: {
      "dealer": (260, 615, 295, 660),
      "first_card": (380, 600, 430, 650),
      "second_card": (440, 600, 480, 650),
      "pot": (378, 688, 500, 710)
      },
    3: {
      "dealer": (200, 570, 240, 615),
      "first_card": (111, 440, 160, 480),
      "second_card": (170, 440, 212, 480),
      "pot": (113, 523, 234, 549)
      },
    4: {
      "dealer": (170, 320, 215, 360),
      "first_card": (140, 185, 180, 230),
      "second_card": (196, 185, 240, 230),
      "pot": (135, 265, 250, 290)
      },
    5: {
      "dealer": (465, 220, 510, 265),
      "first_card": (580, 90, 620, 135),
      "second_card": (636, 90, 675, 135),
      "pot": (576, 172, 693, 193)
      },
    6: {
      "dealer": (1025, 320, 1070, 365),
      "first_card": (1050, 180, 1095, 230),
      "second_card": (1110, 180, 1150, 230),
      "pot": (1050, 268, 1160, 290)
      },
    7: {
      "dealer": (970, 580, 1020, 625),
      "first_card": (1070, 440, 1110, 489),
      "second_card": (1122, 440, 1165, 489),
      "pot": (1068, 523, 1180, 545)
      }
  }


  TOTAL_POT_ZONE = (335, 120, 425, 142)

  BOARD_CARD_ZONES = {
     1: (438, 400, 500, 465),
     2: (515, 400, 570, 465),
     3: (585, 400, 645, 465),
     4: (660, 400, 720, 465),
     5: (730, 400, 793, 465)
  }

  SUIT_COLORS = {
     "blue": "d",
     "red": "h",
     "green": "c",
     "black": "s",
  }

  def crop_zone(self, zone: tuple, ofp:str, ifp:str="testing.png"):
    """
      Takes zone,  output file path (ofp) and input file path (ifp (optional))
        format of zone: (x1, y1, x2, y2)
      Crop zone and saves cropped iamge to ofp.
    """
    # delete previous cropped zone image if exists
    if os.path.exists(ofp):
      os.remove(ofp)
    
    if os.path.exists(ifp):
      x1, y1, x2, y2 = zone
      image = cv2.imread(ifp)
      cropped = image[y1:y2, x1:x2]
      cv2.imwrite(ofp, cropped)

  def tesseract_text_recognition(self, ifp:str) -> str:
    image = cv2.imread(ifp)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to enhance text contrast
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Perform OCR
    custom_config = r'--oem 3 --psm 6'  # Optimize for normal text recognition
    extracted_text = pytesseract.image_to_string(thresh, config=custom_config)

    return extracted_text
  
  def tesseract_number_recognition(self, ifp:str) -> str:
      # Load the image
      image = cv2.imread(ifp)

      # Convert to grayscale
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

      # Apply thresholding to enhance text contrast
      _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

      # Perform OCR with Tesseract (restricting to numbers only)
      custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.'
      extracted_text = pytesseract.image_to_string(thresh, config=custom_config)

      # Return the most relevant number
      return extracted_text


  def get_most_frequent_non_white_color(self, image_path):
      # Load the image
      image = cv2.imread(image_path)
      if image is None:
          raise ValueError("Error: Could not load image. Check the file path.")
      
      # Convert BGR to RGB (OpenCV loads images in BGR format by default)
      image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

      # Reshape image to a list of pixels
      pixels = image_rgb.reshape(-1, 3)

      # Filter out white pixels (255,255,255) and near-white shades
      filtered_pixels = [tuple(map(int, color)) for color in pixels if sum(map(int, color)) < 750]


      # Check if any colors remain after filtering
      if not filtered_pixels:
          raise ValueError("Error: No non-white colors found in the image.")

      # Count the most common remaining colors
      color_counts_filtered = Counter(filtered_pixels)
      most_frequent_non_white_color = color_counts_filtered.most_common(1)[0][0]

      # Convert RGB to HEX
      hex_color_non_white = "#{:02x}{:02x}{:02x}".format(*most_frequent_non_white_color)

      return hex_color_non_white
  
  def classify_color(self, hex_code):
    # Strip out any leading '#' and make sure the hex is in a standard 6- or 8-digit form
    hex_code = hex_code.strip().lstrip('#')
    
    # If there's an alpha channel (8 digits: e.g., AARRGGBB), parse only RR, GG, BB
    # If 6 digits (RR, GG, BB), we take them directly
    if len(hex_code) == 8:
        # The first two are alpha, so skip them
        hex_code = hex_code[2:]
    elif len(hex_code) != 6:
        raise ValueError("Hex code must be 6 digits (RGB) or 8 digits (AARRGGBB).")
    
    # Convert the remaining RR, GG, BB to integer values
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    
    # Reference colors we want to classify against
    reference_colors = {
        'red':   (255, 0, 0),
        'green': (0, 128, 0),   # a "medium" green
        'blue':  (0, 0, 255),
        'black': (0, 0, 0)
    }
    
    def euclidean_distance(c1, c2):
        # Euclidean distance in RGB space
        return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)
    
    # Find the closest reference color
    closest_color = None
    min_distance = float('inf')
    
    for color_name, (cr, cg, cb) in reference_colors.items():
        dist = euclidean_distance((r, g, b), (cr, cg, cb))
        if dist < min_distance:
            min_distance = dist
            closest_color = color_name
    
    return closest_color
  
  def identify_card_suit(self, ifp:str) -> str:
     hex = self.get_most_frequent_non_white_color(ifp)
     color = self.classify_color(hex)
     return self.SUIT_COLORS[color]
  
  



