# Tic-Tac-Toe Game

A Python-based tic-tac-toe game with multiple interfaces and AI opponents. Features simple heuristic AI models, a GUI version with classical algorithms, **AND** the ability to integrate real LLM models (GPT-4, Claude, Gemini, Groq, etc.) for competition.

## 🎮 Game Modes

- **Human vs Local AI** - Play against rule-based AI (Minimax, Aggressive, Defensive, etc.)
- **Human vs LLM** - Play against real LLM models (GPT-4, Claude, Gemini, etc.)
- **Local AI vs Local AI** - Watch rule-based AI models compete
- **LLM vs LLM** - Watch different LLM providers compete against each other!
- **Console Mode** - Classic text-based gameplay

## 🎯 Features

### Local AI Models
- **Minimax AI (Expert)** - Unbeatable using game tree analysis
- **Aggressive AI** - Prioritizes winning moves
- **Defensive AI** - Prioritizes blocking
- **Limited AI (Intermediate)** - Shallow game tree analysis
- **Random AI (Beginner)** - Random moves

### LLM Integration (NEW!)
Support for the best LLMs in the industry:
- **OpenAI** - GPT-4, GPT-4 Turbo, GPT-3.5 Turbo, and any model your API key has access to
- **Anthropic** - Claude Opus 4, Sonnet 4, Haiku
- **Google** - Gemini 2.0 Flash, Gemini 1.5 Pro
- **Groq** - LLaMA 3.3 70B, Mixtral 8x7B
- **Mistral** - Mistral Large, Mistral Medium
- **Cohere** - Command
- **XAI** - Grok (via x.ai API)

**Just add your API keys and start playing!**

## 🚀 Quick Start

### Play Against Local AI
```bash
python tictactoe_gui.py
```
Click "You First" or "AI First" to play against rule-based AI.

### Play Against LLM Models
```bash
python tictactoe_llm_gui.py
```
1. Go to "API Configuration" tab
2. Add your LLM API keys (OpenAI, Claude, Gemini, etc.)
3. Click "Save API Keys"
4. Go to "Human vs LLM" or "LLM vs LLM" tab
5. Select your models and start playing!

### Console Version
```bash
python tictactoe.py
```
Text-based game with simple AI opponent.

## Requirements

- Python 3.8 or higher
- No external dependencies for console and local AI modes
- For LLM support, install provider SDKs (optional):
  ```bash
  pip install openai anthropic google-generativeai groq mistralai cohere
  ```

## Installation

### 1. Clone/Download the project
```bash
cd TicTacToe
```

### 2. (Optional) Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Install dependencies for LLM support (optional)
```bash
# Install all LLM provider SDKs
pip install openai anthropic google-generativeai groq mistralai cohere

# Or install individually as needed:
pip install openai  # For GPT-4, GPT-3.5, XAI Grok
pip install anthropic  # For Claude
pip install google-generativeai  # For Gemini
pip install groq  # For Groq
pip install mistralai  # For Mistral
pip install cohere  # For Cohere
```

### 4. Get API Keys (for LLM support)
Visit each provider's console to get free API keys:
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/account/keys
- **Google**: https://aistudio.google.com/app/apikey
- **Groq**: https://console.groq.com/keys
- **Mistral**: https://console.mistral.ai/api-keys/
- **Cohere**: https://dashboard.cohere.com/api-keys
- **XAI**: https://console.x.ai/

## How to Run

### Local AI GUI (No API Keys Needed)
```bash
python tictactoe_gui.py
```
Features:
- Play against local AI models
- Watch local AI models compete
- No subscription or API keys required
- Instant gameplay

### LLM GUI (Requires API Keys)
```bash
python tictactoe_llm_gui.py
```
Features:
- Play against real LLM models (GPT-4, Claude, Gemini, etc.)
- Watch different LLMs compete against each other
- Supports 6 major LLM providers
- Easy API key management

**Setup:**
1. Click "API Configuration" tab
2. Paste your API keys from OpenAI, Anthropic, Google, Groq, Mistral, Cohere, or XAI
3. Click "Save API Keys"
4. Choose game mode and start!

### Console Version
```bash
python tictactoe.py
```
Features:
- Classic text-based gameplay
- Simple AI opponent
- Choose who goes first
- Quit mid-game option

## Detailed Setup for LLM Mode

See [LLM_SETUP_GUIDE.py](LLM_SETUP_GUIDE.py) for:
- Step-by-step provider setup
- Cost estimates for each provider
- Code examples
- Troubleshooting guide
- How to add new providers

Quick reference:
```bash
python LLM_SETUP_GUIDE.py  # Display full setup guide
```

## How to Play

### General Gameplay
- You play as **X**, the AI plays as **O** (in Human vs AI mode)
- Get three in a row to win
- Board positions are numbered 1-9:
  ```
  1 | 2 | 3
  ---------
  4 | 5 | 6
  ---------
  7 | 8 | 9
  ```

### GUI Mode
- Click any empty square to place your mark
- AI automatically responds
- Status shows current turn and game state

### Console Mode
- Enter a number from 1-9 when prompted
- Type 'q' then confirm to quit mid-game
- Answer yes/no to play again

## Project Structure

```
TicTacToe/
├── tictactoe.py              # Console version
├── tictactoe_gui.py          # Local AI GUI
├── tictactoe_llm_gui.py      # LLM GUI ✨ NEW!
├── ai_models.py              # Local AI strategies
├── llm_models.py             # LLM integrations ✨ NEW!
├── demo_ai_vs_ai.py          # Demo local AI matches
├── LLM_SETUP_GUIDE.py        # Detailed LLM setup guide ✨ NEW!
└── README.md                 # This file
```

## 💡 Example Matchups

### GPT-4 vs Claude
Watch different ways of thinking compete. Both are highly capable.

### Groq vs Mistral (Budget-friendly)
Both are affordable and fast. Great for multiple matches.

### Local AI: Minimax vs Random
See how a perfect-playing AI destroys a random player.

### Aggressive vs Defensive
Watch how different strategies play against each other.

## 🎓 Educational Value

Learn about:
- AI algorithms (Minimax, game trees)
- Different LLM reasoning patterns
- API integration
- Game theory basics
- Python GUI development

## 📊 Cost & Performance

| Provider | Per Game | Speed | Quality |
|----------|----------|-------|---------|
| Groq | ~$0.001 | Very Fast | Good |
| Cohere | ~$0.001 | Fast | Good |
| XAI (Grok) | ~$0.002 | Very Fast | Very Good |
| Mistral | ~$0.004 | Fast | Very Good |
| GPT-3.5 | ~$0.008 | Moderate | Very Good |
| Claude-3 Haiku | ~$0.008 | Moderate | Very Good |
| Gemini | Free/Cheap | Moderate | Very Good |
| Claude-3 Sonnet | ~$0.03 | Moderate | Excellent |
| GPT-4 | ~$0.08 | Slower | Excellent |

## 🛠️ Advanced: Custom LLM Providers

Add any LLM provider by:

1. Create a class in `llm_models.py` inheriting from `LLMModel`
2. Implement `get_name()`, `is_configured()`, and `get_move()`
3. Register in `LLM_PROVIDERS` dict
4. Restart GUI - it appears in dropdowns!

See `llm_models.py` for examples with OpenAI, Anthropic, Google, Groq, Mistral, Cohere, and XAI.

## 📝 License

This is an educational tic-tac-toe game. Free to use and modify!

---

**For detailed LLM setup: `python LLM_SETUP_GUIDE.py`**
