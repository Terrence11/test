# Complete Week 3 — RAG hands-on (Days 1–7)

A self-contained, beginner-friendly Python RAG learning project tailored to industry/NAICS questions. Uses **fictionalized educational notes**; not an authoritative source of company or NAICS assignments.

## Install

```bash
cd rag_week_full
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

OpenAI API calls cost money. Before Days 2–6, export an API key **in your own terminal** (never put credentials in code or Git):

```bash
read -s OPENAI_API_KEY && echo
export OPENAI_API_KEY
```

You can optionally set `OPENAI_MODEL` if you need a supported alternative to the default `gpt-4.1-mini`.

## Day 1 — Chunking (30–45 minutes; no API key)

```bash
python -m raglab.chunking --size 45 --overlap 10
python -m raglab.chunking --size 100 --overlap 20
```

Read `raglab/core.py`: `split_words()` and `load_chunks()`. Compare number of chunks and whether a sentence is cut across chunks. Sizes are **words**, not tokens. Exercise: change overlap to 0 and compare.

## Day 2 — Embeddings + Chroma (45–60 minutes)

```bash
python -m raglab.index
python -m raglab.retrieve "What does Boeing manufacture?"
python -m raglab.retrieve "Which NAICS code relates to courier services?" --top-k 3
```

The embedding model is `text-embedding-3-small`; Chroma is local and persisted at `.chroma/`. `index` regenerates the collection contents each time; it replaces the existing index. API key needed for **both index and retrieval** because a query is embedded. Cosine distance: **smaller** generally means closer, not verified correctness. Exercise: compare two questions' top-3 results.

## Day 3 — RAG answers + evidence (45–60 minutes)

```bash
python -m raglab.ask "What activity does FedEx mainly perform in these notes?"
python -m raglab.ask "Which code is shown for aircraft manufacturing?"
python -m raglab.ask "What is the store return policy?"
```

Flow: query embedding → Chroma top-k → assemble cited snippets → LLM response (`responses.parse`) → validate returned chunk IDs against actual retrieval results. A citation is a link to supplied context, **not a guarantee the claim is true**. Test an out-of-scope question. The demo uses top 3 chunks as model context.

## Day 4 — Reranking (45 minutes)

```bash
python -m raglab.rerank "What is aircraft manufacturing?" --method keyword
python -m raglab.ask "What is aircraft manufacturing?" --rerank keyword
```

`keyword` is a simple baseline, **not** a learned cross-encoder. Optional advanced version:

```bash
python -m pip install -r requirements-rerank.txt
python -m raglab.rerank "What is aircraft manufacturing?" --method cross
```

The `cross` option downloads a third-party model and may take longer; compare ranking quality, not just appearance. It ranks retrieved candidates, not the entire corpus.

## Day 5 — FastAPI (45 minutes)

```bash
uvicorn raglab.api:app --reload
```

Open http://localhost:8000/docs, POST `/ask` with:

```json
{"question":"What does Boeing manufacture?","top_k":5,"rerank":"none"}
```

`GET /health` is an alive check, not proof that external API or vector index works. `POST /ask` needs the index from Day 2 and API credentials. Try empty question and top_k=0 to see 422.

## Day 6 — Evaluation (45 minutes)

```bash
python -m raglab.evaluate
python -m raglab.evaluate --rerank keyword
```

Five labeled questions in `data/eval_questions.jsonl`. Compare Hit@1 and Hit@3; these are **retrieval** metrics, not answer correctness. Small sample is only a smoke test. Add five questions of your own, including ambiguous descriptions. For generation quality, manually inspect answer support and citations.

## Day 7 — Docker + CI (45–60 minutes)

```bash
python -m pytest -q
docker build -t rag-week:v1 .
```

For the **API to work inside Docker**, index the mounted data directory and pass the key at runtime. First create a named volume and populate it using the container:

```bash
docker volume create rag-chroma
docker run --rm -e OPENAI_API_KEY -v rag-chroma:/app/.chroma rag-week:v1 python -m raglab.index
docker run --rm -p 8000:8000 -e OPENAI_API_KEY -v rag-chroma:/app/.chroma rag-week:v1
```

Keep `OPENAI_API_KEY` exported in the same local shell. On Apple Silicon, Docker may download a platform-compatible Python image automatically. The `.github/workflows/ci.yml` workflow runs offline pytest and `docker build` on GitHub pushes; it does **not** perform paid OpenAI calls or publish images. For an existing Git repository, move the `.github/workflows/ci.yml` into its repository root and commit the project files (exclude `.venv`, `.chroma`, `.env`).

## Design notes / limitations

- No external services besides paid OpenAI API and optional cross-encoder model downloads; Chroma runs locally.
- Example docs intentionally small. Word-based chunks are for clarity; use token-aware, section-aware splitting for real documents.
- The local Chroma index is built from trusted educational Markdown; do not send confidential company material to third-party APIs without authorization.
- Simple in-process synchronous FastAPI endpoint; not a production scalability/security implementation.
- This ZIP is for study. Production would add authentic source ingestion, secret management, access control, evaluation datasets, citation checking, monitoring, proper dependency locking and hosted vector storage.
