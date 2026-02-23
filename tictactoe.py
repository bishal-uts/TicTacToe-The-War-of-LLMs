"""
Tic-Tac-Toe Game
A simple console-based tic-tac-toe game where you play against the computer.
"""

import random
from typing import List, Tuple


class TicTacToe:
    def __init__(self, human_first: bool = True):
        """Initialize the game board and set up players.
        
        Args:
            human_first: If True, human plays first. If False, AI plays first.
        """
        self.board: List[str] = [" " for _ in range(9)]
        self.human = "X"
        self.ai = "O"
        self.current_player = self.human if human_first else self.ai

    def print_board(self) -> None:
        """Display the current state of the board."""
        print("\n")
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")
        print()

    def print_board_nums(self) -> None:
        """Display the board with position numbers for reference."""
        print("\nPosition numbers:")
        number_board = [str(i) for i in range(1, 10)]
        for row in [number_board[i*3:(i+1)*3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")
        print()

    def get_available_moves(self) -> List[int]:
        """Return list of available positions (0-8)."""
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def is_winner(self, player: str) -> bool:
        """Check if the specified player has won."""
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
        """Check if the board is completely filled."""
        return " " not in self.board

    def evaluate(self, depth: int = 0) -> int:
        """
        Evaluate the board state for minimax algorithm.
        Returns: 10 if AI wins, -10 if human wins, 0 if draw/ongoing.
        """
        if self.is_winner(self.ai):
            return 10 - depth
        if self.is_winner(self.human):
            return depth - 10
        if self.is_board_full():
            return 0
        return 0

    def minimax(self, depth: int = 0, is_maximizing: bool = True) -> int:
        """Minimax algorithm to find the best move for AI."""
        score = self.evaluate(depth)

        if score == 10 - depth:
            return score
        if score == depth - 10:
            return score
        if self.is_board_full():
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for move in self.get_available_moves():
                self.board[move] = self.ai
                score = self.minimax(depth + 1, False)
                self.board[move] = " "
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for move in self.get_available_moves():
                self.board[move] = self.human
                score = self.minimax(depth + 1, True)
                self.board[move] = " "
                best_score = min(score, best_score)
            return best_score

    def get_best_move(self) -> int:
        """Find the best move for AI using minimax algorithm.
        When multiple moves have equal score, picks randomly to vary gameplay.
        """
        best_score = -float("inf")
        best_moves = []  # List to store all moves with best score
        
        for move in self.get_available_moves():
            self.board[move] = self.ai
            score = self.minimax(0, False)
            self.board[move] = " "
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        
        # If multiple moves have the same best score, pick randomly
        if best_moves:
            return random.choice(best_moves)
        else:
            return random.choice(self.get_available_moves())

    def human_move(self) -> bool:
        """Get and validate human player's move.
        
        Returns:
            True if move was made successfully, False if player wants to quit.
        """
        while True:
            try:
                user_input = input("Enter your move (1-9) or 'q' to quit: ").strip().lower()
                
                # Check for quit command
                if user_input in ["q", "quit"]:
                    confirm = input("Are you sure you want to quit? (yes/no): ").strip().lower()
                    if confirm in ["yes", "y"]:
                        return False
                    continue
                
                move = int(user_input) - 1
                if move < 0 or move > 8:
                    print("Please enter a number between 1 and 9.")
                    continue
                if self.board[move] != " ":
                    print("That position is already taken!")
                    continue
                self.board[move] = self.human
                return True
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9, or 'q' to quit.")

    def ai_move(self) -> None:
        """Make AI's move using minimax algorithm."""
        move = self.get_best_move()
        self.board[move] = self.ai
        print(f"AI plays position {move + 1}")

    def play(self) -> None:
        """Main game loop."""
        print("=" * 40)
        print("Welcome to Tic-Tac-Toe!")
        print("You are X, AI is O")
        print("=" * 40)
        
        if self.current_player == self.human:
            print("You go first!")
        else:
            print("AI goes first!")
        print()

        self.print_board_nums()

        while True:
            self.print_board()

            # Human move
            if self.current_player == self.human:
                if not self.human_move():
                    self.print_board()
                    print("\n[QUIT] Game terminated by player. Thanks for playing!")
                    return
                if self.is_winner(self.human):
                    self.print_board()
                    print("*** You won! Congratulations! ***")
                    break
                self.current_player = self.ai
            # AI move
            else:
                self.ai_move()
                if self.is_winner(self.ai):
                    self.print_board()
                    print("*** AI won! Better luck next time. ***")
                    break
                self.current_player = self.human

            if self.is_board_full():
                self.print_board()
                print("*** It's a draw! ***")
                break


def main() -> None:
    """Entry point for the game."""
    while True:
        # Ask who should go first
        print("\n" + "=" * 40)
        print("Who should go first?")
        print("1. You (Human)")
        print("2. AI")
        print("=" * 40)
        
        while True:
            choice = input("Enter your choice (1 or 2): ").strip()
            if choice in ["1", "2"]:
                human_first = choice == "1"
                break
            print("Invalid choice. Please enter 1 or 2.")
        
        game = TicTacToe(human_first=human_first)
        game.play()

        play_again = input("\nDo you want to play again? (yes/no): ").lower().strip()
        if play_again not in ["yes", "y"]:
            print("Thanks for playing! Goodbye!")
            break


if __name__ == "__main__":
    main()
