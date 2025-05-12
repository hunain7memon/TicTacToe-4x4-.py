import tkinter as tk
import math
import time
import sys
from copy import deepcopy

size = 4
x_player = 'X'
o_player = 'O'
board = [' ' for _ in range(16)]

win_conditions = [
        [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15],
        [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15],
        [0, 5, 10, 15], [3, 6, 9, 12]
    ]

def is_winner(brd, player):
    return any(all(brd[i] == player for i in cond) for cond in win_conditions)

def is_draw(brd):
    return all(cell != ' ' for cell in brd)

def get_available_moves(brd):
    return [i for i, val in enumerate(brd) if val == ' ']

def do_block_move(board):
    for line in win_conditions:
        x_count = sum(1 for i in line if board[i] == 'X')
        o_count = sum(1 for i in line if board[i] == 'O' or board[i] == 'B')
        empty = [i for i in line if board[i] == ' ']

        if x_count >= 3 and o_count == 0 and len(empty) > 0:
            return empty[0]  
    return None

def do_swap_move(board):
    for line in win_conditions:
        o_indices = [i for i in line if board[i] == 'O']
        blockers = [i for i in line if board[i] in ['X', 'B']]
        
        if len(o_indices) == 3 and len(blockers) == 1:
            for i in range(16):
                if board[i] == 'O' and i not in o_indices:
                    blocker_index = blockers[0]
                    # Perform the swap
                    board[i], board[blocker_index] = board[blocker_index], board[i]
                    return i, blocker_index
    return None


