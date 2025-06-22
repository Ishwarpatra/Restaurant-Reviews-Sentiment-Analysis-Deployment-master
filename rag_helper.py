from typing import List
import pandas as pd

try:
    from haystack.document_stores import InMemoryDocumentStore
    from haystack.nodes import BM25Retriever
except ImportError:  # haystack may not be available in all environments
    InMemoryDocumentStore = None
    BM25Retriever = None

document_store = None
retriever = None


def init_rag(doc_path: str = "Restaurant_Reviews.tsv") -> None:
    """Initialise the Haystack DocumentStore and Retriever with reviews."""
    global document_store, retriever
    if InMemoryDocumentStore is None:
        return
    if document_store is not None:
        return

    reviews = pd.read_csv(doc_path, delimiter="\t", quoting=3)
    docs = [{"content": row["Review"]} for _, row in reviews.iterrows()]
    document_store = InMemoryDocumentStore()
    document_store.write_documents(docs)
    retriever = BM25Retriever(document_store=document_store)


def retrieve_context(query: str, top_k: int = 3) -> str:
    """Retrieve contextual documents for the given query."""
    if retriever is None:
        return ""
    retrieved_docs = retriever.retrieve(query=query, top_k=top_k)
    context_parts = [doc.content for doc in retrieved_docs]
    return " \n".join(context_parts)

