# controllers/cipher_controller.py
"""
CipherController — the single point of coordination between UI and core logic.

Responsibilities:
  - Maintain the cipher registry (algorithm name → BaseCipher instance)
  - Dispatch encrypt/decrypt requests to the correct cipher
  - Return CipherResult objects back to the UI without leaking implementation details
"""

from typing import Dict, List, Optional

from core import (
    BaseCipher,
    CaesarCipher,
    VigenereCipher,
    HillCipher,
    DESCipher,
    AESCipher,
    RSACipher,
)
from core.base_cipher import CipherResult


class CipherController:
    """
    Controller that manages cipher instances and routes operations.

    The UI layer only ever calls this controller — it never imports
    from the core package directly.
    """

    def __init__(self) -> None:
        # Registry: display name → cipher instance
        self._registry: Dict[str, BaseCipher] = self._build_registry()
        self._active_cipher_name: Optional[str] = None

    # ------------------------------------------------------------------
    # Registry management
    # ------------------------------------------------------------------

    def _build_registry(self) -> Dict[str, BaseCipher]:
        """Instantiate and register all available cipher algorithms."""
        ciphers = [
            CaesarCipher(),
            VigenereCipher(),
            HillCipher(),
            DESCipher(),
            AESCipher(),
            RSACipher(),
        ]
        return {cipher.name: cipher for cipher in ciphers}

    def get_algorithm_names(self) -> List[str]:
        """Return an ordered list of available algorithm names."""
        return list(self._registry.keys())

    def select_algorithm(self, name: str) -> bool:
        """
        Set the active cipher by name.

        Returns:
            True if the algorithm was found and selected, False otherwise.
        """
        if name in self._registry:
            self._active_cipher_name = name
            return True
        return False

    @property
    def active_cipher(self) -> Optional[BaseCipher]:
        """Return the currently selected cipher instance, or None."""
        if self._active_cipher_name:
            return self._registry[self._active_cipher_name]
        return None

    # ------------------------------------------------------------------
    # Operation dispatch
    # ------------------------------------------------------------------

    def encrypt(self, plaintext: str, key: str) -> CipherResult:
        """
        Encrypt plaintext using the active cipher.

        Returns a CipherResult regardless of success or failure.
        """
        cipher = self._get_active_or_error("encrypt")
        if isinstance(cipher, CipherResult):
            return cipher
        return cipher.encrypt(plaintext, key)

    def decrypt(self, ciphertext: str, key: str) -> CipherResult:
        """
        Decrypt ciphertext using the active cipher.

        Returns a CipherResult regardless of success or failure.
        """
        cipher = self._get_active_or_error("decrypt")
        if isinstance(cipher, CipherResult):
            return cipher
        return cipher.decrypt(ciphertext, key)

    # ------------------------------------------------------------------
    # Metadata accessors (UI helpers)
    # ------------------------------------------------------------------

    def get_active_key_hint(self) -> str:
        """Return the key format hint for the active cipher."""
        cipher = self.active_cipher
        return cipher.key_hint if cipher else "Select an algorithm first."

    def get_active_description(self) -> str:
        """Return the description of the active cipher."""
        cipher = self.active_cipher
        return cipher.description if cipher else ""

    def get_active_name(self) -> str:
        """Return the name of the active cipher."""
        return self._active_cipher_name or "None"

    def generate_active_key(self) -> str:
        """Generate a valid key for the currently selected cipher. Returns empty if none active."""
        cipher = self.active_cipher
        return cipher.generate_key() if cipher else ""

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_active_or_error(self, operation: str):
        """Return the active cipher, or a CipherResult error if none is selected."""
        if not self.active_cipher:
            return CipherResult(
                success=False,
                output="",
                error_message="No algorithm selected. Please choose a cipher first.",
                algorithm_name="None",
                operation=operation,
            )
        return self.active_cipher
