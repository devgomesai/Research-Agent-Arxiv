<div align="center">

# 🧠 Research Agent [arXiv]

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/ArXiv_logo_2022.svg/250px-ArXiv_logo_2022.svg.png" width="200" alt="arXiv Logo">
</p>

<i>Your AI-Powered Academic Research Companion</i>

<p align="center">
  <img src="https://camo.githubusercontent.com/a913e197b7f701a6d6223595d4b6dbc79e9cce66760f61ab148e33fce008c01d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d3337373641422e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d707974686f6e266c6f676f436f6c6f723d7768697465" alt="Python">
  <img src="https://camo.githubusercontent.com/423acdd0473cb26d7b172dbb9dd2fb70fcef81bbbd35efbfdc28b11d25fb038d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c616e67436861696e2d3143334333433f7374796c653d666f722d7468652d6261646765266c6f676f3d6c616e67636861696e266c6f676f436f6c6f723d7768697465" alt="LangChain">
  <img src="https://img.shields.io/badge/arXiv-2F2F2F.svg?style=for-the-badge&logo=arxiv&logoColor=red" alt="arXiv">
</p>

A sophisticated research agent that interfaces with arXiv to search, download, and analyze academic papers. Built with LangChain, this tool leverages MCP (Model Context Protocol) servers to provide seamless access to academic research.

</div>

## Features

- 🔍 **Intelligent Paper Search**: Find academic papers by topic, title, or keywords
- 📥 **Automated Downloads**: Download papers directly from arXiv with a single command
- 📄 **Full Paper Analysis**: Read and analyze complete paper content
- 🤖 **AI-Powered Assistance**: Leverages state-of-the-art LLMs for paper analysis
- 📊 **Rich CLI Interface**: Beautiful terminal interface with color-coded messages
- 🔄 **Interactive & Batch Modes**: Support for both interactive and single-query modes
- 📚 **Local Paper Management**: List and manage all locally downloaded papers
- ⚡ **Streamlined Workflow**: Automated search → download → read → analyze pipeline

## Prerequisites

- Python 3.12 or higher
- An API key from Anthropic (for Claude models) or other supported providers
- `uv` package manager (for MCP server management)

## Setup

### 1. Clone and Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd research-agent

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# Or if using uv: uv pip install -r requirements.txt
```

### 2. Create Your Configuration File

Create a `.env` file in the root directory with your API key:

```env
ANTHROPIC_API_KEY=your_api_key_here

```

### 3. Storage Path Configuration (Required)

**Important**: Before running the application, you must create a storage folder and reference its path in the `--storage-path` parameter.

1. Create a new folder that will store downloaded papers:
   ```bash
   mkdir /path/to/your/storage/folder
   # Example: mkdir ./arxiv_storage
   ```

2. Update the MCP server configuration in `src/mcp_server.py` to point to your storage folder:
   ```python
   # In src/mcp_server.py, modify the storage path:
   "--storage-path",
   "/path/to/your/storage/folder/",  # Update this path
   ```

## Dependencies

This project relies on the following key packages:

- `langchain`: Framework for developing LLM applications
- `langchain-mcp-adapters`: MCP server integration
- `langchain-anthropic`: Anthropic model integration
- `langgraph`: State management for agents
- `rich`: Rich text and beautiful formatting in the terminal
- `python-dotenv`: Environment variable management
- `arxiv-mcp-server`: Backend server for arXiv access

All dependencies are listed in `requirements.txt` and `pyproject.toml`.

## Usage

### Interactive Mode

Run the agent in interactive mode to have an ongoing conversation:

```bash
python -m src.agent
```

The agent will start in interactive mode where you can continuously ask questions about academic papers.

### Single Query Mode

Run a single query and exit:

```bash
python -m src.agent --query "Find papers on Vision Transformers"
```

### Using Different Models

Specify a different language model (default is Claude 3.5 Sonnet):

```bash
python -m src.agent --model anthropic:claude-3-5-sonnet-latest --query "Summarize recent advances in transformer architectures"
```

Other supported models include:
- `anthropic:claude-3-opus`
- And more depending on your configuration

### Additional Options

```bash
# Verbose output for debugging
python -m src.agent --verbose

# Limit number of tools displayed
python -m src.agent --tools-limit 3

# Show help
python -m src.agent --help
```

## Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   User Input    │───▶│ Research     │───▶│   arXiv MCP     │
│                 │    │ Agent        │    │   Server        │
│ (Queries)       │    │ (LangChain)  │    │ (Downloads &   │
└─────────────────┘    └──────────────┘    │  Searches)      │
                                          └─────────────────┘
                                                    │
                                                    ▼
                                          ┌─────────────────┐
                                          │  Storage Path   │
                                          │  (Local Papers) │
                                          └─────────────────┘
```

The system follows this workflow:
1. **Search**: User request triggers paper search on arXiv
2. **Download**: Relevant papers are downloaded to the configured storage path
3. **Read**: Paper content is retrieved from local storage
4. **Analyze**: AI model analyzes and responds to the user's query

## How It Works

The research agent uses the Model Context Protocol (MCP) to interface with the arXiv server. The `arxiv-mcp-server` provides the following tools:

- `search_papers`: Search arXiv for papers by topic, title, or keyword
- `download_paper`: Download a paper using its arXiv ID
- `read_paper`: Retrieve full content of a downloaded paper
- `list_papers`: List all locally downloaded papers

The agent follows a strict workflow:
1. Search for relevant papers based on user input
2. Download the most relevant paper
3. Read the paper content
4. Provide analysis based on user's specific request (summary, detailed analysis, comparison, etc.)

## Storage Management

All downloaded papers are stored in the directory specified by the `--storage-path` parameter in the MCP server configuration. The default location is `C:/arxiv_storage/`, but you should update this to a folder that exists on your system.

The application will automatically create and manage the storage directory, organizing papers by their arXiv IDs for efficient retrieval.

## Development

To modify the agent's behavior, you can update the prompt in `src/prompt.py`. The `PAPER_ANALYSIS_PROMPT` defines the agent's instructions and workflow for paper analysis.

## Troubleshooting

- **API Key Issues**: Ensure your API key is correctly set in the `.env` file
- **Storage Path Issues**: Verify the storage folder exists and has proper read/write permissions
- **Model Access**: Confirm your account has access to the requested language model
- **MCP Server**: Ensure the arXiv MCP server can be accessed through `uv` command
