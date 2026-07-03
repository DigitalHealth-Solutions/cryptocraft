# core/aes_cipher.py
"""
AES (Advanced Encryption Standard) Cipher Implementation.

Uses pycryptodome for standards-compliant AES encryption with CBC mode
and PKCS7 padding. Supports 128, 192, and 256-bit key lengths.
Output is hex-encoded.
"""

import random
import string
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from .base_cipher import BaseCipher, CipherResult



class AESCipher(BaseCipher):
    """
    AES Cipher — block cipher supporting 128, 192, or 256-bit keys.

    Key format: 16, 24, or 32 ASCII characters.
    Uses CBC mode with a zero IV for deterministic output.
    Ciphertext is represented as a hex string.
    """

    VALID_KEY_LENGTHS = {16, 24, 32}  # bytes → 128, 192, 256 bits
    BLOCK_SIZE = 16                    # bytes (128-bit block)
    IV = b'\x00' * 16                 # fixed zero IV for simplicity

    @property
    def name(self) -> str:
        return "AES"

    @property
    def description(self) -> str:
        return (
            "Advanced Encryption Standard — the gold standard of symmetric encryption.\n"
            "Supports 128, 192, or 256-bit keys in CBC mode. Output is hex-encoded."
        )

    @property
    def key_hint(self) -> str:
        return "Enter 16, 24, or 32 characters (128/192/256-bit key)"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def encrypt(self, plaintext: str, key: str) -> CipherResult:
        key_bytes, error = self._validate_and_encode_key(key)
        if error:
            return self._make_error(error, "encrypt")

        try:
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv=self.IV)
            padded_data = pad(plaintext.encode("utf-8"), self.BLOCK_SIZE)
            encrypted = cipher.encrypt(padded_data)
            hex_output = binascii.hexlify(encrypted).decode("utf-8").upper()
            return self._make_success(hex_output, "encrypt")
        except Exception as exc:
            return self._make_error(f"AES encryption failed: {exc}", "encrypt")

    def decrypt(self, ciphertext: str, key: str) -> CipherResult:
        key_bytes, error = self._validate_and_encode_key(key)
        if error:
            return self._make_error(error, "decrypt")

        try:
            raw_bytes = binascii.unhexlify(ciphertext.strip())
        except (binascii.Error, ValueError):
            return self._make_error(
                "Ciphertext must be a valid hex string (from AES encryption output).",
                "decrypt",
            )

        try:
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv=self.IV)
            decrypted_padded = cipher.decrypt(raw_bytes)
            decrypted = unpad(decrypted_padded, self.BLOCK_SIZE).decode("utf-8")
            return self._make_success(decrypted, "decrypt")
        except Exception as exc:
            return self._make_error(f"AES decryption failed: {exc}", "decrypt")

    def generate_key(self) -> str:
        # Default to a strong 256-bit key (32 alphanumeric characters)
        return "".join(random.choices(string.ascii_letters + string.digits, k=32))

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _validate_and_encode_key(self, key: str):
        """
        Validate and encode the AES key.

        Returns:
            Tuple of (key_bytes, error_message). error is None on success.
        """
        key_bytes = key.encode("utf-8")
        if len(key_bytes) not in self.VALID_KEY_LENGTHS:
            return None, (
                f"AES key must be 16, 24, or 32 characters. Got {len(key_bytes)}. "
                "Pad or shorten your key."
            )
        return key_bytes, None
