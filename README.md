# Multi-Agent AI RPA Project

An innovative Robotic Process Automation (RPA) system that uses multiple AI agents to automate web form filling and interactions. Built with LangGraph, this project demonstrates how multiple specialized AI agents can work together to understand and automate web tasks. 

Also has a visual front-end similar to langgraph studio but open source, this will be made available when in a release worthy stage in a separate repo to enable all developer using langgraph to have an opensource front-end built in React, TypeScript, and Vite.

## 🌟 Core Features

- **Intelligent Form Field Detection**: AI-powered detection of form fields and their purposes
- **Natural Language Task Description**: Describe form-filling tasks in plain English
- **Multi-Agent Collaboration**: Specialized agents working together:
  - Element Selector Agent: Identifies the correct form fields
  - Action Writer Agent: Generates precise automation steps
  - Flow Manager: Coordinates the automation workflow
- **Interactive Flow Visualization**: Real-time visualization of agent interactions using React Flow
- **Modern Web Interface**: Built with React, TypeScript, and Vite

## 🏗️ Technical Architecture

### Backend System (LangGraph)
- **State Graph Architecture**: Manages the flow between different agents
- **Specialized Agents**:
  1. **Element Selector**: Uses DOM analysis to identify form fields
  2. **Action Writer**: Generates automation steps
  3. **Flow Manager**: Coordinates the overall process
- **Playwright Integration**: Handles web automation execution

### Frontend Application (React + TypeScript)
- **Modern Tech Stack**:
  - React 19 with TypeScript
  - Vite for fast development and building
  - React Query for efficient data fetching
  - XY Flow (React Flow) for graph visualization
  - ELK.js for automatic graph layouts
- **Key Components**:
  - Interactive agent workflow visualization
  - Real-time state updates
  - Automatic layout algorithms for complex graphs
  - Custom styled nodes and edges

### Test Environment (Django)
- Sample form application for testing automation scenarios
- API endpoints for testing agent interactions

## 🚀 Getting Started

### Prerequisites
- Python 3.11+ (Backend)
- Node.js 18+ (Frontend)
- Poetry for Python dependency management
- Chrome/Chromium browser

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YassinCh/multi-agent-ai-rpa.git
cd multi-agent-ai-rpa
```

2. Install frontend dependencies:
```bash
cd web
npm install
```

3. Install backend dependencies:
```bash
cd ..
poetry install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Configure your environment variables:
# - LLM API keys
# - Backend settings
```

5. Start the development servers:

Frontend:
```bash
cd web
npm run dev
```

Backend:
```bash
poetry run langgraph api serve
```

Test Forms (Optional):
```bash
cd api
poetry run python manage.py runserver
```

## 📖 Project Structure

```
multi-agent-ai-rpa/
├── web/                   # React frontend application
│   ├── src/              # Frontend source code
│   │   ├── components/   # React components
│   │   ├── App.tsx      # Main application
│   │   └── styles/      # CSS and styling
├── src/                  # Core RPA implementation
│   ├── agents/          # AI agent implementations
│   │   ├── element_selector/  # Form field detection
│   │   └── write_action_lines/# Action generation
│   ├── browser/         # Browser automation
│   ├── nodes/           # LangGraph node implementations
│   └── rpa_graph.py     # Main agent workflow definition
├── api/                  # Django test environment
└── reference_material/   # Development references
```

## 🛠️ Key Components

1. **RPA Graph** (`src/rpa_graph.py`):
   - Defines the workflow between agents
   - Manages state transitions
   - Coordinates agent communication
   - Uses Langgraph

2. **Frontend Visualization** (`web/src/`):
   - Interactive graph visualization using React Flow
   - Real-time agent state monitoring
   - Automatic layout management with ELK.js
   - Custom styled nodes and edges

3. **Element Selector** (`src/agents/element_selector/`):
   - Analyzes DOM structure
   - Identifies relevant form fields
   - Maps user requirements to form elements

4. **Action Writer** (`src/agents/write_action_lines/`):
   - Generates automation steps
   - Creates executable browser commands
   - Handles error cases

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the Modified MIT License - see the [LICENSE](LICENSE) file for details. You can freely use, modify, and distribute this software, and incorporate it into your products. However, you cannot sell this software as a standalone product without significant modifications or additions.

## 🙏 Acknowledgments

- Built with [React](https://reactjs.org/) and [TypeScript](https://www.typescriptlang.org/)
- Uses [XY Flow](https://reactflow.dev/) for graph visualization
- [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration
- [Playwright](https://playwright.dev/) for browser automation
- [ELK.js](https://www.eclipse.org/elk/) for graph layouts
- Special thanks to the open-source community for all referenced code and resources used in this project