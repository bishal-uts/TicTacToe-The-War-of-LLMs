"""
Setup guide for LLM-based Tic-Tac-Toe
Instructions for configuring different LLM API providers
"""

LLM_SETUP_GUIDE = """
╔════════════════════════════════════════════════════════════════╗
║       LLM-Based Tic-Tac-Toe Setup Guide                        ║
║       Watch different AI models compete or play against them!  ║
╚════════════════════════════════════════════════════════════════╝

QUICK START
===========
1. Run: python tictactoe_llm_gui.py
2. Go to "API Configuration" tab
3. Add API keys for your desired LLM providers
4. Click "Save API Keys"
5. Choose your game mode and start playing!


SUPPORTED LLM PROVIDERS
=======================

1. OpenAI (GPT-4, GPT-3.5 Turbo, and more)
   ├─ Get API Key: https://platform.openai.com/api-keys
   ├─ Models: gpt-4, gpt-4-turbo, gpt-4o, gpt-3.5-turbo, and ANY model your API key has access to
   ├─ Cost: ~$0.01-0.10 per game
   └─ Setup: Just paste your API key in the configuration tab

2. Anthropic (Claude)
   ├─ Get API Key: https://console.anthropic.com/account/keys
   ├─ Models: claude-opus-4-6, claude-sonnet-4-6, claude-haiku-4-5-20251001
   ├─ Cost: ~$0.01-0.05 per game
   └─ Setup: Just paste your API key in the configuration tab

3. Google Gemini
   ├─ Get API Key: https://aistudio.google.com/app/apikey
   ├─ Models: gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash
   ├─ Note: Has a free tier with rate limits
   └─ Setup: Just paste your API key in the configuration tab

4. Groq (Fast LLM processor)
   ├─ Get API Key: https://console.groq.com/keys
   ├─ Models: llama-3.3-70b-versatile, llama-3.1-8b-instant, mixtral-8x7b-32768
   ├─ Cost: Very fast and affordable
   └─ Setup: Just paste your API key in the configuration tab

5. Mistral AI
   ├─ Get API Key: https://console.mistral.ai/api-keys/
   ├─ Models: mistral-large, mistral-medium
   ├─ Cost: Competitive pricing
   └─ Setup: Just paste your API key in the configuration tab

6. Cohere
   ├─ Get API Key: https://dashboard.cohere.com/api-keys
   ├─ Models: command, command-light
   ├─ Cost: Affordable
   └─ Setup: Just paste your API key in the configuration tab

7. XAI (Grok) [NEW!]
   ├─ Get API Key: https://console.x.ai/
   ├─ Models: grok-beta
   ├─ Cost: ~$0.002 per game (very affordable)
   ├─ Speed: Very fast inference
   └─ Setup: Just paste your API key in the configuration tab


INSTALL REQUIRED LIBRARIES
============================

For each provider you want to use, install its SDK:

# OpenAI (GPT-4, GPT-3.5, and XAI Grok)
pip install openai

# Anthropic (Claude)
pip install anthropic

# Google Gemini
pip install google-generativeai

# Groq
pip install groq

# Mistral
pip install mistralai

# Cohere
pip install cohere

# Or install all at once:
pip install openai anthropic google-generativeai groq mistralai cohere


USAGE EXAMPLES
==============

Example 1: Watch GPT-4 vs Claude
  1. Configure OpenAI and Anthropic API keys
  2. Open LLM GUI: python tictactoe_llm_gui.py
  3. Go to "LLM vs LLM" tab
  4. Player X: Select "OpenAI" → "gpt-4"
  5. Player O: Select "Anthropic" → "claude-3-opus-20240229"
  6. Click "Start Match"
  7. Watch them play!

Example 2: Play against Gemini
  1. Configure Google Gemini API key
  2. Open LLM GUI: python tictactoe_llm_gui.py
  3. Go to "Human vs LLM" tab
  4. Select "Google Gemini" → "gemini-pro"
  5. Click "Start Game"
  6. Click a square to make your move
  7. Gemini will respond!

Example 3: Budget-friendly match (Groq vs Mistral)
  1. Configure Groq and Mistral API keys
  2. Open LLM GUI
  3. Go to "LLM vs LLM" tab
  4. Player X: "Groq" → "mixtral-8x7b-32768"
  5. Player O: "Mistral" → "mistral-large"
  6. Watch the match!


COST ESTIMATE
=============

Approximate cost per game (9 moves total):

OpenAI:
  - GPT-4: $0.05-0.10 per game
  - GPT-3.5: $0.005-0.01 per game

Anthropic:
  - Claude-3 Opus: $0.03-0.06 per game
  - Claude-3 Sonnet: $0.006-0.012 per game

Google Gemini:
  - Free tier has limits
  - Paid: ~$0.005 per game

Groq:
  - Very affordable (~$0.001 per game)
  - Some free tier available

Mistral:
  - ~$0.004 per game

Cohere:
  - ~$0.001 per game


TROUBLESHOOTING
===============

1. "ModuleNotFoundError: No module named 'openai'"
   → Install the SDK: pip install openai

2. "Anthropic API key not found"
   → Check that you saved the key in API Configuration tab

3. "Rate limit exceeded"
   → You're making too many API calls too quickly
   → Wait a few minutes before trying again
   → Some providers have free tier limits

4. "Invalid API key"
   → Check that you copied the key correctly
   → Make sure you're using the right provider's key
   → Ensure the key hasn't been invalidated

5. "LLM returned invalid move"
   → The model returned something other than 1-9
   → This is handled automatically (fallback to valid move)
   → Try a different model or provider

6. "Connection timeout"
   → Check your internet connection
   → The API service might be temporarily down
   → Try again in a few moments


TIPS FOR BEST RESULTS
=====================

1. Model Selection:
   - Stronger models (GPT-4, Claude-3 Opus) play slightly better
   - But Tic-Tac-Toe is solved, so all perform similarly
   - Mix different models for interesting matches!

2. Cost Optimization:
   - Use cheaper models (GPT-3.5, Claude-3 Haiku, Groq)
   - Groq and Cohere offer best value
   - Google Gemini has good free tier

3. Speed:
   - Groq is the fastest provider
   - OpenAI and Anthropic are slightly slower
   - Turn delays in GUI give API time to respond

4. Variety:
   - Create tournaments between different providers
   - Each LLM has slightly different playing style
   - Watch how they handle strategy


ADVANCED: CUSTOM MODELS
========================

You can add support for new providers by:

1. Create a new class in llm_models.py:
   ```python
   class MyProviderModel(LLMModel):
       def get_name(self) -> str:
           return "My Provider"
       
       def is_configured(self) -> bool:
           return bool(self.api_key)
       
       def get_move(self, board: List[str]) -> int:
           # Your API implementation here
           prompt = self.create_prompt(board)
           # Call your API and parse response
           move = parse_response(api_response)
           return move
   ```

2. Add to LLM_PROVIDERS registry:
   ```python
   LLM_PROVIDERS["My Provider"] = {
       "class": MyProviderModel,
       "models": ["model-1", "model-2"],
       "url": "https://your-api-docs.com"
   }
   ```

3. Restart the GUI and your provider will appear in dropdowns!
"""

if __name__ == "__main__":
    print(LLM_SETUP_GUIDE)
