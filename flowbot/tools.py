"""Tool definitions and implementations for FlowBot."""

import requests
import json
from typing import Any, Callable, Dict


def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo instant answer API.

    Args:
        query: Search query string

    Returns:
        The instant answer abstract or error message
    """
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json"}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Try to get useful content from the response
        if data.get("AbstractText"):
            return f"Search result for '{query}':\n{data['AbstractText']}"
        elif data.get("Definition"):
            return f"Definition: {data['Definition']}"
        elif data.get("Heading"):
            return f"Found: {data['Heading']}"
        else:
            return f"No detailed result found for '{query}'"
    except Exception as e:
        return f"Error searching: {str(e)}"


def read_file(path: str) -> str:
    """
    Read contents of a local file.

    Args:
        path: File path

    Returns:
        File contents as string
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found at {path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(path: str, content: str) -> str:
    """
    Write content to a local file.

    Args:
        path: File path
        content: Content to write

    Returns:
        Success or error message
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def run_python(code: str) -> str:
    """
    Execute Python code in a sandboxed namespace.

    Args:
        code: Python code to execute

    Returns:
        stdout output or error message
    """
    try:
        import sys
        from io import StringIO

        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        namespace = {
            "__builtins__": __builtins__,
            "json": json,
            "requests": requests,
        }

        exec(code, namespace)

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        return output if output else "(code executed, no output)"
    except Exception as e:
        sys.stdout = old_stdout
        return f"Error executing code: {str(e)}"


# Tool definitions for OpenAI function calling
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web using DuckDuckGo to find information about a topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a local file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The file path to read",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a local file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The file path to write to",
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_python",
            "description": "Execute Python code and return the output",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute",
                    }
                },
                "required": ["code"],
            },
        },
    },
]

# Mapping of tool names to functions
TOOL_MAP: Dict[str, Callable] = {
    "web_search": web_search,
    "read_file": read_file,
    "write_file": write_file,
    "run_python": run_python,
}
