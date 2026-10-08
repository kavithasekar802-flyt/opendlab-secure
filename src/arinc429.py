"""Educational ARINC 429 word utility.

This is not a substitute for the official ARINC specification. It models a
conventional 32-bit educational layout: bits 1..8 label, 9..10 SDI, 11..29
data, 30..31 SSM, and bit 32 odd parity.
"""


def _odd_parity_bit(lower_31_bits: int) -> int:
    ones = (lower_31_bits & 0x7FFFFFFF).bit_count()
    return 0 if ones % 2 == 1 else 1


def pack_word(label: int, data: int, sdi: int = 0, ssm: int = 0) -> int:
    if not (0 <= label <= 0xFF):
        raise ValueError("label must be 0..255")
    if not (0 <= sdi <= 0x3):
        raise ValueError("sdi must be 0..3")
    if not (0 <= data <= 0x7FFFF):
        raise ValueError("data must fit 19 bits")
    if not (0 <= ssm <= 0x3):
        raise ValueError("ssm must be 0..3")

    word = 0
    word |= label
    word |= sdi << 8
    word |= data << 10
    word |= ssm << 29
    word |= _odd_parity_bit(word) << 31
    return word


def unpack_word(word: int) -> dict:
    word &= 0xFFFFFFFF
    lower = word & 0x7FFFFFFF
    parity = (word >> 31) & 1
    valid = ((lower.bit_count() + parity) % 2) == 1
    return {
        "label": word & 0xFF,
        "sdi": (word >> 8) & 0x3,
        "data": (word >> 10) & 0x7FFFF,
        "ssm": (word >> 29) & 0x3,
        "parity": parity,
        "parity_valid": valid,
    }
