"""
LLM-based AI Models for Tic-Tac-Toe
Integrates with various LLM providers: OpenAI, Anthropic, Google, Xai, etc.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
import json


class LLMModel(ABC):
    """Base class for LLM-based AI models"""
    
    def __init__(self, symbol: str, api_key: str = None):
        self.symbol = symbol
        self.api_key = api_key
        self.opponent_symbol = "O" if symbol == "X" else "X"
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this LLM model"""
        pass
    
    @abstractmethod
    def get_move(self, board: List[str]) -> int:
        """Get the AI's next move by querying the LLM"""
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Check if API key is configured"""
        pass
    
    def get_available_moves(self, board: List[str]) -> List[int]:
        """Get list of available positions"""
        return [i for i, spot in enumerate(board) if spot == " "]
    
    def format_board(self, board: List[str]) -> str:
        """Format board as readable string for LLM"""
        lines = []
        for i in range(3):
            row = board[i*3:(i+1)*3]
            display = [x if x != " " else str(i*3 + j + 1) for j, x in enumerate(row)]
            lines.append(f" {display[0]} | {display[1]} | {display[2]}")
            if i < 2:
                lines.append("---+---+---")
        return "\n".join(lines)
    
    def create_prompt(self, board: List[str]) -> str:
        """Create prompt for the LLM"""
        available_moves = self.get_available_moves(board)
        board_str = self.format_board(board)
        
        prompt = f"""You are playing Tic-Tac-Toe. You are {self.symbol}, your opponent is {self.opponent_symbol}.

Current board:
{board_str}

Available moves: {available_moves}

