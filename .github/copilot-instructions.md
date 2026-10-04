# RAG project instructions

The full project conventions live in [CLAUDE.md](../CLAUDE.md) at the repo root; read it first. It is the single source of truth for code style, logging, error handling, testing, project structure and git workflow. The build order is in [roadmap.md](../roadmap.md).

Summary of the essentials:

- Follow the existing project structure and conventions.
- Keep changes focused on the requested behavior; work one roadmap checkbox at a time.
- Every module uses `logging.getLogger(__name__)` and wraps external calls at their boundary (catch, log, degrade gracefully).
- Every change ships with tests; mock all external services.
- Before committing, run `ruff format .`, `ruff check .`, `mypy .` and `pytest` (all must pass; 90% coverage required).
- Never commit secrets, `.env`, raw corpus data or the vector store.
