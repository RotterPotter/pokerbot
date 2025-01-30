import tkinter as tk
from service import Service
import os
from game_7_players import Game
from extractor import Extractor
from typing import Optional

service = Service()
extractor = Extractor()
game = None
available_card_symbols = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]

def extract_info():
    global game
    """Updates the UI with extracted poker information."""
    # Captures the screen
    screenshot_path = 'game_screenshot.png'
    service.capture_screen(screenshot_path)

    # Set testing BB
    # TODO: implement BB extraction or BB input
    bb:float = 1

    # Extract total pot data
    extractor.crop_zone(zone=extractor.TOTAL_POT_ZONE, ofp="zones/total_pot.png", ifp=screenshot_path)
    total_pot:float = extractor.tesseract_number_recognition("zones/total_pot.png")


    # Extract board cards
    board_cards:list = list()
    for card_number, card_zone in extractor.BOARD_CARD_ZONES.items():
        extractor.crop_zone(zone=card_zone, ifp=screenshot_path, ofp=f"zones/board/{card_number}.png")
        card_symbol = extractor.tesseract_text_recognition(f"zones/board/{card_number}.png").strip()
        if not card_symbol in available_card_symbols:
            break
        card_suit = extractor.identify_card_suit(f"zones/board/{card_number}.png")
        card = card_symbol + card_suit
        board_cards.append(card)

    # Extract player data
    unactive_player_numbers:list = []
    pots: dict = {}
    btn_player_number: Optional[int] = None
    hero_player_number: Optional[int] = None
    hero_hole_cards: Optional[str] = None
    effective_stack: Optional[float] = None

    for player_number in range(8):
        # crop player hole cards zonez
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
                continue

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
            # update pots dict with player's pot
            pot = float(pot)
            pots.update(player_number, pot)
            # set effective stack to pot value if pot value is smaller
            if pot < effective_stack:
                effective_stack = pot

    
    # Creates a game object if not created
    if game is None:
        game = Game()

    # Updates UI vars
    total_pot_var.set(f"Total pot: 423.5$")
    effective_stack_var.set(f"Effective stack: 1200$")
    board_cards_var.set(f"Board cards: ['Ks', '9h', 'Ah']")
    hero_position_var.set(f"Hero position: UTG")
    hole_cards_var.set(f"Hole cards: As3h")
    active_opponents_var.set(f"Active opponents: ['LJ', 'CO', 'BTN']")
    print("Extract Info triggered! Variables updated.")

def build_strategy():
    """Placeholder function for strategy building."""
    print("Build strategy triggered!")

def create_ui():
    global total_pot_var, effective_stack_var, board_cards_var
    global hero_position_var, hole_cards_var, active_opponents_var

    root = tk.Tk()
    root.title("Poker UI")
    root.geometry("400x300")  # Increased width for better spacing

    # Frame for buttons
    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

    # Buttons
    btn_extract = tk.Button(
        top_frame, text="Extract Info", command=extract_info,
        bg="blue", fg="white", width=15, height=2
    )
    btn_extract.pack(side=tk.RIGHT, padx=10)

    btn_build = tk.Button(
        top_frame, text="Build Strategy", command=build_strategy,
        bg="green", fg="white", width=15, height=2
    )
    btn_build.pack(side=tk.RIGHT, padx=10)

    # UI config
    font = ("Arial", 10)

    # Tkinter StringVars (Auto-Updating Variables)
    total_pot_var = tk.StringVar(value="Total pot: --")
    effective_stack_var = tk.StringVar(value="Effective stack: --")
    board_cards_var = tk.StringVar(value="Board cards: --")
    hero_position_var = tk.StringVar(value="Hero position: --")
    hole_cards_var = tk.StringVar(value="Hole cards: --")
    active_opponents_var = tk.StringVar(value="Active opponents: --")

    # Frame for labels (Container for left & right info)
    info_frame = tk.Frame(root)
    info_frame.pack(side="top", fill="both",  padx=10)

    # Left side frame 
    left_info_frame = tk.Frame(info_frame)
    left_info_frame.pack(side="left", expand=True, fill="both")

    # Labels (Left side)
    tk.Label(left_info_frame, textvariable=total_pot_var, font=font).pack(anchor="w", padx=3, pady=1)
    tk.Label(left_info_frame, textvariable=hole_cards_var, font=font).pack(anchor="w", padx=3, pady=1)

    # Center separator (Visual Line)
    separator = tk.Frame(info_frame, width=1, bg="")
    separator.pack(side="left", fill="y", padx=10)

    # Right side frame 
    right_info_frame = tk.Frame(info_frame)
    right_info_frame.pack(side="left", expand=True, fill="both")


    # Labels (Right side)
    tk.Label(right_info_frame, textvariable=effective_stack_var, font=font).pack(anchor="w", padx=3, pady=1)
    tk.Label(right_info_frame, textvariable=hero_position_var, font=font).pack(anchor="w", padx=3, pady=1)

    # Bottom frame 
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side="top",  fill="both", padx=10)

    # Labels (Bottom) 
    tk.Label(bottom_frame, textvariable=board_cards_var, font=font).pack(anchor="w", padx=3, pady=1)
    tk.Label(bottom_frame, textvariable=active_opponents_var, font=font).pack(anchor="w", padx=3, pady=1)
    
    # Bottom separator (Visual Line)
    bottom_separator = tk.Frame(root, width=100, bg="black")
    bottom_separator.pack(side="top", fill="both")

    # Strategy frame
    strategy_frame = bottom_separator = tk.Frame(root)
    strategy_frame.pack(side="top",  fill="both", padx=3)

    # Labels (Strategy frame)
    tk.Label(strategy_frame, text="Strategy will be here", font=font).pack(anchor="w", padx=3, pady=1)

    
    root.mainloop()

if __name__ == "__main__":
    create_ui()