Return ONLY a single number (1-9) indicating your next move. Do not explain, just the number."""
        
        return prompt


class OpenAIModel(LLMModel):
    """OpenAI - Supports any model accessible via your API key"""
    
    def __init__(self, symbol: str, api_key: str = None, model: str = "gpt-4"):
        super().__init__(symbol, api_key)
        self.model = model
    
    def get_name(self) -> str:
        return f"OpenAI {self.model}"
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    def get_move(self, board: List[str]) -> int:
        """Get move from OpenAI API"""
        if not self.is_configured():
            raise ValueError("OpenAI API key not configured")
        
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = self.create_prompt(board)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Tic-Tac-Toe player. Respond with only a number 1-9."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=5
            )
            
            move_text = response.choices[0].message.content.strip()
            move = int(''.join(filter(str.isdigit, move_text)))
            
            # Validate move
            available = self.get_available_moves(board)
            if move - 1 not in available:
                return available[0] if available else 0
            
            return move - 1
            
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            available = self.get_available_moves(board)
            return available[0] if available else 0


class AnthropicModel(LLMModel):
    """Anthropic Claude"""
    
    def __init__(self, symbol: str, api_key: str = None, model: str = "claude-opus-4-6"):
        super().__init__(symbol, api_key)
        self.model = model
    
    def get_name(self) -> str:
        return f"Anthropic Claude"
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    def get_move(self, board: List[str]) -> int:
        """Get move from Anthropic API"""
        if not self.is_configured():
            raise ValueError("Anthropic API key not configured")
        
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            prompt = self.create_prompt(board)
            
            message = client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            move_text = message.content[0].text.strip()
            move = int(''.join(filter(str.isdigit, move_text)))
            
            # Validate move
            available = self.get_available_moves(board)
            if move - 1 not in available:
                return available[0] if available else 0
            
            return move - 1
            
        except Exception as e:
            print(f"Anthropic API Error: {e}")
            available = self.get_available_moves(board)
            return available[0] if available else 0


class GoogleModel(LLMModel):
    """Google Gemini"""
    
    def __init__(self, symbol: str, api_key: str = None, model: str = "gemini-2.0-flash"):
        super().__init__(symbol, api_key)
        self.model = model
    
    def get_name(self) -> str:
        return f"Google Gemini"
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    def get_move(self, board: List[str]) -> int:
        """Get move from Google Gemini API"""
        if not self.is_configured():
            raise ValueError("Google API key not configured")
        
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            prompt = self.create_prompt(board)
            
            response = model.generate_content(prompt)
            move_text = response.text.strip()
            move = int(''.join(filter(str.isdigit, move_text)))
            
            # Validate move
            available = self.get_available_moves(board)
            if move - 1 not in available:
                return available[0] if available else 0
            
            return move - 1
            
        except Exception as e:
            print(f"Google API Error: {e}")
            available = self.get_available_moves(board)
            return available[0] if available else 0


class GroqModel(LLMModel):
    """Groq LLaMA or Mixtral models (accessed via API)"""
    
    def __init__(self, symbol: str, api_key: str = None, model: str = "llama-3.3-70b-versatile"):
        super().__init__(symbol, api_key)
        self.model = model
    
    def get_name(self) -> str:
        return f"Groq {self.model.split('-')[0]}"
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    def get_move(self, board: List[str]) -> int:
        """Get move from Groq API"""
        if not self.is_configured():
            raise ValueError("Groq API key not configured")
        
        try:
            from groq import Groq
            
            client = Groq(api_key=self.api_key)
            prompt = self.create_prompt(board)
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.3,
                max_tokens=5,
            )
            
            move_text = chat_completion.choices[0].message.content.strip()
            move = int(''.join(filter(str.isdigit, move_text)))
            
            # Validate move
            available = self.get_available_moves(board)
            if move - 1 not in available:
                return available[0] if available else 0
            
            return move - 1
            
        except Exception as e:
            print(f"Groq API Error: {e}")
            available = self.get_available_moves(board)
            return available[0] if available else 0


class CohereModel(LLMModel):
    """Cohere API"""
    
    def __init__(self, symbol: str, api_key: str = None, model: str = "command"):
        super().__init__(symbol, api_key)
        self.model = model
    
    def get_name(self) -> str:
        return f"Cohere"
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    def get_move(self, board: List[str]) -> int:
        """Get move from Cohere API"""
        if not self.is_configured():
            raise ValueError("Cohere API key not configured")
        
        try:
            import cohere
            
            client = cohere.ClientV2(api_key=self.api_key)
            prompt = self.create_prompt(board)
            
            response = client.chat(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            move_text = response.message.content[0].text.strip()
            move = int(''.join(filter(str.isdigit, move_text)))
            
            # Validate move
            available = self.get_available_moves(board)
            if move - 1 not in available:
                return available[0] if available else 0
            
            return move - 1
            
        except Exception as e:
            print(f"Cohere API Error: {e}")
            available = self.get_available_moves(board)
            return available[0] if available else 0


class MistralModel(LLMModel):
    """Mistral AI API"""
    
    def __init__(self, symbol: str, api_key: str = None, model: str = "mistral-large-latest"):
        super().__init__(symbol, api_key)
        self.model = model
    
    def get_name(self) -> str:
        return f"Mistral"
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    def get_move(self, board: List[str]) -> int:
        """Get move from Mistral API"""
        if not self.is_configured():
            raise ValueError("Mistral API key not configured")
        
        try:
            from mistralai import Mistral
            
            client = Mistral(api_key=self.api_key)
            prompt = self.create_prompt(board)
            
            message = client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            move_text = message.choices[0].message.content.strip()
            move = int(''.join(filter(str.isdigit, move_text)))
            
            # Validate move
            available = self.get_available_moves(board)
            if move - 1 not in available:
                return available[0] if available else 0
            
            return move - 1
            
        except Exception as e:
            print(f"Mistral API Error: {e}")
            available = self.get_available_moves(board)
            return available[0] if available else 0


class XAIModel(LLMModel):
    """XAI Grok API"""
    
    def __init__(self, symbol: str, api_key: str = None, model: str = "grok-beta"):
        super().__init__(symbol, api_key)
        self.model = model
    
    def get_name(self) -> str:
        return f"XAI Grok"
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    def get_move(self, board: List[str]) -> int:
        """Get move from XAI Grok API"""
        if not self.is_configured():
            raise ValueError("XAI API key not configured")
        
        try:
            import openai
            
            # XAI Grok uses OpenAI-compatible API
            client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://api.x.ai/v1"
            )
            
            prompt = self.create_prompt(board)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Tic-Tac-Toe player. Respond with only a number 1-9."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=5
            )
            
            move_text = response.choices[0].message.content.strip()
            move = int(''.join(filter(str.isdigit, move_text)))
            
            # Validate move
            available = self.get_available_moves(board)
            if move - 1 not in available:
                return available[0] if available else 0
            
            return move - 1
            
        except Exception as e:
            print(f"XAI Grok API Error: {e}")
            available = self.get_available_moves(board)
            return available[0] if available else 0


# Registry of all available LLM models
LLM_PROVIDERS = {
    "OpenAI": {
        "class": OpenAIModel,
        "models": ["gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-3.5-turbo"],
        "url": "https://platform.openai.com/api-keys",
        "note": "Use any model your API key has access to"
    },
    "Anthropic": {
        "class": AnthropicModel,
        "models": ["claude-opus-4-6", "claude-sonnet-4-6", "claude-haiku-4-5-20251001"],
        "url": "https://console.anthropic.com/account/keys"
    },
    "Google Gemini": {
        "class": GoogleModel,
        "models": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
        "url": "https://aistudio.google.com/app/apikey"
    },
    "Groq": {
        "class": GroqModel,
        "models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        "url": "https://console.groq.com/keys"
    },
    "Cohere": {
        "class": CohereModel,
        "models": ["command"],
        "url": "https://dashboard.cohere.com/api-keys"
    },
    "Mistral": {
        "class": MistralModel,
        "models": ["mistral-large-latest", "mistral-medium-latest"],
        "url": "https://console.mistral.ai/api-keys/"
    },
    "XAI (Grok)": {
        "class": XAIModel,
        "models": ["grok-beta"],
        "url": "https://console.x.ai/"
    }
}
