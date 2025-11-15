import os
import json

# Import providers (only import if installed)
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import anthropic
except ImportError:
    anthropic = None


class AIClient:
    """
    A unified client to support multiple AI providers (OpenAI, Google, Anthropic).
    Provides a consistent chat() and complete() interface.
    """

    def __init__(self, provider: str, model: str, api_key: str = None):
        self.provider = provider.lower()
        self.model = model

        # Auto-detect API key
        if api_key is None:
            if self.provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
            elif self.provider == "google":
                api_key = os.getenv("GOOGLE_API_KEY")
            elif self.provider == "anthropic":
                api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError(f"API key for {self.provider} not provided or set in env vars.")

        # Initialize provider clients
        if self.provider == "openai":
            if OpenAI is None:
                raise ImportError("openai package not installed. Run `pip install openai`.")
            self.client = OpenAI(api_key=api_key)

        elif self.provider == "google":
            if genai is None:
                raise ImportError("google-generativeai package not installed. Run `pip install google-generativeai`.")
            genai.configure(api_key=api_key)
            self.client = genai

        elif self.provider == "anthropic":
            if anthropic is None:
                raise ImportError("anthropic package not installed. Run `pip install anthropic`.")
            self.client = anthropic.Anthropic(api_key=api_key)

        else:
            raise ValueError(f"Unknown provider: {provider}")


    def chat(self, messages, tools=None, tool_choice="auto"):
        """
        Unified chat interface across providers.
        Returns dict: { "content": str, "tool_calls": list }
        """
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice
            )
            msg = response.choices[0].message
            return {
                "content": msg.content,
                "tool_calls": msg.tool_calls or []
            }

        elif self.provider == "google":
            response = self.client.GenerativeModel(self.model).generate_content(
                messages[-1]["content"]
            )
            return {
                "content": response.text,
                "tool_calls": []
            }

        elif self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=messages
            )
            return {
                "content": response.content[0].text if response.content else "",
                "tool_calls": []
            }

        else:
            raise ValueError(f"Provider {self.provider} not supported.")


    def complete(self, prompt: str, max_tokens=500):
        """
        Simple text completion.
        """
        if self.provider == "openai":
            response = self.client.completions.create(
                model=self.model,
                prompt=prompt,
                max_tokens=max_tokens
            )
            return response.choices[0].text

        elif self.provider == "google":
            response = self.client.GenerativeModel(self.model).generate_content(prompt)
            return response.text

        elif self.provider == "anthropic":
            response = self.client.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                prompt=prompt
            )
            return response.completion

        else:
            raise ValueError(f"Provider {self.provider} not supported.")
