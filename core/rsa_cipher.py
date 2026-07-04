# core/rsa_cipher.py
"""
RSA (Rivest–Shamir–Adleman) Cipher Implementation.

RSA is an asymmetric (public-key) cryptography algorithm.
Encryption is done with the PUBLIC key; decryption with the PRIVATE key.

Key format used in this app:
  A single string containing both keys separated by '|||':
  "<public_key_b64>|||<private_key_b64>"

  This combined format is returned by generate_key() and stored in the
  single key field, allowing the app to extract the appropriate key
  for each operation without needing separate input fields.

  Output of encryption is Base64-encoded binary ciphertext.
"""

import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from .base_cipher import BaseCipher, CipherResult


class RSACipher(BaseCipher):
    """
    RSA Cipher — asymmetric public-key cryptography.

    Key format: A combined Base64 string produced by the ⚡ Generate button.
    Encryption uses the embedded public key.
    Decryption uses the embedded private key.
    Output is Base64-encoded.
    """

    KEY_SIZE  = 2048          # bits — industry standard for good security
    SEPARATOR = "|||"         # delimiter between public and private key in the combined string

    # ------------------------------------------------------------------
    # BaseCipher interface properties
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        return "RSA"

    @property
    def description(self) -> str:
        return (
            "Asymmetric public-key encryption (2048-bit).\n"
            "Click ⚡ Generate to create a key pair, then Encrypt or Decrypt."
        )

    @property
    def key_hint(self) -> str:
        return "Click ⚡ Generate to create a 2048-bit RSA key pair automatically."

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def encrypt(self, plaintext: str, key: str) -> CipherResult:
        """Encrypt plaintext using the public key embedded in the combined key string."""
        public_key, error = self._extract_public_key(key)
        if error:
            return self._make_error(error, "encrypt")

        try:
            cipher = PKCS1_OAEP.new(public_key)
            encrypted_bytes = cipher.encrypt(plaintext.encode("utf-8"))
            b64_output = base64.b64encode(encrypted_bytes).decode("ascii")
            return self._make_success(b64_output, "encrypt")
        except ValueError as exc:
            return self._make_error(
                f"Plaintext too long for RSA-2048 (max ~214 bytes). Error: {exc}",
                "encrypt",
            )
        except Exception as exc:
            return self._make_error(f"RSA encryption failed: {exc}", "encrypt")

    def decrypt(self, ciphertext: str, key: str) -> CipherResult:
        """Decrypt Base64 ciphertext using the private key embedded in the combined key string."""
        private_key, error = self._extract_private_key(key)
        if error:
            return self._make_error(error, "decrypt")

        try:
            raw_bytes = base64.b64decode(ciphertext.strip())
        except Exception:
            return self._make_error(
                "Ciphertext must be valid Base64 (output from RSA encryption).",
                "decrypt",
            )

        try:
            cipher = PKCS1_OAEP.new(private_key)
            decrypted_bytes = cipher.decrypt(raw_bytes)
            return self._make_success(decrypted_bytes.decode("utf-8"), "decrypt")
        except Exception as exc:
            return self._make_error(f"RSA decryption failed: {exc}", "decrypt")

    def generate_key(self) -> str:
        """
        Generate a 2048-bit RSA key pair.

        Returns a combined string:
          "<public_key_base64>|||<private_key_base64>"

        Both keys are stored together so the single key field can be used
        for both encryption (public key is extracted automatically) and
        decryption (private key is extracted automatically).

        Key generation may take 1-2 seconds — RSA involves finding large primes.
        """
        rsa_key = RSA.generate(self.KEY_SIZE)

        private_pem = rsa_key.export_key().decode("ascii")
        public_pem  = rsa_key.publickey().export_key().decode("ascii")

        private_b64 = base64.b64encode(private_pem.encode()).decode("ascii")
        public_b64  = base64.b64encode(public_pem.encode()).decode("ascii")

        return f"{public_b64}{self.SEPARATOR}{private_b64}"

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _split_combined_key(self, key: str):
        """
        Split the combined key string into its public and private components.
        Returns (public_b64, private_b64, error_message).
        """
        parts = key.strip().split(self.SEPARATOR)
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return None, None, (
                "Invalid key format. Use the ⚡ Generate button to create a valid RSA key pair."
            )
        return parts[0], parts[1], None

    def _extract_public_key(self, key: str):
        """
        Parse and return the RSA public key object from the combined key string.
        Returns (RSA_key_object, error_message).
        """
        public_b64, _, error = self._split_combined_key(key)
        if error:
            return None, error
        try:
            public_pem = base64.b64decode(public_b64).decode("ascii")
            return RSA.import_key(public_pem), None
        except Exception:
            return None, "Could not parse the public key. Use the ⚡ Generate button."

    def _extract_private_key(self, key: str):
        """
        Parse and return the RSA private key object from the combined key string.
        Returns (RSA_key_object, error_message).
        """
        _, private_b64, error = self._split_combined_key(key)
        if error:
            return None, error
        try:
            private_pem = base64.b64decode(private_b64).decode("ascii")
            return RSA.import_key(private_pem), None
        except Exception:
            return None, "Could not parse the private key. Use the ⚡ Generate button."
