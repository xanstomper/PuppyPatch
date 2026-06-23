from horus.core.config import HorusConfig

def test_config_load_default(tmp_path):
    cfg = HorusConfig.load(tmp_path / "missing.yaml")
    assert cfg.agents.max_concurrent == 60

def test_config_save_load(tmp_path):
    p = tmp_path / "horus.yaml"
    cfg = HorusConfig()
    cfg.models.default = "openai:gpt-5.1"
    cfg.save(p)
    assert HorusConfig.load(p).models.default == "openai:gpt-5.1"
