def test_homepage_loads(client):
    res = client.get("/")
    assert res.status_code == 200

def test_personas_endpoint(client):
    res = client.get("/personas")
    assert res.status_code == 200
    data = res.get_json()
    assert "personas" in data
    assert any(p["id"] == "maxnet" for p in data["personas"])

def test_sass_returns_line(client):
    res = client.get("/sass")
    assert res.status_code == 200
    assert "line" in res.get_json()