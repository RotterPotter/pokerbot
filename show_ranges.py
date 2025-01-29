from game_7_players import UTG, SB, BB, LJ, HJ, CO, BTN, Player
from typing import List


positions = ["SB", "BB", "UTG", "LJ", "HJ", "CO", "BTN"]
position_classes: List[Player] = [SB, BB, UTG, LJ, HJ, CO, BTN]

if __name__ == "__main__":
  for class_index, position_class in enumerate(position_classes):
    class_string = positions[class_index]
    for string_index, position_string in enumerate(positions):
      if class_index == string_index:
        continue
      try:
        hero_range, opponent_range = position_class.get_ranges(opponent_position=position_string)
      except TypeError:
        print(f"{class_string} vs {position_string}: NOT IMPLEMENTED")
        continue
      print(f"{class_string} vs {position_string}:\n---{class_string} range: {hero_range}\n---{position_string} range: {opponent_range}")

