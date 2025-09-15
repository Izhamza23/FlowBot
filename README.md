# FlowBot

A Python-based AI automation agent that interprets natural language instructions and executes multi-step workflows across web services autonomously.

## What It Does

FlowBot takes a plain-English description of a task and figures out the steps needed to complete it — calling APIs, parsing responses, and chaining actions together without needing explicit step-by-step instructions from the user. Think of it as a personal assistant you can script with plain text.

## Tech Stack

- **Python** — core runtime
- **OpenAI API / LLM APIs** — natural language understanding and step planning
- **Requests** — HTTP calls to external services
- **dotenv** — environment and API key management

## Features

- Natural language task parsing via LLM prompt engineering
- Modular pipeline: each "action" is a self-contained function that can be chained
- Supports web service calls (REST APIs), text parsing, and conditional branching
- Configurable via a simple YAML task definition file
- Basic logging to track execution steps and catch failures

## Project Structure

```
flowbot/
├── main.py              # Entry point
├── agent.py             # Core agent loop and task planner
├── actions/
│   ├── api_call.py      # Generic REST API action
│   ├── parse.py         # LLM output parsing utilities
│   └── notify.py        # Output/notification actions
├── config/
│   └── tasks.yaml       # Example task definitions
├── .env.example
└── requirements.txt
```

## Getting Started

```bash
git clone https://github.com/Izhamza23/FlowBot.git
cd FlowBot
pip install -r requirements.txt
cp .env.example .env  # add your API keys
python main.py
```

## Status

🚧 Work in progress — currently supports single-chain workflows, multi-branch conditional logic in development.
