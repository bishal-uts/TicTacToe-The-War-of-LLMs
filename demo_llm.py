#!/usr/bin/env python
"""
Tic-Tac-Toe LLM Edition - Quick Demo
Shows how the LLM integration works
"""

from llm_models import LLM_PROVIDERS, LLMModel
from typing import List


def demo_llm_creation():
    """Demo: Create LLM instances"""
    print("\n" + "="*60)
    print("DEMO 1: Creating LLM Model Instances")
    print("="*60)
    
    for provider_name, provider_info in LLM_PROVIDERS.items():
        model_class = provider_info["class"]
        models = provider_info["models"]
        
        print(f"\n{provider_name}:")
        print(f"  Available models: {', '.join(models)}")
        
        # Create instance with dummy API key
        instance = model_class("X", api_key="dummy_key", 
                              model=models[0] if models else None)
        print(f"  Instance name: {instance.get_name()}")
        print(f"  Configured: {instance.is_configured()}")


def demo_board_formatting():
    """Demo: Board formatting"""
    print("\n" + "="*60)
    print("DEMO 2: Board Formatting for LLM")
    print("="*60)
    
    board = [" ", " ", " ", " ", "X", " ", " ", " ", " "]
    
    openai = LLM_PROVIDERS["OpenAI"]["class"]("X", "test_key")
    formatted = openai.format_board(board)
    
    print("\nBoard state:")
    print(formatted)
    print("\nThis is sent to the LLM to make a decision")


def demo_prompt_creation():
    """Demo: Prompt creation"""
    print("\n" + "="*60)
    print("DEMO 3: LLM Prompt Example")
    print("="*60)
    
    board = ["X", " ", " ", " ", "O", " ", " ", " ", " "]
    
    anthropic = LLM_PROVIDERS["Anthropic"]["class"]("O", "test_key")
    prompt = anthropic.create_prompt(board)
    
    print(prompt)


def demo_game_setup():
    """Demo: Setting up a game"""
    print("\n" + "="*60)
    print("DEMO 4: How to Set Up a Game")
    print("="*60)
    
    print("""
To play Human vs LLM:
  1. Run: python tictactoe_llm_gui.py
  2. API Configuration tab → paste your API key
  3. Human vs LLM tab → select provider and model
  4. Click "Start Game"
  5. Click squares to play
  
To watch LLM vs LLM:
  1. Run: python tictactoe_llm_gui.py
  2. API Configuration tab → paste API keys
  3. LLM vs LLM tab → select two different providers/models
  4. Click "Start Match"
  5. Watch them play!

Example Matchups:
  • GPT-4 vs Claude-3 Opus (Premium battle)
  • Groq vs Mistral (Budget-friendly, fast)
  • GPT-3.5 vs Claude-3 Haiku (Cost-effective)
  • Google Gemini vs Groq (Free/cheap options)
    """)


def demo_api_key_sources():
    """Demo: Where to get API keys"""
    print("\n" + "="*60)
    print("DEMO 5: Getting API Keys")
    print("="*60)
    
    print("\nFree or Low-Cost Options:")
    print("  • OpenAI: Free trial credit (~$5)")
    print("    → https://platform.openai.com/api-keys")
    print("  • Google Gemini: Free tier with limits")
    print("    → https://makersuite.google.com/app/apikey")
    print("  • Groq: Free tier available")
    print("    → https://console.groq.com/keys")
    
    print("\nPay-As-You-Go (Low cost):")
    print("  • Anthropic Claude: $0.003-0.015 per 1K tokens")
    print("    → https://console.anthropic.com/account/keys")
    print("  • Mistral: $0.0005-0.002 per 1K tokens")
    print("    → https://console.mistral.ai/api-keys/")
    print("  • Cohere: $0.0001 per 1K tokens")
    print("    → https://dashboard.cohere.com/api-keys")


def main():
    """Run all demos"""
    print("\n")
    print("=" * 60)
    print("Tic-Tac-Toe LLM Edition - Feature Demo")
    print("Watch or play against GPT-4, Claude, Gemini, etc!")
    print("=" * 60)
    
    try:
        demo_llm_creation()
        demo_board_formatting()
        demo_prompt_creation()
        demo_game_setup()
        demo_api_key_sources()
        
        print("\n" + "="*60)
        print("READY TO START!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Install SDK: pip install openai anthropic google-generativeai groq mistralai cohere")
        print("  2. Get API keys from providers above")
        print("  3. Run: python tictactoe_llm_gui.py")
        print("  4. Paste your API keys in Configuration tab")
        print("  5. Play or watch LLMs compete!")
        print()
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
