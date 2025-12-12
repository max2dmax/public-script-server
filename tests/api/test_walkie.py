def test_walkie_requires_audio(client):
    res = client.post("/walkie")
    assert res.status_code == 400

def test_walkie_locked_persona(client):
    data = {
        "persona": "elissatron",
        "key": "wrong"
    }
    res = client.post("/walkie", data=data)
    assert res.status_code == 403