def minimax(brd, depth, is_maximizing, alpha, beta, max_depth=6):
    if is_winner(brd, 'O'):
        return 20 - depth
    if is_winner(brd, 'X'):
        return depth - 20
    if is_draw(brd) or depth >= max_depth:
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for move in get_available_moves(brd):
            brd[move] = 'O'
            eval = minimax(brd, depth + 1, False, alpha, beta)
            brd[move] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in get_available_moves(brd):
            brd[move] = 'X'
            eval = minimax(brd, depth + 1, True, alpha, beta)
            brd[move] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move():
    best_val = -math.inf
    move = None
    for i in get_available_moves(board):
        board[i] = 'O'
        move_val = minimax(board, 0, False, -math.inf, math.inf)
        board[i] = ' '
        if move_val > best_val:
            best_val = move_val
            move = i
    return move


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("4x4 Tic Tac Toe")
        self.buttons = []
        self.status = tk.Label(root, text="Your turn (X)", font=('Arial', 14))
        self.status.grid(row=5, column=0, columnspan=4, pady=10)

        self.block_mode = False
        self.player_swap_mode = False
        self.ai_swap_used = False
        self.swap_selection = []
        self.player_blocks_used = 0
        self.ai_blocks_used = 0
        self.player_swap_used = False

        # Block button
        self.block_button = tk.Button(root, text="Block (2 left)", command=self.toggle_block_mode)
        self.block_button.grid(row=6, column=0, columnspan=2, sticky='ew')

        # Swap button
        self.swap_button = tk.Button(root, text="Swap (1 left)", command=self.toggle_player_swap_mode)
        self.swap_button.grid(row=6, column=2, columnspan=2, sticky='ew')

        for i in range(16):
            button = tk.Button(root, text=' ', font=('Arial', 24), width=4, height=2,
                               command=lambda i=i: self.human_move(i))
            button.grid(row=i // 4, column=i % 4)
            self.buttons.append(button)

    def toggle_block_mode(self):
        if self.player_blocks_used >= 2:
            self.status.config(text="No blocks left!")
            return
        self.block_mode = not self.block_mode
        self.player_swap_mode = False
        self.status.config(text="Block Mode ON" if self.block_mode else "Your turn (X)")

    def toggle_player_swap_mode(self):
        if self.player_swap_used:
            self.status.config(text="Swap already used!")
            return
        self.player_swap_mode = not self.player_swap_mode
        self.block_mode = False
        self.swap_selection = []
        self.status.config(text="Swap Mode ON: Select 2" if self.player_swap_mode else "Your turn (X)")
        if self.player_swap_mode:
            for i in range(16):
                if self.buttons[i].cget("text") == ' ':
                    self.buttons[i].config(state='disabled')
                else:
                    self.buttons[i].config(state='normal')
        else:
            for i in range(16):
                    if self.buttons[i].cget("text") == ' ':
                        self.buttons[i].config(state='normal')
                    else:
                        self.buttons[i].config(state='disabled')


    def human_move(self, index):
        global board
        if board[index] != ' ' and not self.player_swap_mode:
            return

        if self.player_swap_mode:
            if index in self.swap_selection:
                return 
            self.swap_selection.append(index)
            self.buttons[index].config(relief='sunken') 

            if len(self.swap_selection) == 2:
                i, j = self.swap_selection
                board[i], board[j] = board[j], board[i]

                # Update button visuals
                self.buttons[i].config(text=board[i], state='disabled' if board[i] in ['X', 'O', 'B'] else 'normal', relief='raised')
                self.buttons[j].config(text=board[j], state='disabled' if board[j] in ['X', 'O', 'B'] else 'normal', relief='raised')

                self.player_swap_used = True
                self.player_swap_mode = False
                self.status.config(text="Swap done. AI's turn...")
                self.swap_button.config(state='disabled')
                for i in range(16):
                    if self.buttons[i].cget("text") == ' ':
                        self.buttons[i].config(state='normal')
                    else:
                        self.buttons[i].config(state='disabled')
                if is_winner(board, 'X'):
                    self.status.config(text="You win!")
                    self.disable_all()
                    return
                if is_draw(board):
                    self.status.config(text="It's a draw!")
                    return
                self.status.config(text="AI's turn...")
                self.root.after(500, self.ai_move)
            return


        if self.block_mode:
            board[index] = 'B'
            self.buttons[index].config(text='B', state='disabled')
            self.player_blocks_used += 1
            self.block_button.config(text=f"Block ({2 - self.player_blocks_used} left)")
            self.block_mode = False
            self.status.config(text="AI's turn...")
            self.root.after(500, self.ai_move)
            return

        board[index] = 'X'
        self.buttons[index].config(text='X', state='disabled')
        if is_winner(board, 'X'):
            self.status.config(text="You win!")
            self.disable_all()
            return
        if is_draw(board):
            self.status.config(text="It's a draw!")
            return
        self.status.config(text="AI's turn...")
        self.root.after(500, self.ai_move)

    def ai_move(self):
        if not self.ai_swap_used:
            swap_result = do_swap_move(board)
            if swap_result:
                i, j = swap_result
                self.buttons[i].config(text=board[i], state='disabled' if board[i] in ['O', 'X', 'B'] else 'normal')
                self.buttons[j].config(text=board[j], state='disabled' if board[j] in ['O', 'X', 'B'] else 'normal')
                self.ai_swap_used = True
                if is_winner(board, 'O'):
                    self.status.config(text="AI wins!")
                    self.disable_all()
                elif is_draw(board):
                    self.status.config(text="It's a draw!")
                else:
                    self.status.config(text="AI used swap! Your turn (X)")
                return

        block_index = do_block_move(board)
        if block_index is not None and self.ai_blocks_used < 2:
            board[block_index] = 'B'
            self.buttons[block_index].config(text='B', state='disabled')
            self.ai_blocks_used += 1
            self.status.config(text="AI placed a block. Your turn (X)")
            return
        
        move = best_move()
        if move is not None:
            board[move] = 'O'
            self.buttons[move].config(text='O', state='disabled')

        if is_winner(board, 'O'):
            self.status.config(text="AI wins!")
            self.disable_all()
        elif is_draw(board):
            self.status.config(text="It's a draw!")
        else:
            self.status.config(text="Your turn (X)")

    def disable_all(self):
        for btn in self.buttons:
            btn.config(state='disabled')

root = tk.Tk()
game = TicTacToeGUI(root)
root.mainloop()

