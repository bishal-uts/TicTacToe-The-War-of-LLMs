#!/usr/bin/env python
"""
Demo of AI vs AI matches in Tic-Tac-Toe
Shows how different AI models can compete against each other
"""

from ai_models import MinimaxAI, AggressiveAI, DefensiveAI, RandomAI, LimitedDepthAI


def play_ai_vs_ai(ai_x_class, ai_o_class, verbose=True):
    """
    Simulate a game between two AI models
    
    Args:
        ai_x_class: AI class for X player
        ai_o_class: AI class for O player
        verbose: Print game progress
    
    Returns:
        Winner ('X', 'O', or 'Draw')
    """
    board = [" "] * 9
    ai_x = ai_x_class("X")
    ai_o = ai_o_class("O")
    
    current_player = "X"
    move_count = 0
    max_moves = 9
    
    if verbose:
        print(f"\n{ai_x.get_name()} (X) vs {ai_o.get_name()} (O)")
        print("=" * 50)
    
    def print_board():
        if verbose:
            for i, row in enumerate([board[j*3:(j+1)*3] for j in range(3)]):
                print(f" {row[0]} | {row[1]} | {row[2]}")
                if i < 2:
                    print("-----------")
    
    def check_winner(player):
        winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6],
        ]
        return any(all(board[i] == player for i in combo) for combo in winning_combos)
    
    while move_count < max_moves:
        # Get AI move
        if current_player == "X":
            ai = ai_x
        else:
            ai = ai_o
        
        move = ai.get_move(board)
        board[move] = current_player
        
        if verbose:
            print(f"{current_player} plays position {move + 1}")
        
        # Check for winner
        if check_winner(current_player):
            if verbose:
                print_board()
                print(f"\n{ai.get_name()} ({current_player}) WINS!")
            return current_player
        
        # Check for draw
        move_count += 1
        if move_count == max_moves:
            if verbose:
                print_board()
                print("\nDRAW!")
            return "Draw"
        
        # Next player
        current_player = "O" if current_player == "X" else "X"
    
    return "Draw"


def main():
    """Run various AI matchups"""
    print("╔" + "=" * 60 + "╗")
    print("║      TIC-TAC-TOE AI vs AI MATCHUP DEMO                ║")
    print("╚" + "=" * 60 + "╝")
    
    ai_models = [
        ("Minimax (Expert)", MinimaxAI),
        ("Aggressive", AggressiveAI),
        ("Defensive", DefensiveAI),
        ("Limited (Intermediate)", LimitedDepthAI),
        ("Random (Beginner)", RandomAI),
    ]
    
    matchups = [
        (MinimaxAI, RandomAI),
        (AggressiveAI, DefensiveAI),
        (LimitedDepthAI, RandomAI),
        (MinimaxAI, AggressiveAI),
    ]
    
    print("\nRunning sample matchups...\n")
    
    for ai_x_class, ai_o_class in matchups:
        play_ai_vs_ai(ai_x_class, ai_o_class, verbose=True)
        print()
    
    print("=" * 60)
    print("To use AI vs AI in the GUI:")
    print("1. Run: python tictactoe_gui.py")
    print("2. Click 'Select AI Models'")
    print("3. Choose your two AI models")
    print("4. Click 'Start Match' and watch them play!")


if __name__ == "__main__":
    main()
