import itertools

import pytest

from app.schemas.documents import PageText
from app.services.chunker import chunk_pages, split_text


def test_empty_text_gives_no_chunks() -> None:
    assert split_text("   \n  ", 100, 10) == []


def test_short_text_is_single_chunk() -> None:
    assert split_text("hola mundo", 100, 10) == ["hola mundo"]


def test_whitespace_is_normalized() -> None:
    assert split_text("hola\n\n  mundo", 100, 10) == ["hola mundo"]


def test_long_text_is_split_with_overlap() -> None:
    text = " ".join(f"palabra{i}" for i in range(200))
    chunks = split_text(text, 100, 20)

    assert len(chunks) > 1
    assert all(len(c) <= 100 for c in chunks)
    # solapamiento: el final de un fragmento reaparece al inicio del siguiente
    for previous, current in itertools.pairwise(chunks):
        assert previous.split()[-1] in current.split()


def test_no_content_is_lost() -> None:
    words = [f"w{i}" for i in range(300)]
    chunks = split_text(" ".join(words), 80, 15)
    seen = {word for chunk in chunks for word in chunk.split()}
    assert seen == set(words)


def test_words_are_not_cut() -> None:
    words = {f"palabra{i}" for i in range(200)}
    for chunk in split_text(" ".join(sorted(words)), 100, 20):
        assert set(chunk.split()) <= words


def test_zero_overlap_works() -> None:
    chunks = split_text("a " * 100, 50, 0)
    assert len(chunks) >= 2


def test_invalid_parameters() -> None:
    with pytest.raises(ValueError):
        split_text("hola", 0, 0)
    with pytest.raises(ValueError):
        split_text("hola", 10, 10)


def test_chunks_keep_page_number_and_global_index() -> None:
    pages = [
        PageText(page=1, text="uno " * 100),
        PageText(page=2, text=""),
        PageText(page=3, text="tres " * 100),
    ]
    chunks = chunk_pages(pages, 100, 10)

    assert [c.index for c in chunks] == list(range(len(chunks)))
    assert {c.page for c in chunks} == {1, 3}
    assert all(c.text.startswith("uno") for c in chunks if c.page == 1)