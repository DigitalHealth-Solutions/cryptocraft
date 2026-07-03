# core/des_cipher.py
"""
DES (Data Encryption Standard) Cipher Implementation.

Uses the pycryptodome library for standards-compliant DES encryption
with CBC mode and PKCS7 padding. Output is represented as hex string.
"""

import random
import string
import binascii
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

from .base_cipher import BaseCipher, CipherResult



class DESCipher(BaseCipher):
    """
    DES Cipher — 64-bit block cipher with 56-bit effective key.

    Key format: Exactly 8 ASCII characters (64 bits).
    Uses CBC mode with a zero IV for deterministic output.
    Ciphertext is represented as a hex string.
    """

    KEY_LENGTH = 8       # bytes (64-bit key)
    BLOCK_SIZE = 8       # bytes (64-bit block)
    IV = b'\x00' * 8    # fixed zero IV for simplicity

    @property
    def name(self) -> str:
        return "DES"

    @property
    def description(self) -> str:
        return (
            "Data Encryption Standard — a symmetric-key block cipher.\n"
            "Uses 8-character (64-bit) key in CBC mode. Output is hex-encoded."
        )

    @property
    def key_hint(self) -> str:
        return "Enter exactly 8 characters, e.g. MySecret"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def encrypt(self, plaintext: str, key: str) -> CipherResult:
        key_bytes, error = self._validate_and_encode_key(key)
        if error:
            return self._make_error(error, "encrypt")

        try:
            cipher = DES.new(key_bytes, DES.MODE_CBC, iv=self.IV)
            padded_data = pad(plaintext.encode("utf-8"), self.BLOCK_SIZE)
            encrypted = cipher.encrypt(padded_data)
            hex_output = binascii.hexlify(encrypted).decode("utf-8").upper()
            return self._make_success(hex_output, "encrypt")
        except Exception as exc:
            return self._make_error(f"DES encryption failed: {exc}", "encrypt")

    def decrypt(self, ciphertext: str, key: str) -> CipherResult:
        key_bytes, error = self._validate_and_encode_key(key)
        if error:
            return self._make_error(error, "decrypt")

        try:
            raw_bytes = binascii.unhexlify(ciphertext.strip())
        except (binascii.Error, ValueError):
            return self._make_error(
                "Ciphertext must be a valid hex string (from DES encryption output).",
                "decrypt",
            )

        try:
            cipher = DES.new(key_bytes, DES.MODE_CBC, iv=self.IV)
            decrypted_padded = cipher.decrypt(raw_bytes)
            decrypted = unpad(decrypted_padded, self.BLOCK_SIZE).decode("utf-8")
            return self._make_success(decrypted, "decrypt")
        except Exception as exc:
            return self._make_error(f"DES decryption failed: {exc}", "decrypt")

    def generate_key(self) -> str:
        # Generate 8 random alphanumeric characters
        return "".join(random.choices(string.ascii_letters + string.digits, k=self.KEY_LENGTH))

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _validate_and_encode_key(self, key: str):
        """
        Validate and encode the DES key.

        Returns:
            Tuple of (key_bytes, error_message). error is None on success.
        """
        if len(key) != self.KEY_LENGTH:
            return None, f"DES key must be exactly {self.KEY_LENGTH} characters (got {len(key)})."
        return key.encode("utf-8"), None
