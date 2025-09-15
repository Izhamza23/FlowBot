"""Main FlowBot agent implementation."""

from typing import Optional, Any
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from flowbot.llm import LLMClient
from flowbot.tools import TOOL_DEFINITIONS, TOOL_MAP
from flowbot import config


class Agent:
    """AI automation agent that executes multi-step workflows."""

    def __init__(self, tools: Optional[list] = None, system_prompt: Optional[str] = None):
        """
        Initialize the agent.

        Args:
            tools: List of tool definitions (uses defaults if not provided)
            system_prompt: System prompt for the agent
        """
        self.llm_client = LLMClient()
        self.tools = tools or TOOL_DEFINITIONS
        self.system_prompt = system_prompt or config.SYSTEM_PROMPT
        self.console = Console()
        self.iteration_count = 0

    def run(self, goal: str) -> str:
        """
        Execute a multi-step workflow to achieve a goal.

        Args:
            goal: The user's goal or task

        Returns:
            Final result or completion message
        """
        self.iteration_count = 0
        self.console.print(
            Panel(f"[bold blue]Goal:[/bold blue] {goal}", title="FlowBot Agent")
        )

        messages = [{"role": "user", "content": goal}]
        system_message = {"role": "system", "content": self.system_prompt}

        while self.iteration_count < config.MAX_ITERATIONS:
            self.iteration_count += 1
            self.console.print(f"\n[yellow]Iteration {self.iteration_count}[/yellow]")

            # Call LLM with tools
            response = self.llm_client.chat(
                [system_message] + messages,
                tools=self.tools,
                temperature=config.TEMPERATURE,
            )

            # Add assistant response to message history
            messages.append({"role": "assistant", "content": response.content})

            # Print reasoning if available
            if response.content:
                self.console.print(f"[cyan]Reasoning:[/cyan] {response.content}")

            # Check if we have tool calls to execute
            if not hasattr(response, "tool_calls") or not response.tool_calls:
                # No more tool calls, we have a final answer
                self.console.print(
                    Panel(
                        response.content or "Task completed",
                        title="[green]Final Result[/green]",
                    )
                )
                return response.content or "Task completed successfully"

            # Process each tool call
            for tool_call in response.tool_calls:
                tool_name = tool_call.function.name
                tool_args = tool_call.function.arguments

                # Parse arguments if they're a string
                if isinstance(tool_args, str):
                    import json
                    tool_args = json.loads(tool_args)

                self.console.print(f"\n[magenta]→ Calling {tool_name}[/magenta]")
                self.console.print(f"  Args: {tool_args}")

                # Execute the tool
                if tool_name in TOOL_MAP:
                    result = TOOL_MAP[tool_name](**tool_args)
                    self.console.print(f"  Result: {result[:200]}...")

                    # Add tool result to messages
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_name,
                            "content": str(result),
                        }
                    )
                else:
                    error_msg = f"Tool {tool_name} not found"
                    self.console.print(f"  [red]Error:[/red] {error_msg}")
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_name,
                            "content": error_msg,
                        }
                    )

        # Max iterations reached
        self.console.print(
            Panel(
                f"[red]Max iterations ({config.MAX_ITERATIONS}) reached[/red]",
                title="Incomplete",
            )
        )
        return "Goal not completed within iteration limit"
