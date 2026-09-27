import pytest

from enterprise_network_ai.rag import (
    chunk_text,
)


def test_chunk_text():

    text = " ".join(
        f"word{i}"
        for i in range(1, 101)
    )

    chunks = chunk_text(
        text=text,
        chunk_size=30,
        overlap=5,
    )

    assert len(chunks) > 1

    assert chunks[0].startswith(
        "word1"
    )

    assert "word30" in chunks[0]

    assert chunks[1].startswith(
        "word26"
    )


def test_empty_text():

    assert chunk_text("") == []


def test_invalid_chunk_size():

    with pytest.raises(ValueError):

        chunk_text(
            text="hello world",
            chunk_size=0,
        )


def test_invalid_overlap():

    with pytest.raises(ValueError):

        chunk_text(
            text="hello world",
            chunk_size=10,
            overlap=10,
        )