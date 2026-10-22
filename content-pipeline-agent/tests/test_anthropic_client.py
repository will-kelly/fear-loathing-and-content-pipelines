"""AnthropicClient response handling, with the SDK's network layer stubbed.

Checks that text blocks are concatenated, web-search citations are collected,
server_tool_use blocks are counted, and a ``pause_turn`` is continued by
resending the assistant content unchanged.
"""

from types import SimpleNamespace

import pytest

anthropic = pytest.importorskip("anthropic")

from content_pipeline.llm import AnthropicClient  # noqa: E402


class _FakeMessages:
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self._responses.pop(0)


def _text(t, cites=None):
    return SimpleNamespace(type="text", text=t, citations=cites or [])


def _cite(url, title):
    return SimpleNamespace(type="web_search_result_location", url=url, title=title, cited_text="snippet")


def _resp(content, stop="end_turn"):
    return SimpleNamespace(content=content, stop_reason=stop, usage=SimpleNamespace(input_tokens=10, output_tokens=5))


def _client(responses):
    c = AnthropicClient.__new__(AnthropicClient)
    c.model = "test-model"
    c._client = SimpleNamespace(messages=_FakeMessages(responses))
    return c


def test_collects_text_citations_and_search_count():
    responses = [
        _resp([
            _text("I'll search. "),
            SimpleNamespace(type="server_tool_use", id="s1", name="web_search", input={"query": "x"}),
            SimpleNamespace(type="web_search_tool_result", tool_use_id="s1", content=[]),
            _text('{"ok": true}', cites=[_cite("https://a.example", "A"), _cite("https://a.example", "A dup")]),
        ])
    ]
    client = _client(responses)
    res = client.complete(stage="claims", system="s", user="u", max_tokens=100, temperature=0.2, web_search=True)
    assert res.json() == {"ok": True}
    assert res.searches == 1
    assert [c.url for c in res.citations] == ["https://a.example"]
    sent = client._client.messages.calls[0]
    assert sent["tools"][0]["type"] == "web_search_20250305"
    assert sent["tools"][0]["max_uses"] == 5


def test_pause_turn_is_continued():
    first = _resp([_text("partial ")], stop="pause_turn")
    second = _resp([_text('{"done": 1}')])
    client = _client([first, second])
    res = client.complete(stage="claims", system="s", user="u", max_tokens=100, temperature=0.2, web_search=True)
    calls = client._client.messages.calls
    assert len(calls) == 2
    # The paused assistant content is resent verbatim as the next message.
    assert calls[1]["messages"][1] == {"role": "assistant", "content": first.content}
    assert res.text == "partial " + '{"done": 1}'


def test_no_tools_key_when_search_off():
    client = _client([_resp([_text("{}")])])
    client.complete(stage="draft", system="s", user="u", max_tokens=100, temperature=0.4)
    assert "tools" not in client._client.messages.calls[0]
