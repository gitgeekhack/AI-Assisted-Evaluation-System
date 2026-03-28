# AI-Assisted Evaluation MVP

## 🚀 Overview

This project builds an AI-powered evaluation system that ingests multiple artefacts (deck, video, code, prototype URL) and generates a **consistent, evidence-backed evaluation**.

---

## 🧠 Key Features

* Multi-artifact ingestion (PDF, PPT, video transcript, code, URL)
* Unified evidence layer using vector DB (FAISS)
* Cross-artifact claim validation
* Prototype validation using Playwright
* Evidence-grounded scoring with citations & confidence

---

## 🏗 Architecture

Ingestion → Chunking → Embeddings → Vector DB → Retrieval
→ Unified Summary → Claim Validation → Scoring

---

## ▶️ How to Run
First of all, install Ollama in the system and start the Ollama server and then pull the required LLM model
```bash
pip install -r requirements.txt
playwright install
python main.py
```

---

## 📤 Output

Structured JSON:

* Summary
* Prototype validation
* Claim validation
* Rubric-based scores

---

## 🧪 Sample Data

Add your submission inside:

```
sample_data/submission_1/
```

---

## 🎯 Design Principles

* Evidence before scoring
* Cross-artifact validation
* Traceability via citations
* Consistency via structured prompts

---

## 🔥 Highlights

* RAG-based evaluation system
* Multi-source reasoning
* Real-world prototype validation
