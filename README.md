# Prompt Versioning System (Llama 3.1:8B)

**"Git + MLflow for Prompts"** — A complete **LLMOps** project for versioning, executing, evaluating, and A/B testing AI prompts using **Llama 3.1 8B** locally via Ollama.

## ✨ Features
- Full prompt template versioning
- Execution history with latency tracking
- Manual evaluations
- A/B testing between prompt versions
- FastAPI + PostgreSQL + Docker
- Local LLM (Llama 3.1:8B via Ollama)

## 🚀 Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.com/) → Run: `ollama pull llama3.1:8b`

### Run the project
```bash
cd prompt-versioning-system
docker-compose up --build
