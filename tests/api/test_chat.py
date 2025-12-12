from unittest.mock import patch

@patch("openai.ChatCompletion.create")
def test_chat_returns_reply(mock_openai, client):
    mock_openai.return_value = type(
        "obj", (),
        {"choices": [type("c", (), {"message": {"content": "hi bestie"}})]}
    )

    res = client.post("/chat", json={"history": []})
    assert res.status_code == 200
    assert res.get_json()["reply"] == "hi bestie"