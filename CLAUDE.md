# CLAUDE.md

## Project overview

A RAG (retrieval-augmented generation) Q&A system over a real, messy document set: ingest, chunk, embed, retrieve (hybrid), and generate grounded, cited answers with Claude, plus an `/eval` harness that measures retrieval and answer quality. The document domain is not chosen yet (roadmap Section 2); `README.md` is still the template until then. The project is meant to be reviewed by potential employers, so quality, tests, and documentation matter as much as features.

`roadmap.md` is the build order and the source of truth for progress. Follow it in order.

## Tech stack

- Language: Python 3.13
- Key libraries: `anthropic` (generation), `sentence-transformers` (local embeddings), `chromadb` (vector store), `rank-bm25` (keyword retrieval), `streamlit` (UI). Add each one in the roadmap section that needs it, not before.
- Package manager: pip + venv (`venv/`, activate with `.\venv\Scripts\Activate.ps1`)

## Code style

- Formatter: ruff format, run before every commit
- Linter: ruff check (`ruff.toml`), clean; any suppression gets a comment explaining why
- Type checking: mypy strict (`mypy.ini`); every function has type hints
- Naming: snake_case for functions and variables; one clear job per module
- Logging: every module gets `logger = logging.getLogger(__name__)` and logs through it, never `print` (the CLI's user-facing output is the only exception). Format and handler setup live only in `src/logging_config.py`, and `configure_logging()` is called once, at the entry point, never in library modules. Never log secrets: log exception types and status codes where a library's exception message could embed a key or URL.
- Error handling: every external or risky call (network, disk, model, vector store, file parsing) is wrapped at its boundary. Catch the specific exception, log it via the module's logger (`exc_info=True` unless it could leak a secret), and degrade gracefully (skip the item, return a safe default that is distinguishable from a real result, such as a `failed` flag) rather than crashing the caller. Raise project exceptions from `src/errors.py` for conditions the caller must handle. Do this as part of writing the module, not afterward.
- Configuration: all settings come from `src/config.py` (environment and `.env`); no magic constants or hard-coded paths scattered in modules.
- Prompts: live in `/prompts` as versioned files, not inline in code.
- Docstrings: module docstring on every module explaining its role and any non-obvious decision; comments explain why, not what.

## Testing expectations

- Framework: pytest, with pytest-cov enforcing 90% coverage of `src/` (`pytest.ini`)
- Every new function or module ships with tests in the same commit; don't mark a roadmap item done without them
- Test failure paths as thoroughly as success paths: timeouts, malformed model output, corrupt files, empty results, missing config
- Mock all external calls (Anthropic, network); the test suite never hits a real API and never needs a key
- Use temporary directories or in-memory stores, never the real vector store or corpus
- Run the full suite before considering any change done

## Before finishing any task, run

```bash
ruff format .
ruff check .
mypy .
pytest
```

All four must pass before reporting a task complete. The same checks, plus a `detect-secrets` scan, run automatically as a pre-commit hook (`.pre-commit-config.yaml`; one-time `pre-commit install` per clone; commit with the venv active) and in CI (`.github/workflows/ci.yml`). Before pushing a section that changes dependencies, run `pip-audit -r requirements.txt` (needs network). If the secret scan flags a false positive, add `# pragma: allowlist secret` on the line rather than editing the baseline by hand.

## Project structure

```
/src        application code (config, logging_config, errors, then one module per pipeline stage)
/tests      pytest suite, one test file per module
/eval       evaluation harness, question set, results
/prompts    versioned prompt templates
/docs       corpus notes and architecture decision records
roadmap.md  build order and progress
```

- Keep each stage (load, chunk, embed, retrieve, generate) an independently callable function with clear inputs and outputs. `src/pipeline.py` is the only place that chains them.
- Service-specific code stays in one file: Anthropic only in the generation module, Chroma only in the store module.

## Git conventions

- Commit messages: imperative mood ("Add hybrid retrieval"), with the attribution trailer
- Each roadmap checkbox is a checkpoint: when it is done and the gate passes, tick the box in `roadmap.md` and commit. Commit the code and its tests together.
- Push at the end of every numbered roadmap section
- Never commit `.env`, API keys, raw corpus data, or the vector store; confirm `.gitignore` covers them
- Whenever a package is installed, run `pip freeze > requirements.txt` and commit it with the code that needs it
- Never skip hooks (`--no-verify`)
- When a roadmap item would apply to other projects, add it to `C:\dev\roadmap-template.md` in the same step

## Domain-specific notes

Fill these in as decisions are made (chunking strategy, retrieval fusion, prompt rules, eval results). Record the why in `docs/` as short decision records and summarize in the README.

## What "done" looks like

A feature is done when it passes the gate, has tests for success and failure paths, logs its stages, is documented where a user or reviewer would look, and a full run completes end-to-end even if one document or question fails partway. The project as a whole is done when a fresh clone can follow the README to ingest, ask, and evaluate, and the README shows real eval numbers.
