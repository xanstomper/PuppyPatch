from horus.backends import LocalBackend, DockerBackend, SSHBackend, BackendRegistry

def test_local_backend_dry_run():
    r=LocalBackend().run("git push origin main", dry_run=True)
    assert r.risk == "destructive"

def test_backend_registry():
    reg=BackendRegistry(); reg.register(DockerBackend("python:3.11")); reg.register(SSHBackend("example.com"))
    assert "docker" in reg.list() and "ssh" in reg.list()
