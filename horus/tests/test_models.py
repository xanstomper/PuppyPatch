from horus.models import ModelRouter, ProviderRegistry, detect_capabilities, ModelRef

def test_provider_registry():
    assert ProviderRegistry().supports("openrouter")
    assert ProviderRegistry().supports("custom")

def test_model_route():
    r = ModelRouter("openrouter:default", {"coder":"nvidia:nemotron"})
    assert r.route("coder").provider == "nvidia"

def test_capabilities():
    assert detect_capabilities(ModelRef.parse("gemini:gemini-2.5-pro")).context_window >= 128000
