import tkinter as tk
from tkinter import messagebox
from service import capture_screen

def capture_and_evaluate():
    capture_screen()
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
