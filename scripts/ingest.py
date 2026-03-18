import json

def parse_chunks(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    raw_chunks = [block.strip() for block in content.strip().split("---") if block.strip()]
    chunks = []

    for i in range(0, len(raw_chunks) - 1, 2):
        metadata_block = raw_chunks[i]
        content_block = raw_chunks[i + 1]

        metadata = {}
        for line in metadata_block.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

        chunks.append({
            "text": content_block,
            "metadata": metadata
        })

    return chunks

if __name__ == "__main__":
    filepath = "data/japanese_grammar.txt"
    chunks = parse_chunks(filepath)

    print(f"Found {len(chunks)} chunks")
    for idx, chunk in enumerate(chunks):
        print(f"Chunk {idx + 1}")
        print(f"Metadata {chunk['metadata']}")
        print(f"Text Preview {chunk['text'][:80]}....")
        print()

    with open("data/chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)

    print("Chunks saved to data/chunks.json")