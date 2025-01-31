import tkinter as tk
from service import Service
import os
from game_7_players import Game
from extractor import Extractor
from typing import Optional
from game_7_players import UTG, CO, LJ, HJ, BTN, SB, BB, Player
from app_helper import AppHelper

app_helper = AppHelper()
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

    # start game if not game 
    if game is None:
        game = Game(bb=bb, total_pot=0, effective_stack=0)

    # Extract total pot data
    extractor.crop_zone(zone=extractor.TOTAL_POT_ZONE, ofp="zones/total_pot.png", ifp=screenshot_path)
    game.total_pot = float(extractor.tesseract_number_recognition("zones/total_pot.png"))
    
    # Extract board cards
    for card_number, card_zone in extractor.BOARD_CARD_ZONES.items():
        extractor.crop_zone(zone=card_zone, ifp=screenshot_path, ofp=f"zones/board/{card_number}.png")
        card_symbol = extractor.tesseract_text_recognition(f"zones/board/{card_number}.png").strip()
        if not card_symbol in available_card_symbols:
            break
        card_suit = extractor.identify_card_suit(f"zones/board/{card_number}.png")
        card = card_symbol + card_suit
        game.board_cards.append(card)

    # Extract player data
    data = app_helper.extract_player_data(screenshot_path)
    unactive_player_numbers:list = data[0]
    btn_player_number: Optional[int] = data[1]
    hero_player_number: Optional[int] = data[2]
    hero_hole_cards: Optional[str] = data[3]
    effective_stack: Optional[float] = data[4]

    # define players and positions
    positions = [SB, BB, UTG, LJ, HJ, CO]
    player_positions = {btn_player_number: BTN}
    hero_position = None

        # move of genious - I know :)
    for index, position in enumerate(positions):
        player_number = btn_player_number + index + 1
        if player_number > 7:
            player_number -= 7

        player_positions[player_number] = position

    player1 = player_positions[1](game, effective_stack=effective_stack)
    player2 = player_positions[2](game, effective_stack=effective_stack)
    player3 = player_positions[3](game, effective_stack=effective_stack)
    player4 = player_positions[4](game, effective_stack=effective_stack)
    player5 = player_positions[5](game, effective_stack=effective_stack)
    player6 = player_positions[6](game, effective_stack=effective_stack)
    player7 = player_positions[7](game, effective_stack=effective_stack)

    we_are = UTG(game)

    # define who we are
    if hero_player_number == 1:
        we_are = player1
    elif hero_player_number == 2:
        we_are = player2
    elif hero_player_number == 3:
        we_are = player3
    elif hero_player_number == 4:
        we_are = player4
    elif hero_player_number == 5:
        we_are = player5
    elif hero_player_number == 6:
        we_are = player6
    elif hero_player_number == 7:
        we_are = player7


    # TODO: resolve, because may cause problems
    for player_number, position in player_positions.items():
        if player_number in unactive_player_numbers:
            try:
                game.active_positions.remove(position.position)
            except ValueError:
                pass

    # Update UI vars
    total_pot_var.set(f"Total pot: {game.total_pot}$")
    effective_stack_var.set(f"Effective stack: {effective_stack}")
    board_cards_var.set(f"Board cards: {game.board_cards}")
    hero_position_var.set(f"Hero position: {we_are.position}")
    hole_cards_var.set(f"Hole cards: {we_are.hole_cards}")
    active_opponents_var.set(f"Active opponents: {game.active_positions}")
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

