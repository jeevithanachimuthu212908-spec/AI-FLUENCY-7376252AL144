from langchain_chroma import Chroma

from settings import VECTOR_DIR, HashEmbeddings, MAX_DISTANCE

COLLECTION_NAME = "college_handbook"


def open_store():
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTOR_DIR),
        embedding_function=HashEmbeddings(),
        collection_metadata={"hnsw:space": "cosine"}
    )


def main():
    store = open_store()

    questions = [
        "What CGPA do I need to be eligible for placements?",
        "What is the capital of France?"
    ]

    for query in questions:
        print(f"\nQUESTION: {query}")

        results = store.similarity_search_with_score(
            query, k=3
        )

        for document, score in results:
            print(
                f"Score: {score:.4f} | "
                f"Source: {document.metadata.get('source')} | "
                f"Chunk: {document.metadata.get('chunk')}"
            )

        kept = [
            (doc, score)
            for doc, score in results
            if float(score) <= MAX_DISTANCE
        ]

        if kept:
            print("Guard: MATCH")
            print("Top source:", kept[0][0].metadata["source"])
        else:
            print("Guard: NO_MATCH")

        print("MAX_DISTANCE:", MAX_DISTANCE)


if __name__ == "__main__":
    main()