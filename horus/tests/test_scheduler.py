from horus.automations import Scheduler, Automation

def test_scheduler():
    s=Scheduler(); s.create(Automation(name="nightly", prompt="audit", schedule="0 2 * * *"))
    assert len(s.list()) == 1
