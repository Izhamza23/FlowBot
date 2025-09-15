"""FlowBot main entry point."""

import sys
import os
from dotenv import load_dotenv
from flowbot.agent import Agent
from flowbot.tools import TOOL_DEFINITIONS


def main():
    """Run FlowBot with a user-provided goal."""
    # Load environment variables
    load_dotenv()

    # Get goal from command line or prompt user
    if len(sys.argv) > 1:
        goal = " ".join(sys.argv[1:])
    else:
        print("FlowBot - AI Automation Agent")
        print("=" * 40)
        goal = input("Enter your goal: ").strip()

        if not goal:
            print("No goal provided. Exiting.")
            return

    # Create and run agent
    agent = Agent(tools=TOOL_DEFINITIONS)
    result = agent.run(goal)
    print("\nAgent finished.")
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
