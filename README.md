# Robot Research Team 🤖

An autonomous multi-agent research pipeline. Four AI agents — a Planner, Researcher, Critic, and Writer — collaborate without human intervention to produce a complete research report on any topic.

## How it works

1. **Planner** breaks the topic into 3-5 focused sub-questions
2. **Researcher** answers each sub-question
3. **Critic** reviews the research for gaps and can send it back for another pass
4. **Writer** compiles everything into a polished final report

## Tech Stack

- **LangGraph** — orchestrates the multi-agent workflow
- **FastAPI** — serves the pipeline as a live-streaming API
- **Google Gemini API** — powers each agent's reasoning
- **Vanilla HTML/CSS/JS** — animated frontend with live agent status

## Running locally

1. Clone this repo
2. Create a virtual environment and install dependencies:
