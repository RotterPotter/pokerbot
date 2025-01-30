import tkinter as tk
from service import Service
import os


service = Service()

def extract_info():
    """Updates the UI with extracted poker information."""
    screen_region = {
                "left": 0,
                "top": 0,
                "width": 1230,
                "height": 930,
            }
    
    service.capture_screen('screenshot.png')
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

