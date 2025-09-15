"""LLM client for OpenAI API."""

import os
from typing import Optional, Any
from openai import OpenAI


class LLMClient:
    """Wrapper around OpenAI client for chat completions."""

    def __init__(self):
        """Initialize OpenAI client from environment variables."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)

    def chat(
        self,
        messages: list[dict[str, str]],
        tools: Optional[list[dict[str, Any]]] = None,
        temperature: float = 0.7,
    ) -> Any:
        """
        Call OpenAI chat completions API.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions in OpenAI function format
            temperature: Sampling temperature

        Returns:
            The response message object
        """
        kwargs = {
            "model": "gpt-4o",
            "messages": messages,
            "temperature": temperature,
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message
