"""
Tic-Tac-Toe GUI with LLM Support
Play against or watch LLM models compete
"""

import tkinter as tk
from tkinter import messagebox, ttk
import threading
from typing import List
from llm_models import LLM_PROVIDERS, LLMModel


class LLMTicTacToeGUI:
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("Tic-Tac-Toe - LLM Edition")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # Game state
        self.board: List[str] = [" "] * 9
        self.game_over = False
        self.game_started = False
        self.current_player = "X"
        
        # LLM state
        self.llm_x = None
        self.llm_o = None
        self.api_keys = {}
        
        # Create GUI
        self.create_widgets()
    
    def create_widgets(self):
        """Create main GUI elements"""
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: API Configuration
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="API Configuration")
        self.create_config_tab()
        
        # Tab 2: Human vs LLM
        self.human_vs_llm_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.human_vs_llm_frame, text="Human vs LLM")
        self.create_human_vs_llm_tab()
        
        # Tab 3: LLM vs LLM
        self.llm_vs_llm_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.llm_vs_llm_frame, text="LLM vs LLM")
        self.create_llm_vs_llm_tab()
    
    def create_config_tab(self):
        """Create API configuration tab"""
        ttk.Label(self.config_frame, text="Configure LLM API Keys", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Create scrollable frame
        canvas = tk.Canvas(self.config_frame)
        scrollbar = ttk.Scrollbar(self.config_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add providers
        self.key_entries = {}
        for provider_name, provider_info in LLM_PROVIDERS.items():
            self.create_provider_section(scrollable_frame, provider_name, provider_info)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Save button
        ttk.Button(self.config_frame, text="Save API Keys", 
                  command=self.save_api_keys).pack(pady=10)
    
    def create_provider_section(self, parent, provider_name, provider_info):
        """Create configuration section for a provider"""
        frame = ttk.LabelFrame(parent, text=provider_name, padding=10)
        frame.pack(fill="x", padx=5, pady=5)
        
        # API Key input
        ttk.Label(frame, text="API Key:").grid(row=0, column=0, sticky="w")
        entry = ttk.Entry(frame, width=50, show="*")
        entry.grid(row=0, column=1, padx=5)
        self.key_entries[provider_name] = entry
        
        # Models available
        models_text = f"Available models: {', '.join(provider_info['models'])}"
        ttk.Label(frame, text=models_text, font=("Arial", 9), 
                 foreground="gray").grid(row=1, column=0, columnspan=2, sticky="w")
        
        # Documentation link
        doc_link = f"Get API key: {provider_info['url']}"
        ttk.Label(frame, text=doc_link, font=("Arial", 9, "underline"), 
                 foreground="blue").grid(row=2, column=0, columnspan=2, sticky="w")
    
    def save_api_keys(self):
        """Save API keys from entries"""
        for provider_name, entry in self.key_entries.items():
            key = entry.get().strip()
            if key:
                self.api_keys[provider_name] = key
        
        if self.api_keys:
            messagebox.showinfo("Success", f"Saved {len(self.api_keys)} API key(s)")
        else:
            messagebox.showwarning("Warning", "No API keys configured")
    
    def create_human_vs_llm_tab(self):
        """Create Human vs LLM tab"""
        # Title
        ttk.Label(self.human_vs_llm_frame, text="Human vs LLM", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # LLM selection
        selection_frame = ttk.LabelFrame(self.human_vs_llm_frame, text="Select LLM Opponent", padding=10)
        selection_frame.pack(padx=10, pady=10, fill="x")
        
        # Provider selection
        ttk.Label(selection_frame, text="Provider:").pack(anchor="w")
        self.hvl_provider_var = tk.StringVar()
        self.hvl_provider_combo = ttk.Combobox(selection_frame, textvariable=self.hvl_provider_var, 
                                              values=list(LLM_PROVIDERS.keys()), state="readonly")
        self.hvl_provider_combo.pack(fill="x", pady=5)
        self.hvl_provider_combo.bind("<<ComboboxSelected>>", self.update_hvl_models)
        
        # Model selection
        ttk.Label(selection_frame, text="Model:").pack(anchor="w")
        self.hvl_model_var = tk.StringVar()
        self.hvl_model_combo = ttk.Combobox(selection_frame, textvariable=self.hvl_model_var)
        self.hvl_model_combo.pack(fill="x", pady=5)
        
        # Start button
        ttk.Button(selection_frame, text="Start Game", 
                  command=self.start_human_vs_llm).pack(pady=10)
        
        # Game board
        self.hvl_board_frame = ttk.Frame(self.human_vs_llm_frame)
        self.hvl_board_frame.pack(pady=10)
        
        self.hvl_buttons = []
        for i in range(9):
            btn = tk.Button(self.hvl_board_frame, text="", font=("Arial", 16, "bold"),
                           width=5, height=2, command=lambda pos=i: self.human_move(pos))
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.hvl_buttons.append(btn)
        
        # Status
        self.hvl_status_var = tk.StringVar(value="Configure API keys and select a model")
        ttk.Label(self.human_vs_llm_frame, textvariable=self.hvl_status_var,
                 font=("Arial", 11)).pack(pady=10)
        
        # Buttons
        button_frame = ttk.Frame(self.human_vs_llm_frame)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="New Game", command=self.new_game_hvl).pack(side=tk.LEFT, padx=5)
    
    def create_llm_vs_llm_tab(self):
        """Create LLM vs LLM tab"""
        ttk.Label(self.llm_vs_llm_frame, text="LLM vs LLM Match", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # LLM selection
        selection_frame = ttk.LabelFrame(self.llm_vs_llm_frame, text="Select LLM Competitors", padding=10)
        selection_frame.pack(padx=10, pady=10, fill="x")
        
        # Player X
        ttk.Label(selection_frame, text="Player X (First):", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(selection_frame, text="Provider:").pack(anchor="w")
        self.llm_x_provider_var = tk.StringVar()
        self.llm_x_provider_combo = ttk.Combobox(selection_frame, textvariable=self.llm_x_provider_var,
                                                values=list(LLM_PROVIDERS.keys()), state="readonly")
        self.llm_x_provider_combo.pack(fill="x", pady=5)
        self.llm_x_provider_combo.bind("<<ComboboxSelected>>", self.update_llm_x_models)
        
        ttk.Label(selection_frame, text="Model:").pack(anchor="w")
        self.llm_x_model_var = tk.StringVar()
        self.llm_x_model_combo = ttk.Combobox(selection_frame, textvariable=self.llm_x_model_var)
        self.llm_x_model_combo.pack(fill="x", pady=5)
        
        ttk.Separator(selection_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Player O
        ttk.Label(selection_frame, text="Player O (Second):", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(selection_frame, text="Provider:").pack(anchor="w")
        self.llm_o_provider_var = tk.StringVar()
        self.llm_o_provider_combo = ttk.Combobox(selection_frame, textvariable=self.llm_o_provider_var,
                                                values=list(LLM_PROVIDERS.keys()), state="readonly")
        self.llm_o_provider_combo.pack(fill="x", pady=5)
        self.llm_o_provider_combo.bind("<<ComboboxSelected>>", self.update_llm_o_models)
        
        ttk.Label(selection_frame, text="Model:").pack(anchor="w")
        self.llm_o_model_var = tk.StringVar()
        self.llm_o_model_combo = ttk.Combobox(selection_frame, textvariable=self.llm_o_model_var)
        self.llm_o_model_combo.pack(fill="x", pady=5)
        
        # Start button
        ttk.Button(selection_frame, text="Start Match", 
                  command=self.start_llm_vs_llm).pack(pady=15)
        
        # Game board
        self.lvl_board_frame = ttk.Frame(self.llm_vs_llm_frame)
        self.lvl_board_frame.pack(pady=10)
        
        self.lvl_buttons = []
        for i in range(9):
            btn = tk.Button(self.lvl_board_frame, text="", font=("Arial", 16, "bold"),
                           width=5, height=2, state=tk.DISABLED)
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.lvl_buttons.append(btn)
        
        # Status
        self.lvl_status_var = tk.StringVar(value="Select two LLM models and click 'Start Match'")
        ttk.Label(self.llm_vs_llm_frame, textvariable=self.lvl_status_var,
                 font=("Arial", 11)).pack(pady=10)
        
        # Buttons
        button_frame = ttk.Frame(self.llm_vs_llm_frame)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="New Match", command=self.new_game_lvl).pack(side=tk.LEFT, padx=5)
    
    def update_hvl_models(self, event=None):
        """Update available models for Human vs LLM"""
        provider = self.hvl_provider_var.get()
        if provider in LLM_PROVIDERS:
            models = LLM_PROVIDERS[provider]["models"]
            self.hvl_model_combo["values"] = models
            if models:
                self.hvl_model_combo.current(0)
    
    def update_llm_x_models(self, event=None):
        """Update available models for LLM X"""
        provider = self.llm_x_provider_var.get()
        if provider in LLM_PROVIDERS:
            models = LLM_PROVIDERS[provider]["models"]
            self.llm_x_model_combo["values"] = models
            if models:
                self.llm_x_model_combo.current(0)
    
    def update_llm_o_models(self, event=None):
        """Update available models for LLM O"""
        provider = self.llm_o_provider_var.get()
        if provider in LLM_PROVIDERS:
            models = LLM_PROVIDERS[provider]["models"]
            self.llm_o_model_combo["values"] = models
            if models:
                self.llm_o_model_combo.current(0)
    
    def start_human_vs_llm(self):
        """Start Human vs LLM game"""
        provider = self.hvl_provider_var.get()
        model_name = self.hvl_model_var.get()
        
        if not provider or not model_name:
            messagebox.showwarning("Error", "Please select a provider and model")
            return
        
        if provider not in self.api_keys:
            messagebox.showerror("Error", f"API key not configured for {provider}")
            return
        
        # Create LLM instance
        model_class = LLM_PROVIDERS[provider]["class"]
        self.llm_o = model_class("O", self.api_keys[provider], model_name)
        
        # Reset game
        self.board = [" "] * 9
        self.game_over = False
        self.game_started = True
        self.current_player = "X"
        
        self.update_hvl_display()
        self.hvl_status_var.set("Your turn (X). Click a square to play.")
    
    def start_llm_vs_llm(self):
        """Start LLM vs LLM match"""
        x_provider = self.llm_x_provider_var.get()
        x_model = self.llm_x_model_var.get()
        o_provider = self.llm_o_provider_var.get()
        o_model = self.llm_o_model_var.get()
        
        if not all([x_provider, x_model, o_provider, o_model]):
            messagebox.showwarning("Error", "Please select providers and models for both players")
            return
        
        if x_provider not in self.api_keys:
            messagebox.showerror("Error", f"API key not configured for {x_provider}")
            return
        if o_provider not in self.api_keys:
            messagebox.showerror("Error", f"API key not configured for {o_provider}")
            return
        
        # Create LLM instances
        x_class = LLM_PROVIDERS[x_provider]["class"]
        o_class = LLM_PROVIDERS[o_provider]["class"]
        
        self.llm_x = x_class("X", self.api_keys[x_provider], x_model)
        self.llm_o = o_class("O", self.api_keys[o_provider], o_model)
        
        # Reset game
        self.board = [" "] * 9
        self.game_over = False
        self.game_started = True
        self.current_player = "X"
        
        self.update_lvl_display()
        self.lvl_status_var.set(f"{self.llm_x.get_name()} (X) vs {self.llm_o.get_name()} (O)")
        
        # Start playing
        self.root.after(1000, self.llm_vs_llm_play)
    
    def human_move(self, position: int):
        """Handle human move in Human vs LLM"""
        if not self.game_started or self.game_over or self.current_player != "X":
            return
        
        if self.board[position] != " ":
            messagebox.showwarning("Invalid", "Position already taken")
            return
        
        self.board[position] = "X"
        self.update_hvl_display()
        
        if self.check_winner("X"):
            self.end_game_hvl("You won!")
            return
        
        if self.is_board_full():
            self.end_game_hvl("It's a draw!")
            return
        
        self.current_player = "O"
        self.hvl_status_var.set("AI is thinking...")
        self.root.after(1000, self.llm_move_hvl)
    
    def llm_move_hvl(self):
        """LLM move in Human vs LLM"""
        try:
            move = self.llm_o.get_move(self.board)
            self.board[move] = "O"
            self.update_hvl_display()
            
            if self.check_winner("O"):
                self.end_game_hvl("AI won!")
                return
            
            if self.is_board_full():
                self.end_game_hvl("It's a draw!")
                return
            
            self.current_player = "X"
            self.hvl_status_var.set("Your turn (X)")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to get LLM move: {str(e)}")
            self.hvl_status_var.set("Error communicating with LLM")
    
    def llm_vs_llm_play(self):
        """Execute LLM vs LLM game"""
        if self.game_over or not self.game_started:
            return
        
        try:
            if self.current_player == "X":
                move = self.llm_x.get_move(self.board)
            else:
                move = self.llm_o.get_move(self.board)
            
            self.board[move] = self.current_player
            self.update_lvl_display()
            self.lvl_status_var.set(f"{self.current_player} played position {move + 1}")
            
            if self.check_winner(self.current_player):
                winner_name = self.llm_x.get_name() if self.current_player == "X" else self.llm_o.get_name()
                self.end_game_lvl(f"{winner_name} ({self.current_player}) won!")
                return
            
            if self.is_board_full():
                self.end_game_lvl("It's a draw!")
                return
            
            self.current_player = "O" if self.current_player == "X" else "X"
            self.root.after(1500, self.llm_vs_llm_play)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to get LLM move: {str(e)}")
            self.end_game_lvl("Match ended due to API error")
    
    def check_winner(self, player: str) -> bool:
        """Check if player won"""
        combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6],
        ]
        return any(all(self.board[i] == player for i in combo) for combo in combos)
    
    def is_board_full(self) -> bool:
        """Check if board is full"""
        return " " not in self.board
    
    def update_hvl_display(self):
        """Update Human vs LLM board display"""
        for i, btn in enumerate(self.hvl_buttons):
            btn.config(text=self.board[i])
            if self.board[i] != " ":
                btn.config(state=tk.DISABLED, fg="red" if self.board[i] == "O" else "blue")
            else:
                btn.config(state=tk.NORMAL, fg="black")
    
    def update_lvl_display(self):
        """Update LLM vs LLM board display"""
        for i, btn in enumerate(self.lvl_buttons):
            btn.config(text=self.board[i], fg="red" if self.board[i] == "O" else "blue")
    
    def end_game_hvl(self, message: str):
        """End Human vs LLM game"""
        self.game_over = True
        self.hvl_status_var.set(message)
        for btn in self.hvl_buttons:
            btn.config(state=tk.DISABLED)
    
    def end_game_lvl(self, message: str):
        """End LLM vs LLM match"""
        self.game_over = True
        self.lvl_status_var.set(message)
    
    def new_game_hvl(self):
        """New Human vs LLM game"""
        self.board = [" "] * 9
        self.game_over = False
        self.game_started = False
        self.current_player = "X"
        self.update_hvl_display()
        self.hvl_status_var.set("Select a model and start a new game")
        for btn in self.hvl_buttons:
            btn.config(state=tk.NORMAL)
    
    def new_game_lvl(self):
        """New LLM vs LLM match"""
        self.board = [" "] * 9
        self.game_over = False
        self.game_started = False
        self.current_player = "X"
        self.update_lvl_display()
        self.lvl_status_var.set("Select models and start a new match")


def main():
    """Main entry point"""
    root = tk.Tk()
    gui = LLMTicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
