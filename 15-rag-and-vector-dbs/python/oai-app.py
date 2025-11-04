from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

load_dotenv()
EMBEDDING_MODEL_NAME = "text-embedding-3-small"
OPENAI_MODEL_NAME = "gpt-5-nano"

def connect_to_vector_db():
    chroma_client = chromadb.Client()
    return chroma_client

def create_collection(chroma_client, collection_name: str):
    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        embedding_function=OpenAIEmbeddingFunction(
            model_name=EMBEDDING_MODEL_NAME
        )
    )
    return collection

def add_document_to_collection(chroma_client, collection_name: str, document: dict):
    collection = chroma_client.get_collection(name=collection_name)
    collection.add(documents=[document])

def query_collection(chroma_client, collection_name: str, query: str, n_results: int = 5):
    collection = chroma_client.get_collection(name=collection_name)
    results = collection.query(query_texts=[query], n_results=n_results)
    return results

def create_vector_embedding(openai_client: OpenAI, text: str):
    response = openai_client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL_NAME
    )
    embedding = response.data[0].embedding
    return embedding

def cosine_similarity(vec1: list, vec2: list) -> float:
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def main():
    openai_client = OpenAI()
    chroma_client = connect_to_vector_db()
    collection = create_collection(chroma_client, "my_collection")


if __name__ == "__main__":
    main()