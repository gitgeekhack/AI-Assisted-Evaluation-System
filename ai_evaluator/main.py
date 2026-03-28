import json

from ingestion.deck import extract_deck_text
from ingestion.video import load_video_transcript
from ingestion.code import extract_code
from ingestion.url import validate_url

from processing.chunking import chunk_data
from processing.embeddings import get_embeddings

from retrieval.vector_store import build_vector_store
from retrieval.retriever import retrieve_evidence

from evaluation.summary import generate_unified_summary
from evaluation.claim_validation import validate_claims
from evaluation.scoring import score_submission


def run_pipeline(submission_id, deck, video, code, url=None):

    # 1. Ingestion
    deck_data = extract_deck_text(deck)
    video_data = load_video_transcript(video)
    code_data = extract_code(code)

    all_docs = deck_data + video_data + code_data

    # 2. Chunking
    chunks = chunk_data(all_docs)

    # 3. Embeddings + Vector Store
    embeddings = get_embeddings()
    vector_store = build_vector_store(chunks, embeddings)

    # 4. Retrieval (core evidence)
    evidence = retrieve_evidence(
        vector_store,
        "problem solution features implementation architecture",
        k=8
    )

    # 5. Prototype Validation
    prototype_data = validate_url(url) if url else {}

    # 6. Unified Summary
    summary = generate_unified_summary(evidence, prototype_data)

    # 7. Claim Validation
    claim_validation = validate_claims(evidence, prototype_data)

    # 8. Scoring
    scores = score_submission(
        evidence,
        prototype_data=prototype_data,
        claim_validation=claim_validation
    )

    # 9. Final Output
    result = {
        "submission_id": submission_id,
        "summary": summary,
        "prototype_validation": prototype_data,
        "claim_validation": claim_validation,
        "scores": scores
    }

    return result


if __name__ == "__main__":

    result_1 = run_pipeline(
        submission_id="S1",
        deck="sample_data/submission_1/deck.pdf",
        video="sample_data/submission_1/video.txt",
        code="sample_data/submission_1/repo/",
        url="https://example.com"
    )

    result_2 = run_pipeline(
        submission_id="S2",
        deck="sample_data/submission_2/deck.pdf",
        video="sample_data/submission_2/video.txt",
        code="sample_data/submission_2/repo/",
        url="https://invalid-demo-app.com"
    )

    with open("output/result_1.json", "w") as f:
        json.dump(result_1, f, indent=2)

    with open("output/result_2.json", "w") as f:
        json.dump(result_2, f, indent=2)

    print("Evaluation Complete. Outputs saved.")