import re

def markdown_chunking(markdown_text, max_chunk_size=1000, overlap=100):
    """
    Splits a Markdown document into chunks based on header hierarchy.

    Args:
        markdown_text (str): Markdown content as a single string.
        max_chunk_size (int): Maximum number of characters per chunk.
        overlap (int): Number of overlapping characters between chunks.

    Returns:
        List[str]: A list of chunked sections.
    """
    # Step 1: Split by top-level and sub-level headers (e.g., #, ##, ###) - Only upto ##
    header_pattern = re.compile(r'^(#{1,2})\s+(.*)', re.MULTILINE)
    sections = []
    current_section = {"header": "", "content": ""}
    lines = markdown_text.splitlines()

    for line in lines:
        header_match = header_pattern.match(line)
        if header_match:
            if current_section["content"]:
                sections.append(current_section)
            current_section = {
                "header": line.strip(),
                "content": ""
            }
        else:
            current_section["content"] += line + "\n"

    if current_section["content"]:
        sections.append(current_section)

    # Step 2: Combine smaller sections, and chunk large ones further if needed
    chunks = []
    for section in sections:
        text = section["header"] + "\n" + section["content"]
        if len(text) <= max_chunk_size:
            chunks.append(text.strip())
        else:
            # Fallback: split by paragraphs inside the large section
            paragraphs = text.split("\n\n")
            current_chunk = ""
            for para in paragraphs:
                if len(current_chunk) + len(para) + 2 <= max_chunk_size:
                    current_chunk += para + "\n\n"
                else:
                    chunks.append(current_chunk.strip())
                    current_chunk = para + "\n\n"
            if current_chunk:
                chunks.append(current_chunk.strip())

    # Step 3: Add optional overlap
    if overlap > 0 and len(chunks) > 1:
        overlapped_chunks = []
        for i in range(len(chunks)):
            prev = chunks[i - 1][-overlap:] if i > 0 else ""
            overlapped_chunks.append(prev + chunks[i])
        return overlapped_chunks

    return chunks