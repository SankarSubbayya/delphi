from delphi.agent import _extract_json


def test_extract_json_finds_object():
    text = 'Here is my answer:\n{"position": 0.7, "confidence": 0.8, "reasoning": "yes", "sources": []}'
    out = _extract_json(text)
    assert out["position"] == 0.7
    assert out["confidence"] == 0.8


def test_extract_json_handles_markdown_fences():
    text = '```json\n{"position": "positive", "confidence": 0.5, "reasoning": "x", "sources": []}\n```'
    out = _extract_json(text)
    assert out["position"] == "positive"


def test_extract_json_returns_empty_on_garbage():
    assert _extract_json("no json here") == {}
    assert _extract_json("") == {}
    assert _extract_json("{ this is not valid json") == {}
