import pytest
from raglab.core import split_words, load_chunks

def test_overlap():
    result=split_words('a b c d e f',4,2)
    assert result[0]=='a b c d'
    assert result[1]=='c d e f'

def test_invalid_overlap():
    with pytest.raises(ValueError):split_words('one two',3,3)

def test_documents_have_sources():
    chunks=load_chunks()
    assert chunks and all(c.source.endswith('.md') for c in chunks)
