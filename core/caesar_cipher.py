# core/caesar_cipher.py
"""
Caesar Cipher Implementation.

The Caesar cipher is a substitution cipher where each letter in the
plaintext is shifted a certain number of places down the alphabet.
"""

import random
from .base_cipher import BaseCipher, CipherResult



class CaesarCipher(BaseCipher):
    """
    Caesar Cipher — shifts each alphabetic character by a numeric key.

    Key format: An integer between 1 and 25.
    Non-alphabetic characters are preserved unchanged.
    """

    ALPHABET_SIZE = 26

    @property
    def name(self) -> str:
        return "Caesar Cipher"

    @property
    def description(self) -> str:
        return (
            "A classic substitution cipher that shifts each letter by a fixed number.\n"
            "Non-alphabetic characters remain unchanged."
        )

    @property
    def key_hint(self) -> str:
        return "Enter a number (1–25), e.g. 3"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def encrypt(self, plaintext: str, key: str) -> CipherResult:
        shift = self._parse_key(key)
        if shift is None:
            return self._make_error("Key must be an integer between 1 and 25.", "encrypt")

        result = self._shift_text(plaintext, shift)
        return self._make_success(result, "encrypt")

    def decrypt(self, ciphertext: str, key: str) -> CipherResult:
        shift = self._parse_key(key)
        if shift is None:
            return self._make_error("Key must be an integer between 1 and 25.", "decrypt")

        # Decryption is just encryption with the inverse shift
        result = self._shift_text(ciphertext, -shift)
        return self._make_success(result, "decrypt")

    def generate_key(self) -> str:
        return str(random.randint(1, 25))

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _parse_key(self, key: str):
        """Validate and parse the shift key. Returns None on failure."""
        try:
            shift = int(key.strip())
            if not (1 <= shift <= 25):
                return None
            return shift
        except ValueError:
            return None

    def _shift_text(self, text: str, shift: int) -> str:
        """Apply a shift to all alphabetic characters in the text."""
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - base + shift) % self.ALPHABET_SIZE
                result.append(chr(base + shifted))
            else:
                result.append(char)
        return "".join(result)
