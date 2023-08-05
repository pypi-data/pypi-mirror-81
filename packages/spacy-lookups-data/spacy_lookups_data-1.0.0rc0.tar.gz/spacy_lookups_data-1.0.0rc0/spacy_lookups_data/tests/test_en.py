import pytest
from spacy.tokens import Doc


@pytest.mark.xfail
@pytest.mark.parametrize("text", ["faster", "fastest", "better", "best"])
def test_en_lemmatizer_handles_irreg_adverbs(en_nlp, text):
    tokens = en_nlp(text)
    assert tokens[0].lemma_ in ["fast", "well"]


@pytest.mark.xfail
def test_issue4104(en_nlp):
    """Test that English lookup lemmatization of spun & dry are correct
    expected mapping = {'dry': 'dry', 'spun': 'spin', 'spun-dry': 'spin-dry'}
    """
    words = ["dry", "spun", "spun-dry"]
    doc = Doc(en_nlp.vocab, words=words)
    lemmatizer = en_nlp.get_pipe("lemmatizer")
    doc = lemmatizer(doc)
    assert [token.lemma_ for token in doc] == ["dry", "spin", "spin-dry"]


@pytest.mark.parametrize(
    "text,norms", [("I'm", ["i", "am"]), ("shan't", ["shall", "not"])]
)
def test_en_tokenizer_norm_exceptions(en_nlp, text, norms):
    tokens = en_nlp(text)
    assert [token.norm_ for token in tokens] == norms
