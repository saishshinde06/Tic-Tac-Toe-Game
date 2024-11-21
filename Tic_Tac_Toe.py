import tkinter as tk
from tkinter import messagebox

# Initialize the main application window
root = tk.Tk()
root.title("Tic Tac Toe - Player vs Computer")
root.configure(bg="#f0f8ff")  # Set background color

# Global variables
player = "X"  # Human player
computer = "O"  # AI
board = [""] * 9

# Colors
BUTTON_BG = "#87cefa"  # Button background color
BUTTON_FG = "#000080"  # Button text color
RESET_BG = "#ff4500"  # Reset button background color
RESET_FG = "#ffffff"  # Reset button text color

# Reset the game
def reset_game():
    global board, player
    board = [""] * 9
    player = "X"
    for btn in buttons:
        btn.config(text="", state=tk.NORMAL, bg=BUTTON_BG)

# Check for a winner
def check_winner():
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    return None

# Check if the board is full
def is_draw():
    return all(cell != "" for cell in board)

# Minimax algorithm for AI
def minimax(is_maximizing):
    winner = check_winner()
    if winner == computer:
        return 1
    elif winner == player:
        return -1
    elif is_draw():
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = computer
                score = minimax(False)
                board[i] = ""
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = player
                score = minimax(True)
                board[i] = ""
                best_score = min(best_score, score)
        return best_score

# Computer makes a move
def computer_move():
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = computer
            score = minimax(False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    if move is not None:
        board[move] = computer
        buttons[move].config(text=computer, state=tk.DISABLED, bg="#ffcccb")
        winner = check_winner()
        if winner:
            messagebox.showinfo("Tic Tac Toe", f"Computer ({computer}) wins!")
            reset_game()
        elif is_draw():
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
            reset_game()

# Handle player move
def button_click(index):
    global player
    if board[index] == "":
        board[index] = player
        buttons[index].config(text=player, state=tk.DISABLED, bg="#98fb98")
        winner = check_winner()
        if winner:
            messagebox.showinfo("Tic Tac Toe", f"Player ({player}) wins!")
            reset_game()
        elif is_draw():
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
            reset_game()
        else:
            computer_move()

# Create buttons for the grid
buttons = []
for i in range(9):
    btn = tk.Button(
        root, text="", font=("Arial", 24), width=5, height=2, bg=BUTTON_BG, fg=BUTTON_FG,
        command=lambda i=i: button_click(i)
    )
    btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
    buttons.append(btn)

# Add a reset button
reset_btn = tk.Button(
    root, text="Reset", font=("Arial", 16), bg=RESET_BG, fg=RESET_FG, command=reset_game
)
reset_btn.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

# Start the GUI event loop
root.mainloop()
