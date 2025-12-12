from app import persona_unlocked, get_persona

def test_default_persona_unlocked():
    assert persona_unlocked("maxnet", None) is True

def test_elissatron_locked_without_key(monkeypatch):
    monkeypatch.setenv("ELISSATRON_KEY", "richgirl")
    assert persona_unlocked("elissatron", None) is False

def test_elissatron_unlocks_with_correct_key(monkeypatch):
    monkeypatch.setenv("ELISSATRON_KEY", "richgirl")
    assert persona_unlocked("elissatron", "richgirl") is True

def test_get_persona_defaults_to_maxnet():
    persona = get_persona("nonexistent")
    assert persona["label"].lower().startswith("maxnet")