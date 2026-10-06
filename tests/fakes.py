"""Deterministic stand-ins for the embedding model and the LLM, so tests need no GPU or network."""

import hashlib
import math
import re


class HashingEmbedder:
    """A bag-of-words stand-in for bge-m3: identical texts get identical vectors."""

    dimension = 512

    def embed(self, texts):
        vectors = []
        for text in texts:
            vector = [0.0] * self.dimension
            for word in re.findall(r"\w+", text.lower()):
                vector[int(hashlib.md5(word.encode()).hexdigest(), 16) % self.dimension] += 1.0
            norm = math.sqrt(sum(v * v for v in vector)) or 1.0
            vectors.append([v / norm for v in vector])
        return vectors


class RecordingChat:
    """Replies with a fixed text and records every prompt it receives."""

    def __init__(self, reply="Réponse [AI Act, Article 6, §2]", fail=False):
        self.reply = reply
        self.fail = fail
        self.calls = []

    def complete(self, system, user):
        self.calls.append((system, user))
        return self.reply

    def stream(self, system, user):
        self.calls.append((system, user))
        if self.fail:
            raise RuntimeError("model unreachable")
        for word in self.reply.split(" "):
            yield word + " "
