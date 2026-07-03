# main.py
"""
Entry point for the Encryption Algorithms Suite.

Usage:
    python main.py

Architecture summary:
    main.py
    └── ui/app_window.py (AppWindow)
        ├── controllers/cipher_controller.py (CipherController)
        │   └── core/ (BaseCipher implementations)
        ├── ui/views/selection_view.py (SelectionView)
        ├── ui/views/cipher_view.py (CipherView)
        └── utils/ (AppTheme, clipboard)
"""

import sys
import os

# Ensure the project root is in sys.path so all packages resolve correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app_window import AppWindow


def main() -> None:
    """Create and run the application."""
    app = AppWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
