def test_walkie_locked_persona(client):
    data = {
        "persona": "elissatron",
        "key": "wrong"
    }
    res = client.post(
        "/walkie",
        data=data,
        content_type="multipart/form-data"
    )
    assert res.status_code == 403