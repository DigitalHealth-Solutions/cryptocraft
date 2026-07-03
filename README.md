# Encryption Algorithms Suite

A professional Python GUI desktop application implementing multiple classical and modern encryption algorithms with clean, decoupled architecture.

Developed by: **Mohannad Al-Majidi**

## Key Features
- **Clean Architecture:** Strict separation between user interface views, controller coordinators, and core mathematical/cryptographic logic.
- **Theme Customizer:** Smooth, native switching between Light Mode and Dark Mode with custom-designed palettes.
- **Smart Key Generator:** Dynamically generates cryptographically/mathematically valid keys depending on the chosen algorithm.
- **Fault Tolerance:** Safe input validation and custom result-wrapper encapsulation to prevent execution-time crashes.

## Supported Algorithms
- **Caesar Cipher:** Shifts alphabetic characters by a configurable integer key (1-25).
- **Vigenere Cipher:** Polyalphabetic substitution using an alphabetic keyword.
- **Hill Cipher:** Matrix multiplication modulo 26, using an invertible 2x2 matrix as the key.
- **DES (Data Encryption Standard):** Symmetric 64-bit block cipher utilizing CBC mode with an 8-character ASCII key and hexadecimal output.
- **AES (Advanced Encryption Standard):** High-security block cipher using CBC mode with a 32-character (256-bit) ASCII key and hexadecimal output.

## Architecture Directory Structure
```
├── main.py                          # Application entry point
├── requirements.txt                 # Dependencies
├── core/                            # Business Logic Layer (Pure algorithms)
│   ├── base_cipher.py               # Abstract Base Class and CipherResult definitions
│   ├── caesar_cipher.py
│   ├── vigenere_cipher.py
│   ├── hill_cipher.py
│   ├── des_cipher.py
│   └── aes_cipher.py
├── controllers/                     # Controller Layer (Coordinates UI and Core)
│   └── cipher_controller.py
├── ui/                              # Presentation Layer (Views and Custom Widgets)
│   ├── app_window.py                # Main orchestrator window
│   ├── views/
│   │   ├── selection_view.py        # Algorithm choosing screen
│   │   └── cipher_view.py           # Workspace and execution interface
│   └── widgets/
│       └── algorithm_card.py        # Custom selection card component
└── utils/                           # Shared Utilities
    ├── theme.py                     # Light and Dark design tokens
    └── clipboard.py                 # Cross-platform copy helper
```

## Installation & Setup

### Prerequisites
- Python 3.12 or higher

### Install Dependencies
Run the following command to install the required libraries:
```bash
pip install -r requirements.txt
```

### Run the Application
Start the program by executing:
```bash
python main.py
```

## License
Licensed under the MIT License.
