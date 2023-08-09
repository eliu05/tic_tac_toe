import tkinter as tk
from tkinter import messagebox

# Initialize the Tic Tac Toe board
board = [' ' for _ in range(9)]

def print_board():
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i+1]} | {board[i+2]}")
        if i < 6:
            print("-" * 9)

def is_winner(board, player):
    win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]
    for combo in win_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

def is_board_full(board):
    return all(cell != ' ' for cell in board)

def get_empty_cells(board):
    return [i for i, cell in enumerate(board) if cell == ' ']

def minimax(board, depth, maximizing_player):
    if is_winner(board, 'X'):
        return -1
    if is_winner(board, 'O'):
        return 1
    if is_board_full(board):
        return 0
    
    if maximizing_player:
        max_eval = float('-inf')
        for empty_cell in get_empty_cells(board):
            board[empty_cell] = 'O'
            eval = minimax(board, depth + 1, False)
            board[empty_cell] = ' '
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for empty_cell in get_empty_cells(board):
            board[empty_cell] = 'X'
            eval = minimax(board, depth + 1, True)
            board[empty_cell] = ' '
            min_eval = min(min_eval, eval)
        return min_eval

def get_best_move(board):
    best_move = None
    best_eval = float('-inf')
    for empty_cell in get_empty_cells(board):
        board[empty_cell] = 'O'
        eval = minimax(board, 0, False)
        board[empty_cell] = ' '
        if eval > best_eval:
            best_eval = eval
            best_move = empty_cell
    return best_move

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.root, text=' ', font=('normal', 24), height=2, width=5,
                               command=lambda idx=i: self.make_move(idx))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

    def make_move(self, idx):
        if board[idx] == ' ':
            board[idx] = 'X'
            self.buttons[idx].config(text='X', state=tk.DISABLED)
            if is_winner(board, 'X'):
                self.show_message("Congratulations! You win!")
                self.reset_game()
            elif is_board_full(board):
                self.show_message("It's a tie!")
                self.reset_game()
            else:
                computer_move = get_best_move(board)
                board[computer_move] = 'O'
                self.buttons[computer_move].config(text='O', state=tk.DISABLED)
                if is_winner(board, 'O'):
                    self.show_message("Computer wins! Better luck next time.")
                    self.reset_game()
                elif is_board_full(board):
                    self.show_message("It's a tie!")
                    self.reset_game()

    def show_message(self, message):
        messagebox.showinfo("Game Over", message)

    def reset_game(self):
        for i in range(9):
            board[i] = ' '
            self.buttons[i].config(text=' ', state=tk.NORMAL)

def main():
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()