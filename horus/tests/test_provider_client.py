from horus.models import OpenAICompatibleClient, ChatRequest, ChatMessage, ModelRef, supports_request

def test_provider_payload_and_endpoint(monkeypatch):
    c=OpenAICompatibleClient({"custom":"http://localhost:9999/v1"})
    req=ChatRequest(ModelRef.parse("custom:test"), [ChatMessage("user","hi")])
    assert c.endpoint("custom") == "http://localhost:9999/v1/chat/completions"
    assert c.payload(req)["messages"][0]["content"] == "hi"

def test_supports_request():
    assert supports_request(ModelRef.parse("openrouter:claude-sonnet-4.5"), tools=True, json_mode=True)
