import pytest

from raglab import core


def test_keyword_rerank_prefers_more_matches_then_lower_distance():
    hits = [
        {"text": "No matching terms", "distance": 0.01},
        {"text": "FedEx courier service", "distance": 0.4},
        {"text": "FedEx courier industry notes", "distance": 0.8},
        {"text": "FedEx courier", "distance": 0.2},
    ]

    ranked = core.keyword_rerank("FedEx courier industry", hits)

    assert [hit["text"] for hit in ranked] == [
        "FedEx courier industry notes",
        "FedEx courier",
        "FedEx courier service",
        "No matching terms",
    ]


def test_retrieve_rejects_empty_question_before_accessing_index(monkeypatch):
    def fail_if_called():
        pytest.fail("the vector index should not be accessed")

    monkeypatch.setattr(core, "get_collection", fail_if_called)

    with pytest.raises(ValueError, match="Question cannot be empty"):
        core.retrieve("   ")


def test_retrieve_reports_empty_index(monkeypatch):
    class EmptyCollection:
        def count(self):
            return 0

    monkeypatch.setattr(core, "get_collection", EmptyCollection)

    with pytest.raises(RuntimeError, match="Vector index empty"):
        core.retrieve("What does FedEx do?")


def test_retrieve_limits_results_and_returns_metadata(monkeypatch):
    class Collection:
        def count(self):
            return 2

        def query(self, **kwargs):
            self.query_args = kwargs
            return {
                "ids": [["chunk-1", "chunk-2"]],
                "documents": [["first text", "second text"]],
                "metadatas": [
                    [{"source": "first.md", "chunk_index": 0},
                     {"source": "second.md", "chunk_index": 1}]
                ],
                "distances": [[0.1, 0.2]],
            }

    collection = Collection()
    monkeypatch.setattr(core, "get_collection", lambda: collection)
    monkeypatch.setattr(core, "embed_texts", lambda texts: [[0.5, 0.6]])

    results = core.retrieve("What does FedEx do?", k=5)

    assert collection.query_args["n_results"] == 2
    assert collection.query_args["query_embeddings"] == [[0.5, 0.6]]
    assert results == [
        {
            "id": "chunk-1",
            "text": "first text",
            "source": "first.md",
            "chunk_index": 0,
            "distance": 0.1,
        },
        {
            "id": "chunk-2",
            "text": "second text",
            "source": "second.md",
            "chunk_index": 1,
            "distance": 0.2,
        },
    ]
