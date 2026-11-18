"""Chiffrement du tableau de bord : AES-GCM 256, clé dérivée du PIN par PBKDF2-SHA256.

Format compatible WebCrypto : `ct` = chiffré + tag GCM concaténés.
"""
import base64
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERATIONS = 100_000


def _cle(pin: str, sel: bytes, iterations: int) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=sel, iterations=iterations)
    return kdf.derive(pin.encode("utf-8"))


def _b64(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


def chiffrer(clair: bytes, pin: str, iterations: int = ITERATIONS) -> dict:
    sel, iv = os.urandom(16), os.urandom(12)
    ct = AESGCM(_cle(pin, sel, iterations)).encrypt(iv, clair, None)
    return {"v": 1, "iter": iterations, "sel": _b64(sel), "iv": _b64(iv), "ct": _b64(ct)}


def dechiffrer(enveloppe: dict, pin: str) -> bytes:
    sel = base64.b64decode(enveloppe["sel"])
    iv = base64.b64decode(enveloppe["iv"])
    ct = base64.b64decode(enveloppe["ct"])
    try:
        return AESGCM(_cle(pin, sel, enveloppe["iter"])).decrypt(iv, ct, None)
    except InvalidTag:
        raise ValueError("PIN incorrect") from None
