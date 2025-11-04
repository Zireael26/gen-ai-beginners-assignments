from dotenv import load_dotenv
from openai import OpenAI
from vector_db import connect_to_vector_db, create_collection, create_vector_embedding, get_similar_documents
import pandas as pd
from pathlib import Path

load_dotenv()
OPENAI_MODEL_NAME = "gpt-5-nano"

def load_and_chunk_markdown(file_path: str):
    from md_chunking import markdown_chunking

    with open(file_path, 'r') as file:
        markdown_text = file.read()
    
    return markdown_chunking(markdown_text, max_chunk_size=500, overlap=50)
    

def add_data_to_collection(data_dir: str, collection):
    for file_path in Path(data_dir).glob("*"):
        chunks = load_and_chunk_markdown(file_path)
        print(f"Loaded and chunked {file_path.name} into {len(chunks)} chunks.")
        for i, chunk in enumerate(chunks):
            doc_id = f"{file_path.stem}_chunk_{i}"
            # print(f"{doc_id=}")
            # print(chunk)
            collection.add(
                ids=[doc_id],
                documents=[chunk]
            )
            print(f"Added chunk {i} from {file_path.name} to the collection.")

def main():
    openai_client = OpenAI()
    chroma_client = connect_to_vector_db()
    collection = create_collection(chroma_client, "my_collection")
    
    # Need only be called once
    # add_data_to_collection("15-rag-and-vector-dbs/data", collection)

    prompt = input("Enter your query: ")
    similar_docs = get_similar_documents(chroma_client=chroma_client, collection_name="my_collection", query_string=prompt, top_k=5)

    print("Top similar documents:")
    print(similar_docs)

    response = openai_client.responses.create(
        model=OPENAI_MODEL_NAME,
        instructions="Answer the user's question based on the provided documents.",
        reasoning={"effort": "low"},
        input=f"User Query: {prompt}\n\nRelevant Documents:\n" + "\n\n".join(similar_docs['document'].tolist())
    )
    
    print()
    print(response.output_text)

if __name__ == "__main__":
    main()