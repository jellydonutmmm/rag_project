# Roadmap

Build order for the RAG Q&A project, derived from README.md and CLAUDE.md (started from `C:\dev\roadmap-template.md`).

**Workflow rules**

- Every checkbox is a checkpoint: when it is done, the quality gate passes, the box is ticked, and it is committed (one commit per checkpoint, imperative message).
- At the end of every numbered section, `git push`.
- Every module gets logging, exception handling at its external boundaries, and tests in the same checkpoint as the code, never retrofitted.

## 0. Project setup

- [ ] Add `roadmap.md`; commit and push
- [ ] Create venv, `/src`, `/tests`, `/docs`; extend `.gitignore` (`.env`, `*.log`, vector store and data dirs, caches)
- [ ] Install dev tools (pytest, pytest-cov, ruff, mypy strict, pre-commit, detect-secrets, pip-audit); `pip freeze > requirements.txt`
- [ ] Config files: `pytest.ini` (90% coverage gate), `mypy.ini` (strict), `ruff.toml`
- [ ] `.pre-commit-config.yaml` running format check, lint, mypy, pytest and detect-secrets on every commit; `pre-commit install`; test the secret scan once with a fake key
- [ ] `.env.example` (names only)
- [ ] GitHub Actions CI workflow running the same gate on every push and pull request; badge in README
- [ ] Repo hygiene: LICENSE, `.github/dependabot.yml`, `.editorconfig`
- [ ] Rewrite CLAUDE.md for the real project (replace "Project status", delete `CLAUDE-template.md`)
- [ ] Push

## 1. Logging & error-handling foundation

- [ ] `src/logging_config.py`: one consistent format, console plus rotating log file, configured once at the entry point only; tests
- [ ] Redaction filter so secrets (API keys, tokens) never reach logs, even via exception messages; tests
- [ ] `src/errors.py`: project exception hierarchy (ingest, embed, retrieve, generate) so boundaries raise or catch specific types; tests
- [ ] `src/config.py`: typed settings loaded from the environment, fails fast with a clear message when a required value is missing; tests
- [ ] Document the conventions in CLAUDE.md (per-module logger, boundary handling, no secrets in logs)
- [ ] Push

## 2. Domain & corpus

- [ ] Choose the document domain (decision pending) and record why in the README
- [ ] Record each source's license and provenance in `docs/corpus.md`
- [ ] Download script for a small, reproducible corpus (raw data is gitignored); tests with mocked network
- [ ] Push

## 3. Ingestion & chunking

- [ ] Loaders per format (PDF / HTML / Markdown / text) returning a normalized `Document`; corrupt or empty files are skipped and logged, never fatal
- [ ] Cleaning step for messy input (headers/footers, whitespace, encoding)
- [ ] Chunking with metadata (source, page/section, offsets); document the strategy and its tradeoffs
- [ ] Tests, including malformed and empty files
- [ ] Push

## 4. Embeddings & vector store

- [ ] `embed.py`: local sentence-transformers behind an interface; batching; model name in config
- [ ] `store.py`: Chroma persistence, idempotent re-ingestion (same chunk id, no duplicates)
- [ ] Tests with a fake embedder and a temporary store, including failure cases
- [ ] Push

## 5. Retrieval

- [ ] Dense retrieval with a score threshold
- [ ] Keyword (BM25) retrieval and hybrid fusion; document why
- [ ] Optional reranking step, only if the eval (Section 7) shows it helps
- [ ] Tests covering empty results, ties and filters
- [ ] Push

## 6. Answer generation (Claude)

- [ ] Prompt design: answer only from the supplied passages, cite chunk ids, say "I don't know" when the passages don't support an answer; prompts live in `/prompts`, versioned
- [ ] Structured output schema (`answer`, `citations`, `grounded`); validate at the boundary; retry once on malformed output, then return a safe default with a `failed` flag
- [ ] Anthropic boundary: timeouts, retries with backoff, never log the key; token and cost logging per call
- [ ] Tests with a mocked client: valid, malformed, refusal, API failure, no-context question
- [ ] Push

## 7. Evaluation harness (`/eval`)

- [ ] Hand-written question set with expected source passages (at least 30 questions, including unanswerable ones)
- [ ] Retrieval metrics: hit rate@k, MRR, recall@k
- [ ] Answer metrics: citation correctness, abstention rate on unanswerable questions
- [ ] Results written to `eval/results/` and summarized in the README, with a before/after comparison for at least one design change (chunk size or hybrid vs dense)
- [ ] Tests for the metric code
- [ ] Push

## 8. Integration & CLI

- [ ] `pipeline.py` is the only place that chains ingest, retrieve and generate
- [ ] Per-stage event logging, one failing document or question never stops a run, run summary (processed, succeeded, failed)
- [ ] CLI (`ingest`, `ask`, `eval`) using argparse; entry point is the only place `configure_logging()` is called
- [ ] End-to-end test with every external call mocked, including one failing item
- [ ] Push

## 9. Streamlit UI

- [ ] Thin UI over `pipeline.py`: question box, answer, expandable cited passages, error states shown to the user
- [ ] Tests for non-UI logic; manual check of the UI in a browser
- [ ] Push

## 10. Quality gate

Wired up in Section 0; verify it holds at the end of every section.

- [ ] `ruff format --check`, `ruff check`, `mypy` (strict), `pytest` with coverage at or above 90%, detect-secrets
- [ ] `pip-audit -r requirements.txt` before each push of a section that changes dependencies
- [ ] CI green on `main`

## 11. External services & credentials

### Anthropic
Purpose: answer generation (and optionally LLM-as-judge in the eval)
Env var(s): `ANTHROPIC_API_KEY`
Limits / cost: per-token billing; log token usage per call
1. Go to https://console.anthropic.com and sign in.
2. Create an API key dedicated to this project.
3. Add `ANTHROPIC_API_KEY=<value>` to `.env`.
4. Verify with one real question.
Rotate / revoke: console, API keys, then update `.env` and any CI secret.

- [ ] Anthropic key created, stored in `.env`, verified with one real call, rotation noted
- [ ] `ANTHROPIC_API_KEY` added as a GitHub repository secret only if CI needs it (it should not; CI uses mocks)

## 12. Manual verification ("done" bar)

- [ ] Ingest the real corpus and ask at least 10 real questions; read the answers and citations by hand
- [ ] Confirm unanswerable questions get "I don't know"
- [ ] Simulate a failure (bad file, API outage) and confirm the run survives
- [ ] Fresh-clone test: follow the README from scratch on a clean checkout

## 13. Documentation cleanup

- [ ] README placeholders replaced with real content, architecture diagram, eval results, screenshot or GIF
- [ ] "Known limitations" and "What I'd do differently" written from actual findings
- [ ] `docs/` holds corpus notes and short architecture decision records (chunking, retrieval, embeddings)
- [ ] Add a roadmap item to `C:\dev\roadmap-template.md` for anything here that applies to other projects (CI, dependabot, license, redaction filter, fresh-clone test)
