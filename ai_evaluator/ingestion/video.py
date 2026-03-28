import os
import re


def parse_timestamped_transcript(text):
    """
    Parses transcript with timestamps like:
    [00:02:10] User logs in
    """

    pattern = r"\[(\d{2}:\d{2}:\d{2})\](.*)"
    matches = re.findall(pattern, text)

    chunks = []

    for i, (timestamp, content) in enumerate(matches):
        cleaned_text = content.strip()

        if cleaned_text:
            chunks.append({
                "source": f"video_{timestamp}",
                "type": "video",
                "timestamp": timestamp,
                "content": cleaned_text
            })

    return chunks


def fallback_chunking(text, chunk_size=300):
    """
    Fallback if no timestamps found
    Splits transcript into chunks
    """

    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk_words = words[i:i + chunk_size]
        chunk_text = " ".join(chunk_words)

        chunks.append({
            "source": f"video_chunk_{i // chunk_size}",
            "type": "video",
            "content": chunk_text
        })

    return chunks


def load_video_transcript(file_path):
    """
    Main ingestion function for video transcripts

    Supports:
    - Timestamped transcripts
    - Plain text transcripts

    Returns:
        List[Dict] with:
        - source
        - type
        - timestamp (if available)
        - content
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Transcript file not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        # Try parsing timestamps
        parsed_chunks = parse_timestamped_transcript(text)

        if parsed_chunks:
            return parsed_chunks

        # Fallback if no timestamps detected
        return fallback_chunking(text)

    except Exception as e:
        raise RuntimeError(f"Error processing video transcript: {str(e)}")