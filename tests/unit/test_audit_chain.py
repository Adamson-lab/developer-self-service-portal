from core import audit


def setup_function():
    audit.reset()


def test_chain_verifies_when_untouched():  # G-07
    for i in range(5):
        audit.record("request.submitted", request_id=str(i))
    assert audit.verify() == (True, None)


def test_tampering_is_detected():  # G-07
    for i in range(3):
        audit.record("request.submitted", request_id=str(i))
    audit._EVENTS[1]["request_id"] = "forged"
    intact, seq = audit.verify()
    assert not intact and seq == 2


def test_deletion_is_detected():  # G-07
    for i in range(3):
        audit.record("request.submitted", request_id=str(i))
    del audit._EVENTS[1]
    intact, _ = audit.verify()
    assert not intact
