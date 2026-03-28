import os

# File types to include
SUPPORTED_EXTENSIONS = [".py", ".js", ".ts", ".jsx", ".tsx", ".json", ".yaml", ".yml", ".md"]

# Folders to ignore
IGNORE_DIRS = {"venv", "__pycache__", ".git", "node_modules", "dist", "build"}


def is_valid_file(file_name):
    return any(file_name.endswith(ext) for ext in SUPPORTED_EXTENSIONS)


def should_ignore_dir(dir_name):
    return dir_name in IGNORE_DIRS


def chunk_code(content, chunk_size=300):
    """
    Splits code into chunks (line-based)
    """
    lines = content.split("\n")
    chunks = []

    for i in range(0, len(lines), chunk_size):
        chunk_lines = lines[i:i + chunk_size]
        chunk_text = "\n".join(chunk_lines)

        chunks.append({
            "chunk_id": i // chunk_size,
            "content": chunk_text
        })

    return chunks


def extract_code(repo_path):
    """
    Extracts and structures code from repository

    Returns:
        List[Dict] with:
        - source (file + chunk)
        - type (code)
        - file_path
        - content
    """

    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"Repository path not found: {repo_path}")

    code_chunks = []

    try:
        for root, dirs, files in os.walk(repo_path):

            # Remove ignored directories
            dirs[:] = [d for d in dirs if not should_ignore_dir(d)]

            for file in files:
                if not is_valid_file(file):
                    continue

                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()

                    if not content:
                        continue

                    chunks = chunk_code(content)

                    for chunk in chunks:
                        code_chunks.append({
                            "source": f"{file}:chunk_{chunk['chunk_id']}",
                            "type": "code",
                            "file_path": file_path,
                            "content": chunk["content"]
                        })

                except Exception:
                    # Skip problematic files but continue processing
                    continue

    except Exception as e:
        raise RuntimeError(f"Error processing repository: {str(e)}")

    return code_chunks