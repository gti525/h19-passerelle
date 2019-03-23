import pytest

from app.utils.aes import decrypt, encrypt


class TestAES(object):

    @pytest.mark.parametrize("text", [
        ("Je suis le plus grand"),
        ("I currently have 4 windows open up… and I don’t know why."),
        ("Everyone was busy, so I went to the movie alone."),
        ("She only paints with bold colors; she does not like pastels"),
        ("He didn’t want to go to the dentist, yet he went anyway."),
        (1232)
    ])
    def test_encryption(self, text):
        assert text == decrypt(encrypt(text))
