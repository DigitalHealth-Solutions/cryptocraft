# core/base_cipher.py
"""
Abstract base class for all cipher implementations.
Enforces the interface contract using ABC.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class CipherResult:
    """
    Immutable result object returned from every cipher operation.
    Separates success/failure data cleanly.
    """
    success: bool
    output: str
    error_message: Optional[str] = None
    algorithm_name: str = ""
    operation: str = ""  # 'encrypt' | 'decrypt'

    def __str__(self) -> str:
        if self.success:
            return f"[{self.algorithm_name}] {self.operation.capitalize()}: {self.output}"
        return f"[{self.algorithm_name}] Error: {self.error_message}"


class BaseCipher(ABC):
    """
    Abstract base class for all cipher implementations.

    Every cipher must implement encrypt() and decrypt(),
    and provide metadata like name, description, and key_hint.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the cipher."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Short description of the cipher."""
        ...

    @property
    @abstractmethod
    def key_hint(self) -> str:
        """Hint shown to the user explaining the expected key format."""
        ...

    @abstractmethod
    def encrypt(self, plaintext: str, key: str) -> CipherResult:
        """
        Encrypt plaintext using the given key.

        Args:
            plaintext: The text to encrypt.
            key: The encryption key (format depends on cipher).

        Returns:
            CipherResult with success status and encrypted output.
        """
        ...

    @abstractmethod
    def decrypt(self, ciphertext: str, key: str) -> CipherResult:
        """
        Decrypt ciphertext using the given key.

        Args:
            ciphertext: The text to decrypt.
            key: The decryption key (format depends on cipher).

        Returns:
            CipherResult with success status and decrypted output.
        """
        ...

    @abstractmethod
    def generate_key(self) -> str:
        """
        Generate a random, mathematically valid key for this cipher.

        Returns:
            A string representation of the generated key.
        """
        ...

    def _make_success(self, output: str, operation: str) -> CipherResult:
        """Factory method for successful results."""
        return CipherResult(
            success=True,
            output=output,
            algorithm_name=self.name,
            operation=operation,
        )

    def _make_error(self, message: str, operation: str) -> CipherResult:
        """Factory method for error results."""
        return CipherResult(
            success=False,
            output="",
            error_message=message,
            algorithm_name=self.name,
            operation=operation,
        )
