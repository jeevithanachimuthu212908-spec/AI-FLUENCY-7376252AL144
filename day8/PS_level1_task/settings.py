import hashlib
import os
import re
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent
HANDBOOK_DIR = ROOT / "handbook"
VECTOR_DIR = ROOT / os.getenv("VECTOR_DIR", "vector_store")
EMBED_PROVIDER = os.getenv("EMBED_PROVIDER", "hash").lower()
MAX_DISTANCE = float(os.getenv("MAX_DISTANCE", "0.60"))

if EMBED_PROVIDER != "hash":
    raise ValueError("Set EMBED_PROVIDER=hash in .env")


class HashEmbeddings:
    """Deterministic, offline embeddings for ChromaDB."""

    def __init__(self, dimensions=1024):
        self.dimensions = dimensions

    def _embed(self, text):
        tokens = re.findall(r"[a-z0-9]+", (text or "").lower())
        features = list(tokens)
        features += [
            f"{a}_{b}" for a, b in zip(tokens, tokens[1:])
        ]

        compact = " ".join(tokens)
        padded = f"  {compact}  "
        features += [
            padded[i:i + 3]
            for i in range(max(0, len(padded) - 2))
        ]

        vector = [0.0] * self.dimensions

        for feature in features:
            digest = hashlib.blake2b(
                feature.encode("utf-8"), digest_size=8
            ).digest()

            number = int.from_bytes(digest, "little")
            index = number % self.dimensions
            sign = 1.0 if ((number >> 8) & 1) else -1.0
            vector[index] += sign

        norm = sum(v * v for v in vector) ** 0.5

        if norm:
            vector = [v / norm for v in vector]

        return vector

    def embed_documents(self, texts):
        return [self._embed(text) for text in texts]

    def embed_query(self, text):
        return self._embed(text)