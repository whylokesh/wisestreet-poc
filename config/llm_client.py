# config/llm_client.py

from abc import ABC, abstractmethod
import json

# ---------- Base LLM Abstraction ----------
class BaseLLM(ABC):
    """
    Abstract base class for any LLM client.
    Handles generation + tool-calling structure.
    """

    @abstractmethod
    def chat(self, messages: list[dict], tools: list[dict] = None) -> dict:
        """
        Send messages to LLM.
        Returns dict with keys: { "content": str, "tool_calls": list }
        """
        pass


# ---------- OpenAI Implementation ----------
class OpenAILLM(BaseLLM):
    def __init__(self, client, model="gpt-4o-mini"):
        self.client = client
        self.model = model

    def chat(self, messages: list[dict], tools: list[dict] = None) -> dict:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto" if tools else None
        )

        message = resp.choices[0].message

        # Normalize response
        return {
            "content": message.get("content"),
            "tool_calls": message.get("tool_calls", [])
        }


# ---------- Google Gemini Implementation ----------
class GoogleLLM(BaseLLM):
    def __init__(self, client, model="gemini-1.5-flash"):
        self.client = client
        self.model = model

    def chat(self, messages: list[dict], tools: list[dict] = None) -> dict:
        # Convert OpenAI-style messages -> Gemini format
        chat_history = [
            {"role": m["role"], "parts": [m["content"]]} for m in messages
        ]

        resp = self.client.models.generate_content(
            model=self.model,
            contents=chat_history,
            tools=tools
        )

        # Gemini’s tool calls are embedded differently, normalize them
        tool_calls = []
        if resp.candidates:
            parts = resp.candidates[0].content.parts
            for part in parts:
                if "functionCall" in part:  # Gemini ADK style
                    tool_calls.append({
                        "name": part["functionCall"]["name"],
                        "arguments": part["functionCall"]["args"]
                    })

        return {
            "content": resp.candidates[0].content.parts[0].text
            if resp.candidates and resp.candidates[0].content.parts else "",
            "tool_calls": tool_calls
        }
