#!/usr/bin/env python
"""Quick test of AI models"""

try:
    from ai_models import MinimaxAI, AggressiveAI, DefensiveAI, RandomAI, LimitedDepthAI
    print("✓ All AI models imported successfully")
    
    # Test creating instances
    models = [
        MinimaxAI("X"),
        AggressiveAI("X"),
        DefensiveAI("X"),
        RandomAI("X"),
        LimitedDepthAI("X")
    ]
    
    for model in models:
        print(f"✓ {model.get_name()}")
    
    # Test a simple board
    board = [" "] * 9
    board[4] = "X"
    
    minimax = MinimaxAI("O")
    move = minimax.get_move(board)
    print(f"✓ MinimaxAI move: {move + 1}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
