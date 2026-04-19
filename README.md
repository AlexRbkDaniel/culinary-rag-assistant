# Culinary RAG Assistant

An interactive CLI-based food recommendation system that combines semantic similarity search with conversational AI. Built with ChromaDB for vector storage, Sentence Transformers for embeddings, and the Anthropic Claude API for natural language responses.

## Scope

The project demonstrates three approaches to food discovery:

1. **Interactive Search** — conversational CLI that accepts free-text queries and returns semantically similar food items
2. **Advanced Search** — filtered search with support for cuisine type and calorie constraints, plus a demonstration mode
3. **RAG Chatbot** *(coming soon)* — retrieval-augmented generation using Claude to produce natural language recommendations from search results

## Project Structure

```
culinary-rag-assistant/
├── resources/
│   └── data/
│       └── FoodDataSet.json        # 185 food items with full nutritional metadata
├── src/
│   ├── cli/
│   │   ├── interactive_search.py   # Entry point: basic conversational search
│   │   ├── advanced_search.py      # Entry point: filtered search with menu
│   │   └── display.py              # Shared result formatting utilities
│   └── food_search/
│       └── similarity_manager.py   # FoodSimilarityManager — ChromaDB + embeddings
├── .env.example                    # Environment variable template
├── pyproject.toml                  # Package config and CLI entry points
└── requirements.txt                # Python dependencies
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd culinary-rag-assistant
```

### 2. Create and activate a virtual environment

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install the package in editable mode

This makes the `food_search` and `cli` packages importable from anywhere in the project:

```bash
pip install -e .
```

### 5. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Get your API key at [console.anthropic.com](https://console.anthropic.com).

## Running the Application

**Interactive Search:**
```bash
python -m cli.interactive_search
```

**Advanced Search with Filters:**
```bash
python -m cli.advanced_search
```

Or use the installed CLI entry points (after `pip install -e .`):
```bash
interactive-search
advanced-search
```

> On first run, the food database is embedded and cached locally in `.chroma/`. Subsequent runs load from cache and start instantly.