import pytest

from tablette.publier.crypto import chiffrer, dechiffrer


def test_aller_retour():
    env = chiffrer(b'{"a":1}', "4821")
    assert set(env) == {"v", "iter", "sel", "iv", "ct"}
    assert env["v"] == 1 and env["iter"] == 100_000
    assert dechiffrer(env, "4821") == b'{"a":1}'


def test_sel_et_iv_aleatoires():
    a, b = chiffrer(b"x", "1"), chiffrer(b"x", "1")
    assert a["sel"] != b["sel"] and a["iv"] != b["iv"]


def test_mauvais_pin():
    with pytest.raises(ValueError, match="PIN incorrect"):
        dechiffrer(chiffrer(b"x", "1111"), "2222")
