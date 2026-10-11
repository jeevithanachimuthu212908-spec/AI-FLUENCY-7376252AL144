import shutil

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from settings import HANDBOOK_DIR, VECTOR_DIR, HashEmbeddings

COLLECTION_NAME = "college_handbook"


def main():
    paths = sorted(HANDBOOK_DIR.glob("*.md"))

    if len(paths) != 6:
        raise SystemExit(
            f"Expected 6 documents, found {len(paths)}"
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=650,
        chunk_overlap=100,
        separators=["\n## ", "\n### ", "\n", " ", ""]
    )

    texts = []
    metadatas = []

    for path in paths:
        content = path.read_text(encoding="utf-8")
        chunks = splitter.split_text(content)

        for index, chunk in enumerate(chunks):
            texts.append(chunk)
            metadatas.append({
                "source": path.name,
                "chunk": index
            })

    if VECTOR_DIR.exists():
        shutil.rmtree(VECTOR_DIR)

    store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTOR_DIR),
        embedding_function=HashEmbeddings(),
        collection_metadata={"hnsw:space": "cosine"}
    )

    store.add_texts(
        texts=texts,
        metadatas=metadatas
    )

    print(f"Documents loaded: {len(paths)}")
    print(f"Chunks indexed: {len(texts)}")
    print(f"Vector store: {VECTOR_DIR}")


if __name__ == "__main__":
    main()