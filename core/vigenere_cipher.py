# core/vigenere_cipher.py
"""
Vigenère Cipher Implementation.

The Vigenère cipher uses a keyword to apply multiple Caesar shifts,
cycling through the keyword characters for each letter in the plaintext.
"""

import random
import string
from .base_cipher import BaseCipher, CipherResult



class VigenereCipher(BaseCipher):
    """
    Vigenère Cipher — uses a repeating keyword to shift each letter.

    Key format: An alphabetic string (e.g., 'SECRET').
    Non-alphabetic characters in plaintext are preserved unchanged.
    """

    ALPHABET_SIZE = 26

    @property
    def name(self) -> str:
        return "Vigenère Cipher"

    @property
    def description(self) -> str:
        return (
            "A polyalphabetic cipher using a keyword to shift letters.\n"
            "Each letter is shifted by the corresponding keyword letter's position."
        )

    @property
    def key_hint(self) -> str:
        return "Enter an alphabetic keyword, e.g. SECRET"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def encrypt(self, plaintext: str, key: str) -> CipherResult:
        sanitized_key = self._sanitize_key(key)
        if not sanitized_key:
            return self._make_error(
                "Key must contain at least one alphabetic character.", "encrypt"
            )
        result = self._process(plaintext, sanitized_key, mode="encrypt")
        return self._make_success(result, "encrypt")

    def decrypt(self, ciphertext: str, key: str) -> CipherResult:
        sanitized_key = self._sanitize_key(key)
        if not sanitized_key:
            return self._make_error(
                "Key must contain at least one alphabetic character.", "decrypt"
            )
        result = self._process(ciphertext, sanitized_key, mode="decrypt")
        return self._make_success(result, "decrypt")

    def generate_key(self) -> str:
        length = random.randint(6, 10)
        return "".join(random.choices(string.ascii_uppercase, k=length))

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _sanitize_key(self, key: str) -> str:
        """Strip non-alpha characters and uppercase the key."""
        return "".join(c.upper() for c in key if c.isalpha())

    def _process(self, text: str, key: str, mode: str) -> str:
        """
        Apply Vigenère transformation.

        Args:
            text: Input text.
            key: Sanitized uppercase alphabetic key.
            mode: 'encrypt' or 'decrypt'.
        """
        result = []
        key_index = 0

        for char in text:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)]) - ord('A')
                base = ord('A') if char.isupper() else ord('a')
                char_offset = ord(char) - base

                if mode == "encrypt":
                    shifted = (char_offset + key_shift) % self.ALPHABET_SIZE
                else:
                    shifted = (char_offset - key_shift) % self.ALPHABET_SIZE

                result.append(chr(base + shifted))
                key_index += 1
            else:
                result.append(char)

        return "".join(result)
