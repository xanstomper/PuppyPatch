from horus_gateway.adapters import GatewayRouter, InMemoryAdapter

def test_gateway_router():
    r=GatewayRouter(); a=InMemoryAdapter("cli"); r.register(a); r.set_home("u","cli"); r.deliver("u","hello")
    assert a.sent == [("u","hello")]
