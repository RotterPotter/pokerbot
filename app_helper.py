from extractor import Extractor
from typing import Dict, List, Optional

extractor = Extractor()

class AppHelper:

  def extract_player_data(self, screenshot_path: str):
    available_card_symbols:Dict[str] = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
    unactive_player_numbers:List[int] = []
    btn_player_number: Optional[int] = None
    hero_player_number: Optional[int] = None
    hero_hole_cards: Optional[str] = None
    effective_stack:Optional[float] = None

    for player_number in range(1, 8):
        # crop player hole cards zonez
        print(player_number)
        extractor.crop_zone(zone=extractor.PLAYER_ZONES[player_number]["first_card"], ifp=screenshot_path, ofp=f"zones/p{player_number}/first_card.png")
        extractor.crop_zone(zone=extractor.PLAYER_ZONES[player_number]["second_card"],ifp=screenshot_path, ofp=f"zones/p{player_number}/second_card.png")

        first_card_symbol = extractor.tesseract_text_recognition(f"zones/p{player_number}/first_card.png").strip()
        second_card_symbol = extractor.tesseract_text_recognition(f"zones/p{player_number}/second_card.png").strip()
        
        # unactivate user if no cards in hand (even if he isn't a hero)
        if first_card_symbol not in available_card_symbols:
            card_color_hex = extractor.get_most_frequent_non_white_color(f"zones/p{player_number}/first_card.png")
            # unactivate user 
            if extractor.classify_color(card_color_hex) != "red":
                unactive_player_numbers.append(player_number)

        if hero_player_number is not None:
            # udentify hole cards if possible and if not identified
            if first_card_symbol in available_card_symbols and second_card_symbol in available_card_symbols:
                first_card_suit = extractor.identify_card_suit(f"zones/p{player_number}/first_card.png")
                second_card_suit = extractor.identify_card_suit(f"zones/p{player_number}/second_card.png")
                hero_hole_cards = first_card_symbol + first_card_suit + second_card_symbol + second_card_suit

            hero_player_number = player_number

        # check if player is BTN if not btn_player identified yet
        if btn_player_number is None:
            # crop dealer zone
            extractor.crop_zone(zone=extractor.PLAYER_ZONES[player_number]["dealer"], ifp=screenshot_path, ofp=f"zones/p{player_number}/dealer.png")
            # extract "D" from dealer zone
            extracted_string = extractor.tesseract_text_recognition(f"zones/p{player_number}/dealer.png")
            # if "D" extracted, player is button
            if extracted_string.strip().upper() == "D":
                btn_player_number = player_number
        
        # extract player's pot
        extractor.crop_zone(extractor.PLAYER_ZONES[player_number]["pot"], ifp=screenshot_path, ofp=f"zones/p{player_number}/pot.png")
        pot = extractor.tesseract_number_recognition(f"zones/p{player_number}/pot.png").strip()
        if pot == "":
            # unactivate player 
            unactive_player_numbers.append(player_number)
        else:
            if effective_stack is None:
              effective_stack = pot
            # set effective stack to pot value if pot value is smaller
            if pot < effective_stack:
                effective_stack = pot
    
    return [unactive_player_numbers, btn_player_number, hero_player_number, hero_hole_cards, effective_stack]