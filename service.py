import mss
import mss.tools
import cv2
import pytesseract
import dotenv
import os
from pydantic import BaseModel
from typing import List
import requests
from itertools import product

class SolvePost(BaseModel):
  hero_role:str
  hole_cards:str
  pot: float
  effective_stack: float
  board: List[str]
  range_ip: List[str]
  range_oop: List[str]
  game_stage: str
  bet_size_IP_bet: int
  bet_size_IP_raise: int
  bet_size_OOP_bet: int
  bet_size_OOP_raise: int
  accuracy: float
  max_iteration: int
  use_isomorphism: int
  allin_threshold: float
  et_thread_num: int

dotenv.load_dotenv()
class Service:
    SERVER_URL = r'http://localhost:8000'

    def capture_screen(self, output_path="screenshot.png", region=None):
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
    
    def extract_info(self, image_path:str):
        pass

    def send_data_to_solver(self, data: SolvePost):
        response = requests.post(
            f'{self.SERVER_URL}/solve',
            json=data.model_dump()  # Use the `json` parameter to send the data as JSON
        )
        try:
            return response.json() # Print the JSON response from the server
        except requests.exceptions.JSONDecodeError:
            print(f"Failed to decode JSON response: {response.text}")

    def generate_auto_ranges(self, board_cards, hole_cards, player_role):
        """
        Automatically generate OOP and IP ranges given a board and hero hole cards.

        :param board_cards: List[str] - The community cards on the board (e.g. ["Ks", "9s", "8d", "Qd"]).
        :param hole_cards:  List[str] - The 2 known hole cards for exactly one player (e.g. ["Ah", "Kh"]).
        :param player_role: str       - The role of the player with the known hole cards: "OOP" or "IP".

        :return: dict with two keys:
                {
                "OOP": [...],  # all combos (in condensed form) for OOP
                "IP":  [...],  # all combos (in condensed form) for IP
                }
        """
        import itertools

        # ------------------------------
        # 1) Basic definitions
        # ------------------------------
        ranks = "AKQJT98765432"  # Descending rank order
        suits = "shdc"           # Suit order doesn't matter much, but let's define it
        used_cards = set(board_cards + hole_cards)  # All blocked cards

        # ------------------------------
        # 2) Utility to condense a 2-card hand
        #    e.g. condense_2card_hand("Jh","Kh") -> "KJs"
        # ------------------------------
        def condense_2card_hand(card1, card2):
            """
            Given two explicit cards like "Jh" (Jack of hearts) and "Kh" (King of hearts),
            return condensed notation like "KJs" if they are suited, "KJo" if off-suit,
            or "JJ" / "KK" for pairs.
            """
            rank1, suit1 = card1[0], card1[1]
            rank2, suit2 = card2[0], card2[1]
            idx1 = ranks.index(rank1)
            idx2 = ranks.index(rank2)

            # Pocket pair case
            if rank1 == rank2:
                return rank1 + rank2  # e.g. "JJ", "KK"

            # Otherwise figure out which rank is higher (lower index in 'ranks')
            if idx1 < idx2:
                high_rank, low_rank = rank1, rank2
                high_suit, low_suit = suit1, suit2
            else:
                high_rank, low_rank = rank2, rank1
                high_suit, low_suit = suit2, suit1

            # Check if suits match
            if high_suit == low_suit:
                return high_rank + low_rank + 's'
            else:
                return high_rank + low_rank + 'o'

        # ------------------------------
        # 3) Build a deck and remove used_cards
        # ------------------------------
        full_deck = [r + s for r in ranks for s in suits]  # e.g. "As", "Ah", "Ad", "Ac", "Ks", ...
        available_cards = [c for c in full_deck if c not in used_cards]

        # ------------------------------
        # 4) Generate all possible combos from the remaining deck
        # ------------------------------
        valid_condensed_combos = set()
        for c1, c2 in itertools.combinations(available_cards, 2):
            combo = condense_2card_hand(c1, c2)
            valid_condensed_combos.add(combo)

        # Convert the hero hole cards into condensed notation
        hero_combo = condense_2card_hand(hole_cards[0], hole_cards[1])

        # ------------------------------
        # 5) Assign ranges based on player_role
        # ------------------------------
        # The known hole cards should go to whichever role the hero is playing;
        # the other role gets the full filtered range.
        if player_role == "OOP":
            oop_range = [hero_combo]
            ip_range  = sorted(valid_condensed_combos)
        else:  # player_role == "IP"
            oop_range = sorted(valid_condensed_combos)
            ip_range  = [hero_combo]

        return {
            "OOP": oop_range,
            "IP":  ip_range
        }

    def define_game_stage(self, board: List[str]):
        """
        Return the stage name ("flop", "turn", or "river") given the list of board cards.
        """
        stages = {
            3: "flop",
            4: "turn",
            5: "river"
        }
        return stages[len(board)]


