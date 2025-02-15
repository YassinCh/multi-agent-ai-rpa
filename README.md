# Multi-Agent AI RPA Project

A Django + LangGraph project that implements an AI-powered RPA system.

## Project Structure
```
## Key Components

1. **agents/** - Contains all LangGraph agent implementations
   - Separated by agent type (reasoner, worker, etc.)
   - Each agent has its own prompts and implementation

2. **core/** - Shared functionality used across both Django and LangGraph
   - Environment configuration
   - Shared utilities and helpers

3. **web/** - Django web application
   - REST API for agent communication
   - Frontend interface
   - Django project configuration

4. **tests/** - Organized test suite
   - Separate directories for agent and web tests
   - Shared test configuration

## Development Setup

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run Django development server:
```bash
poetry run python web/manage.py runserver
```

4. Run LangGraph API server:
```bash
poetry run langgraph api serve