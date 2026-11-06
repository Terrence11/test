import sys
from types import SimpleNamespace

import pytest

from raglab import core


def test_answer_uses_top_three_chunks_and_filters_unknown_citations(monkeypatch):
    hits = [
        {"id": f"chunk-{index}", "text": f"text {index}", "source": f"{index}.md"}
        for index in range(1, 5)
    ]
    monkeypatch.setattr(core, "retrieve", lambda question, k: hits)

    parsed_answer = SimpleNamespace(
        answer="The answer is supported.",
        cited_chunk_ids=["chunk-2", "not-retrieved", "chunk-4"],
    )
    parse_calls = {}

    class FakeResponses:
        def parse(self, **kwargs):
            parse_calls.update(kwargs)
            return SimpleNamespace(output_parsed=parsed_answer)

    class FakeOpenAI:
        def __init__(self):
            self.responses = FakeResponses()

    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=FakeOpenAI))

    result = core.answer_question("What is the answer?")

    assert result["answer"] == "The answer is supported."
    assert [hit["id"] for hit in result["retrieved_chunks"]] == [
        "chunk-1",
        "chunk-2",
        "chunk-3",
    ]
    assert result["citations"] == [{"chunk_id": "chunk-2", "source": "2.md"}]
    assert "chunk-4" not in parse_calls["input"]


def test_answer_raises_when_model_returns_no_parsed_answer(monkeypatch):
    monkeypatch.setattr(
        core,
        "retrieve",
        lambda question, k: [
            {"id": "chunk-1", "text": "text", "source": "notes.md"}
        ],
    )

    class FakeResponses:
        def parse(self, **kwargs):
            return SimpleNamespace(output_parsed=None)

    class FakeOpenAI:
        def __init__(self):
            self.responses = FakeResponses()

    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=FakeOpenAI))

    with pytest.raises(RuntimeError, match="no parsed answer"):
        core.answer_question("What is the answer?")
