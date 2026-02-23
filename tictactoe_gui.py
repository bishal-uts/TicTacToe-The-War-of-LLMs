"""
Tic-Tac-Toe GUI using Tkinter
A graphical user interface for the tic-tac-toe game
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
from typing import List, Optional
from ai_models import MinimaxAI, AggressiveAI, DefensiveAI, RandomAI, LimitedDepthAI, AIModel


class TicTacToeGUI:
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("Tic-Tac-Toe Game")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Game variables
        self.board: List[str] = [" " for _ in range(9)]
        self.current_player = "X"
        self.game_over = False
        self.game_started = False
        self.game_mode = None  # "human_vs_ai", "ai_vs_ai"
        
        # For human vs AI
        self.human = "X"
        self.ai = "O"
        self.ai_model = None
        
        # For AI vs AI
        self.ai_x_model = None
        self.ai_o_model = None
        
        # Available AI models
        self.ai_models_list = [
            MinimaxAI,
            AggressiveAI,
            DefensiveAI,
            LimitedDepthAI,
            RandomAI
        ]
        
        # Create GUI elements
        self.create_menu()
        self.create_info_frame()
        self.create_board_frame()
        
    def create_menu(self):
        """Create menu frame with game setup options"""
        menu_frame = ttk.LabelFrame(self.root, text="Game Mode", padding=10)
        menu_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(menu_frame, text="Select Game Mode:", font=("Arial", 11, "bold")).pack()
        
        # Human vs AI section
        human_ai_frame = ttk.LabelFrame(menu_frame, text="Human vs AI", padding=5)
        human_ai_frame.pack(pady=5, fill="x")
        
        ttk.Button(human_ai_frame, text="You First (X)", command=lambda: self.setup_human_vs_ai(True)).pack(side=tk.LEFT, padx=5)
        ttk.Button(human_ai_frame, text="AI First (O)", command=lambda: self.setup_human_vs_ai(False)).pack(side=tk.LEFT, padx=5)
        
        # AI vs AI section
        ai_ai_frame = ttk.LabelFrame(menu_frame, text="AI vs AI", padding=5)
        ai_ai_frame.pack(pady=5, fill="x")
        
        ttk.Button(ai_ai_frame, text="Select AI Models", command=self.select_ai_models).pack(padx=5)
    
    def create_info_frame(self):
        """Create info display frame"""
        info_frame = ttk.Frame(self.root)
        info_frame.pack(pady=10)
        
        self.status_var = tk.StringVar(value="Press a button to start the game")
        self.status_label = ttk.Label(info_frame, textvariable=self.status_var, font=("Arial", 11), foreground="blue")
        self.status_label.pack()
        
        button_frame = ttk.Frame(info_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="New Game", command=self.new_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Quit", command=self.quit_game).pack(side=tk.LEFT, padx=5)
    
    def create_board_frame(self):
        """Create the game board"""
        board_frame = ttk.Frame(self.root)
        board_frame.pack(pady=10)
        
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                board_frame,
                text="",
                font=("Arial", 24, "bold"),
                width=5,
                height=2,
                command=lambda pos=i: self.human_move(pos)
            )
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(btn)
    
    def setup_human_vs_ai(self, human_first: bool):
        """Setup human vs AI game"""
        self.game_mode = "human_vs_ai"
        self.ai_model = MinimaxAI("O")  # Default to expert AI
        self.current_player = "X" if human_first else "O"
        self.game_over = False
        self.game_started = True
        self.board = [" " for _ in range(9)]
        self.update_board_display()
        
        if human_first:
            self.status_var.set(f"Your turn (X). AI: {self.ai_model.get_name()}")
        else:
            self.status_var.set(f"AI's turn (O) - {self.ai_model.get_name()}. Please wait...")
            self.root.after(800, self.ai_move)
    
    def select_ai_models(self):
        """Open dialog to select AI models for AI vs AI match"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Select AI Models")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="AI vs AI Match", font=("Arial", 12, "bold")).pack(pady=10)
        
        # AI X selection
        ttk.Label(dialog, text="Player X (First):", font=("Arial", 10)).pack(anchor="w", padx=10)
        x_var = tk.StringVar(value=self.ai_models_list[0]("X").get_name())
        for model_class in self.ai_models_list:
            model = model_class("X")
            ttk.Radiobutton(dialog, text=model.get_name(), variable=x_var, 
                          value=model.get_name()).pack(anchor="w", padx=30)
        
        # AI O selection
        ttk.Label(dialog, text="Player O (Second):", font=("Arial", 10)).pack(anchor="w", padx=10, pady=(15, 0))
        o_var = tk.StringVar(value=self.ai_models_list[4]("O").get_name())  # Random by default
        for model_class in self.ai_models_list:
            model = model_class("O")
            ttk.Radiobutton(dialog, text=model.get_name(), variable=o_var,
                          value=model.get_name()).pack(anchor="w", padx=30)
        
        def start_ai_match():
            # Find the selected models
            x_name = x_var.get()
            o_name = o_var.get()
            
            for model_class in self.ai_models_list:
                if model_class("X").get_name() == x_name:
                    self.ai_x_model = model_class("X")
                if model_class("O").get_name() == o_name:
                    self.ai_o_model = model_class("O")
            
            dialog.destroy()
            self.start_ai_vs_ai_game()
        
        ttk.Button(dialog, text="Start Match", command=start_ai_match).pack(pady=15)
    
    def start_ai_vs_ai_game(self):
        """Start an AI vs AI match"""
        self.game_mode = "ai_vs_ai"
        self.current_player = "X"
        self.game_over = False
        self.game_started = True
        self.board = [" " for _ in range(9)]
        self.update_board_display()
        
        self.status_var.set(f"{self.ai_x_model.get_name()} (X) vs {self.ai_o_model.get_name()} (O)")
        self.root.after(1000, self.ai_vs_ai_move)
    
    def ai_vs_ai_move(self):
        """Execute move for AI vs AI match"""
        if self.game_over or not self.game_started or self.game_mode != "ai_vs_ai":
            return
        
        if self.current_player == "X":
            move = self.ai_x_model.get_move(self.board)
        else:
            move = self.ai_o_model.get_move(self.board)
        
        self.board[move] = self.current_player
        self.update_board_display()
        self.status_var.set(f"{self.current_player} played position {move + 1}")
        
        if self.check_winner(self.current_player):
            self.end_game(f"*** {self.current_player} ({self.ai_x_model.get_name() if self.current_player == 'X' else self.ai_o_model.get_name()}) Won! ***")
            return
        
        if self.is_board_full():
            self.end_game("*** It's a draw! ***")
            return
        
        self.current_player = "O" if self.current_player == "X" else "X"
        self.root.after(1500, self.ai_vs_ai_move)
    
    def start_game(self, human_first: bool):
        """Start a new game"""
        self.human_first = human_first
        self.current_player = self.human if human_first else self.ai
        self.game_over = False
        self.game_started = True
        self.board = [" " for _ in range(9)]
        self.update_board_display()
        
        if human_first:
            self.status_var.set("Your turn (X). Click a square to play.")
        else:
            self.status_var.set("AI's turn (O). Please wait...")
            self.root.after(500, self.ai_move)
    
    def update_board_display(self):
        """Update button display to match current board state"""
        for i, btn in enumerate(self.buttons):
            btn.config(text=self.board[i], state=tk.NORMAL)
            if self.board[i] == "X":
                btn.config(fg="blue", state=tk.DISABLED)
            elif self.board[i] == "O":
                btn.config(fg="red", state=tk.DISABLED)
            else:
                btn.config(fg="black")
    
    def human_move(self, position: int):
        """Handle human player move"""
        if not self.game_started or self.game_over or self.current_player != self.human:
            return
        
        if self.board[position] != " ":
            messagebox.showwarning("Invalid Move", "That position is already taken!")
            return
        
        self.board[position] = self.human
        self.update_board_display()
        
        if self.check_winner(self.human):
            self.end_game("*** You won! Congratulations! ***")
            return
        
        if self.is_board_full():
            self.end_game("*** It's a draw! ***")
            return
        
        self.current_player = self.ai
        self.status_var.set("AI's turn (O). Please wait...")
        self.root.after(800, self.ai_move)
    
    def ai_move(self):
        """Make AI move"""
        if self.game_over or not self.game_started or self.game_mode != "human_vs_ai":
            return
        
        move = self.ai_model.get_move(self.board)
        self.board[move] = "O"
        self.update_board_display()
        self.status_var.set(f"AI played position {move + 1}")
        
        if self.check_winner("O"):
            self.end_game("*** AI won! Better luck next time. ***")
            return
        
        if self.is_board_full():
            self.end_game("*** It's a draw! ***")
            return
        
        self.current_player = "X"
        self.status_var.set("Your turn (X). Click a square to play.")
    
    def get_available_moves(self) -> List[int]:
        """Get list of available positions"""
        return [i for i, spot in enumerate(self.board) if spot == " "]
    
    def check_winner(self, player: str) -> bool:
        """Check if player has won"""
        winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6],              # Diagonals
        ]
        for combo in winning_combos:
            if all(self.board[i] == player for i in combo):
                return True
        return False
    
    def is_board_full(self) -> bool:
        """Check if board is full"""
        return " " not in self.board
    
    def end_game(self, message: str):
        """End the game"""
        self.game_over = True
        self.status_var.set(message)
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
    
    def new_game(self):
        """Start a new game"""
        self.game_started = False
        self.game_over = False
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        
        for btn in self.buttons:
            btn.config(text="", state=tk.NORMAL, fg="black")
        
        self.status_var.set("Press a button to start the game")
    
    def quit_game(self):
        """Quit the game"""
        self.root.quit()


def main():
    """Main entry point"""
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
