"""
Tic-Tac-Toe AI Models
Different AI strategies for the game
"""

import random
from typing import List, Tuple
from abc import ABC, abstractmethod


class AIModel(ABC):
    """Base class for AI models"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.opponent_symbol = "O" if symbol == "X" else "X"
    
    @abstractmethod
    def get_move(self, board: List[str]) -> int:
        """Get the AI's next move"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this AI model"""
        pass
    
    def get_available_moves(self, board: List[str]) -> List[int]:
        """Get list of available positions"""
        return [i for i, spot in enumerate(board) if spot == " "]
    
    def check_winner(self, board: List[str], player: str) -> bool:
        """Check if player has won"""
        winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6],              # Diagonals
        ]
        for combo in winning_combos:
            if all(board[i] == player for i in combo):
                return True
        return False
    
    def is_board_full(self, board: List[str]) -> bool:
        """Check if board is full"""
        return " " not in board


class MinimaxAI(AIModel):
    """Standard minimax AI - unbeatable"""
    
    def get_name(self) -> str:
        return "Minimax AI (Expert)"
    
    def get_move(self, board: List[str]) -> int:
        """Get move using minimax algorithm"""
        best_score = -float("inf")
        best_moves = []
        
        for move in self.get_available_moves(board):
            board[move] = self.symbol
            score = self.minimax(board, 0, False)
            board[move] = " "
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        
        return random.choice(best_moves) if best_moves else random.choice(self.get_available_moves(board))
    
    def minimax(self, board: List[str], depth: int, is_maximizing: bool) -> int:
        """Minimax algorithm"""
        score = self.evaluate(board, depth)
        
        if score == 10 - depth:  # AI wins
            return score
        if score == depth - 10:  # Opponent wins
            return score
        if self.is_board_full(board):
            return 0
        
        if is_maximizing:
            best_score = -float("inf")
            for move in self.get_available_moves(board):
                board[move] = self.symbol
                score = self.minimax(board, depth + 1, False)
                board[move] = " "
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for move in self.get_available_moves(board):
                board[move] = self.opponent_symbol
                score = self.minimax(board, depth + 1, True)
                board[move] = " "
                best_score = min(score, best_score)
            return best_score
    
    def evaluate(self, board: List[str], depth: int) -> int:
        """Evaluate board state"""
        if self.check_winner(board, self.symbol):
            return 10 - depth
        if self.check_winner(board, self.opponent_symbol):
            return depth - 10
        return 0


class AggressiveAI(AIModel):
    """Aggressive AI - prioritizes winning"""
    
    def get_name(self) -> str:
        return "Aggressive AI"
    
    def get_move(self, board: List[str]) -> int:
        """Get move prioritizing winning moves"""
        available = self.get_available_moves(board)
        
        # First, try to win
        for move in available:
            board[move] = self.symbol
            if self.check_winner(board, self.symbol):
                board[move] = " "
                return move
            board[move] = " "
        
        # Second, block opponent from winning
        for move in available:
            board[move] = self.opponent_symbol
            if self.check_winner(board, self.opponent_symbol):
                board[move] = " "
                return move
            board[move] = " "
        
        # Third, take center if available
        if 4 in available:
            return 4
        
        # Fourth, take corners
        corners = [0, 2, 6, 8]
        corner_moves = [m for m in available if m in corners]
        if corner_moves:
            return random.choice(corner_moves)
        
        # Finally, take any available move
        return random.choice(available)


class DefensiveAI(AIModel):
    """Defensive AI - prioritizes blocking"""
    
    def get_name(self) -> str:
        return "Defensive AI"
    
    def get_move(self, board: List[str]) -> int:
        """Get move prioritizing blocking"""
        available = self.get_available_moves(board)
        
        # First, block opponent from winning
        for move in available:
            board[move] = self.opponent_symbol
            if self.check_winner(board, self.opponent_symbol):
                board[move] = " "
                return move
            board[move] = " "
        
        # Second, try to win if possible
        for move in available:
            board[move] = self.symbol
            if self.check_winner(board, self.symbol):
                board[move] = " "
                return move
            board[move] = " "
        
        # Third, take center if available
        if 4 in available:
            return 4
        
        # Finally, take any available move
        return random.choice(available)


class RandomAI(AIModel):
    """Random AI - plays randomly (for easy difficulty)"""
    
    def get_name(self) -> str:
        return "Random AI (Beginner)"
    
    def get_move(self, board: List[str]) -> int:
        """Get a random move"""
        available = self.get_available_moves(board)
        return random.choice(available) if available else -1


class LimitedDepthAI(AIModel):
    """Limited depth minimax - looks ahead only 2 moves"""
    
    def get_name(self) -> str:
        return "Limited AI (Intermediate)"
    
    def get_move(self, board: List[str]) -> int:
        """Get move using limited depth minimax"""
        best_score = -float("inf")
        best_moves = []
        max_depth = 4  # Only look 2 moves ahead
        
        for move in self.get_available_moves(board):
            board[move] = self.symbol
            score = self.minimax_limited(board, 0, False, max_depth)
            board[move] = " "
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        
        return random.choice(best_moves) if best_moves else random.choice(self.get_available_moves(board))
    
    def minimax_limited(self, board: List[str], depth: int, is_maximizing: bool, max_depth: int) -> int:
        """Limited depth minimax"""
        score = self.evaluate_limited(board)
        
        if score == 10:  # AI wins
            return score + (max_depth - depth)
        if score == -10:  # Opponent wins
            return score - (max_depth - depth)
        if self.is_board_full(board) or depth >= max_depth:
            return 0
        
        if is_maximizing:
            best_score = -float("inf")
            for move in self.get_available_moves(board):
                board[move] = self.symbol
                score = self.minimax_limited(board, depth + 1, False, max_depth)
                board[move] = " "
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for move in self.get_available_moves(board):
                board[move] = self.opponent_symbol
                score = self.minimax_limited(board, depth + 1, True, max_depth)
                board[move] = " "
                best_score = min(score, best_score)
            return best_score
    
    def evaluate_limited(self, board: List[str]) -> int:
        """Evaluate board state"""
        if self.check_winner(board, self.symbol):
            return 10
        if self.check_winner(board, self.opponent_symbol):
            return -10
        return 0
