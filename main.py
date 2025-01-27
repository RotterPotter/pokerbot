import tkinter as tk
from tkinter import messagebox
from service import Service, SolvePost


service = Service()

def capture_and_evaluate():
    # output_path = service.capture_screen()
    # service.extract_info(output_path)

    # TEST
    board = ["9c", "8c", "3h"]
    game_stage = service.define_game_stage(board)
    hero_hole = ["Jh", "Kh"]  
    role = "OOP"
    ranges = service.generate_auto_ranges(board, hero_hole, role)
    print(ranges)
    range_ip=ranges["IP"]
    range_oop=ranges["OOP"]
    bet_size_ip_bet = 50
    bet_size_ip_raise = 60
    bet_size_oop_bet = 50
    bet_size_oop_raise = 60

    response = service.send_data_to_solver(
        SolvePost(
            hole_cards="".join(hero_hole),
            pot=4,
            effective_stack=10,
            board=board,
            range_ip=range_ip,
            range_oop=range_oop,
            game_stage=game_stage,
            bet_size_IP_bet=bet_size_ip_bet,
            bet_size_IP_raise=bet_size_ip_raise,
            bet_size_OOP_bet=bet_size_oop_bet,
            bet_size_OOP_raise=bet_size_oop_raise,
            accuracy=0.05,
            max_iteration=200,
            use_isomorphism=1,
            allin_threshold=0.67,
            et_thread_num=8

        )
    )
    print(response)

    # Simulate the evaluation process
    suggested_action = "Call"  # Replace with the result from your evaluation algorithm
    result_label.config(text=f"Suggested Action: {suggested_action}")

# Create the main application window
root = tk.Tk()
root.title("Poker Bot Assistant")
root.geometry("400x200")

# Create a label for instructions
instructions_label = tk.Label(root, text="Click the button to capture and evaluate your poker turn.", font=("Arial", 12))
instructions_label.pack(pady=10)

# Create a button to trigger the capture and evaluation
capture_button = tk.Button(root, text="Capture and Evaluate", font=("Arial", 12), command=capture_and_evaluate)
capture_button.pack(pady=10)

# Create a label to display the suggested action
result_label = tk.Label(root, text="Suggested Action: None", font=("Arial", 14, "bold"), fg="blue")
result_label.pack(pady=20)

# Run the application
root.mainloop()
