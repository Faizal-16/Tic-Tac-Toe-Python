"""
Unbeatable Tic-Tac-Toe AI - Simple AI College Project
-----------------------------------------------------
The computer plays 'O' using the Minimax algorithm with Alpha-Beta pruning.
You play 'X'. The best you can do against it is a draw.

Run:  python tictactoe_ai.py          (opens the GUI)
      python tictactoe_ai.py --test   (AI vs random players, no GUI)
"""

import sys
import random

HUMAN, AI, EMPTY = "X", "O", " "
WIN_LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
             (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
             (0, 4, 8), (2, 4, 6)]              # diagonals

nodes_explored = 0  # counter to show how much work the AI does


# ---------------------------- Game logic ----------------------------
def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    return EMPTY not in board


def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == EMPTY]


# ---------------------------- The AI --------------------------------
def minimax(board, is_ai_turn, alpha, beta, depth):
    """Return the score of a position. AI win = +10, human win = -10.
    Faster wins / slower losses are preferred via the depth term."""
    global nodes_explored
    nodes_explored += 1

    w = winner(board)
    if w == AI:
        return 10 - depth
    if w == HUMAN:
        return depth - 10
    if is_full(board):
        return 0

    if is_ai_turn:                      # AI tries to MAXIMIZE the score
        best = -float("inf")
        for move in available_moves(board):
            board[move] = AI
            best = max(best, minimax(board, False, alpha, beta, depth + 1))
            board[move] = EMPTY
            alpha = max(alpha, best)
            if beta <= alpha:           # alpha-beta pruning
                break
        return best
    else:                               # Human tries to MINIMIZE the score
        best = float("inf")
        for move in available_moves(board):
            board[move] = HUMAN
            best = min(best, minimax(board, True, alpha, beta, depth + 1))
            board[move] = EMPTY
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def best_move(board):
    global nodes_explored
    nodes_explored = 0
    best_score, move = -float("inf"), None
    for m in available_moves(board):
        board[m] = AI
        score = minimax(board, False, -float("inf"), float("inf"), 1)
        board[m] = EMPTY
        if score > best_score:
            best_score, move = score, m
    return move


# ---------------------------- Test mode -----------------------------
def self_test(games=300):
    """AI (as O) vs a random player (as X). The AI must never lose."""
    results = {"AI wins": 0, "Draws": 0, "AI losses": 0}
    for _ in range(games):
        board = [EMPTY] * 9
        human_turn = random.random() < 0.5
        while not winner(board) and not is_full(board):
            if human_turn:
                board[random.choice(available_moves(board))] = HUMAN
            else:
                board[best_move(board)] = AI
            human_turn = not human_turn
        w = winner(board)
        results["AI wins" if w == AI else "AI losses" if w == HUMAN else "Draws"] += 1
    print(f"Results over {games} games vs a random player: {results}")
    assert results["AI losses"] == 0, "AI should never lose!"
    print("PASS: the AI never lost.")


# ---------------------------- GUI -----------------------------------
def run_gui():
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.title("Unbeatable Tic-Tac-Toe AI")
    board = [EMPTY] * 9
    buttons = []
    info = tk.Label(root, text="Your turn (X)", font=("Arial", 14))
    info.grid(row=0, column=0, columnspan=3, pady=8)

    def end_game():
        w = winner(board)
        msg = "You win!" if w == HUMAN else "AI wins!" if w == AI else "It's a draw!"
        messagebox.showinfo("Game over", msg)
        reset()

    def reset():
        for i in range(9):
            board[i] = EMPTY
            buttons[i].config(text=" ", state="normal")
        info.config(text="Your turn (X)")

    def click(i):
        if board[i] != EMPTY:
            return
        board[i] = HUMAN
        buttons[i].config(text=HUMAN, fg="blue")
        if winner(board) or is_full(board):
            return end_game()
        move = best_move(board)
        board[move] = AI
        buttons[move].config(text=AI, fg="red")
        info.config(text=f"AI checked {nodes_explored} positions. Your turn!")
        if winner(board) or is_full(board):
            end_game()

    for i in range(9):
        b = tk.Button(root, text=" ", font=("Arial", 28, "bold"), width=4, height=2,
                      command=lambda i=i: click(i))
        b.grid(row=1 + i // 3, column=i % 3, padx=3, pady=3)
        buttons.append(b)

    tk.Button(root, text="New Game", command=reset).grid(row=4, column=0, columnspan=3, pady=8)
    root.mainloop()


if __name__ == "__main__":
    if "--test" in sys.argv:
        self_test()
    else:
        run_gui()
