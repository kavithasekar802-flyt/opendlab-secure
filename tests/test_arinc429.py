from src.arinc429 import pack_word, unpack_word

def test_pack_unpack_and_odd_parity():
    word = pack_word(label=0o203, data=12345, sdi=1, ssm=0)
    decoded = unpack_word(word)
    assert decoded["label"] == 0o203
    assert decoded["data"] == 12345
    assert decoded["sdi"] == 1
    assert decoded["parity_valid"] is True

def test_detect_parity_error():
    word = pack_word(label=0o310, data=42)
    corrupted = word ^ (1 << 12)
    assert unpack_word(corrupted)["parity_valid"] is False
