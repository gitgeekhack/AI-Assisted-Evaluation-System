# Design Note

## 1. Problem

Evaluating submissions across multiple artefacts leads to:

* inconsistent scoring
* unverifiable claims
* lack of traceability

---

## 2. Solution

We built an **AI Evidence Layer** that:

* aggregates signals across deck, video, code, and prototype
* stores them in a vector DB
* retrieves grounded evidence for evaluation

---

## 3. Key Components

### Ingestion Layer

Normalizes all artefacts into structured format.

### Evidence Store (RAG)

FAISS-based vector DB for retrieval.

### Unified Understanding

Combines multi-source insights into structured representation.

### Claim Validation

Cross-references claims across artefacts.

### Prototype Validation

Uses Playwright to validate real app behavior.

### Scoring Engine

Evaluates using rubric with:

* citations
* confidence
* strict grounding

---

## 4. Design Decisions

* Used FAISS for simplicity and speed
* Used structured prompts for deterministic outputs
* Used metadata for traceability

---

## 5. Trade-offs

* Heuristic-based UI interaction (not full E2E testing)
* Limited semantic understanding of code

---

## 6. Future Improvements

* Graph-based claim linking
* Better UI automation
* Function-level code understanding
