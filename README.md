# 🔐 Encryption Algorithms Suite

A professional Python GUI application implementing multiple encryption algorithms with clean architecture.

## Algorithms Supported
- Caesar Cipher
- Hill Cipher
- Vigenère Cipher
- DES (Data Encryption Standard)
- AES (Advanced Encryption Standard)

## Architecture
- **Presentation Layer** (`ui/`) — CustomTkinter GUI views
- **Business Logic Layer** (`core/`) — Algorithm implementations
- **Controller Layer** (`controllers/`) — Bridges UI and logic
- **Utilities** (`utils/`) — Shared helpers

## Run
```bash
pip install -r requirements.txt
python main.py
```
