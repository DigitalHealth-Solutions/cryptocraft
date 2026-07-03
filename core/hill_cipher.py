# core/hill_cipher.py
"""
Hill Cipher Implementation.

The Hill cipher is a polygraphic substitution cipher that uses
linear algebra (matrix multiplication mod 26) for encryption.
"""

import random
import numpy as np
from .base_cipher import BaseCipher, CipherResult



class HillCipher(BaseCipher):
    """
    Hill Cipher — uses an n×n invertible matrix as the key.

    Key format: Space-separated integers representing a square matrix,
    row by row (e.g., '6 24 1 13 16 10 20 17 15' for a 3×3 matrix).

    Only alphabetic characters are processed; punctuation is dropped
    during encryption (Hill cipher operates on block-grouped letters).
    """

    MOD = 26

    @property
    def name(self) -> str:
        return "Hill Cipher"

    @property
    def description(self) -> str:
        return (
            "A polygraphic cipher using matrix multiplication modulo 26.\n"
            "Key must be an invertible square matrix (2×2 or 3×3 recommended)."
        )

    @property
    def key_hint(self) -> str:
        return "Enter matrix values row-by-row, e.g. for 2×2: 6 24 1 13"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def encrypt(self, plaintext: str, key: str) -> CipherResult:
        key_matrix, error = self._parse_key_matrix(key)
        if error:
            return self._make_error(error, "encrypt")

        letters = self._extract_letters(plaintext).upper()
        if not letters:
            return self._make_error("Plaintext must contain at least one alphabetic character.", "encrypt")

        n = key_matrix.shape[0]
        padded = self._pad_text(letters, n)
        result = self._apply_matrix(padded, key_matrix, n)
        return self._make_success(result, "encrypt")

    def decrypt(self, ciphertext: str, key: str) -> CipherResult:
        key_matrix, error = self._parse_key_matrix(key)
        if error:
            return self._make_error(error, "decrypt")

        letters = self._extract_letters(ciphertext).upper()
        if not letters:
            return self._make_error("Ciphertext must contain at least one alphabetic character.", "decrypt")

        n = key_matrix.shape[0]
        inv_matrix, inv_error = self._matrix_mod_inverse(key_matrix, n)
        if inv_error:
            return self._make_error(inv_error, "decrypt")

        result = self._apply_matrix(letters, inv_matrix, n)
        return self._make_success(result, "decrypt")

    def generate_key(self) -> str:
        """
        Generate a random, invertible 2x2 matrix mod 26.
        An invertible key ensures encryption and decryption will work.
        """
        while True:
            # Generate random 4 integers for a 2x2 matrix
            values = [random.randint(0, 25) for _ in range(4)]
            matrix = np.array(values).reshape(2, 2)
            det = int(round(np.linalg.det(matrix))) % self.MOD
            
            # Check determinant is non-zero and coprime with 26
            if det != 0 and self._gcd(det, self.MOD) == 1:
                return " ".join(map(str, values))

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _parse_key_matrix(self, key: str):
        """
        Parse and validate the key into a numpy matrix.

        Returns:
            Tuple of (matrix, error_message). error_message is None on success.
        """
        try:
            values = list(map(int, key.strip().split()))
        except ValueError:
            return None, "Key must be space-separated integers."

        n = int(len(values) ** 0.5)
        if n * n != len(values) or n < 2:
            return None, "Key must have n² integers forming a square matrix (n ≥ 2)."

        matrix = np.array(values).reshape(n, n) % self.MOD

        # Check determinant is non-zero and coprime with 26
        det = int(round(np.linalg.det(matrix))) % self.MOD
        if det == 0 or self._gcd(det, self.MOD) != 1:
            return None, (
                f"Matrix determinant ({det}) must be non-zero and coprime with 26. "
                "Please choose a different key matrix."
            )

        return matrix, None

    def _matrix_mod_inverse(self, matrix: np.ndarray, n: int):
        """Compute the modular inverse of a matrix mod 26."""
        det = int(round(np.linalg.det(matrix))) % self.MOD
        det_inv = self._mod_inverse(det, self.MOD)
        if det_inv is None:
            return None, "Matrix is not invertible mod 26."

        adjugate = (np.round(np.linalg.det(matrix) * np.linalg.inv(matrix))
                    .astype(int) % self.MOD)
        inv_matrix = (det_inv * adjugate) % self.MOD
        return inv_matrix.astype(int), None

    def _apply_matrix(self, text: str, matrix: np.ndarray, n: int) -> str:
        """Apply matrix multiplication to blocks of n letters."""
        result = []
        for i in range(0, len(text), n):
            block = [ord(c) - ord('A') for c in text[i:i + n]]
            block_vector = np.array(block)
            encrypted_vector = (matrix @ block_vector) % self.MOD
            result.extend(chr(int(v) + ord('A')) for v in encrypted_vector)
        return "".join(result)

    def _extract_letters(self, text: str) -> str:
        """Keep only alphabetic characters."""
        return "".join(c for c in text if c.isalpha())

    def _pad_text(self, text: str, block_size: int) -> str:
        """Pad text with 'X' to make it divisible by block_size."""
        remainder = len(text) % block_size
        if remainder:
            text += 'X' * (block_size - remainder)
        return text

    def _gcd(self, a: int, b: int) -> int:
        """Compute greatest common divisor."""
        while b:
            a, b = b, a % b
        return a

    def _mod_inverse(self, a: int, m: int):
        """Extended Euclidean algorithm to find modular inverse."""
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None
