from horus.skills import SkillRegistry

def test_skill_create_improve(tmp_path):
    r = SkillRegistry(str(tmp_path / "skills"))
    s = r.create_from_session("Repo Audit", "Audit repositories", ["inspect", "report"], ["read_file"])
    assert r.list()[0].name == "Repo Audit"
    s = r.record_use(s, True)
    assert s.success_rate > 0
