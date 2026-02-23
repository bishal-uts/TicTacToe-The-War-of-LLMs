<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview

This is a basic tic-tac-toe game implemented in Python. The game allows a human player to compete against an AI opponent that uses the minimax algorithm for optimal play.

## Technology Stack

- **Language**: Python 3.6+
- **Algorithm**: Minimax for AI decision-making
- **Interface**: Console-based

## Game Features

- Interactive console interface
- AI opponent with unbeatable strategy
- Board position reference display
- Replay functionality

## How to Run

```bash
python tictactoe.py
```

## File Structure

- `tictactoe.py` - Main game implementation with TicTacToe class
- `README.md` - User documentation and instructions

## Development Notes

- The AI uses minimax algorithm to evaluate game states
- The game board is represented as a list of 9 elements (positions 0-8)
- Player symbols: X (human) and O (AI)
- The game continues until there's a winner or the board is full
