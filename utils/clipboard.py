# utils/clipboard.py
"""
Cross-platform clipboard utility.
Abstracts away tkinter clipboard access.
"""

import tkinter as tk


def copy_to_clipboard(root: tk.Tk, text: str) -> None:
    """
    Copy text to the system clipboard using the tkinter root window.

    Args:
        root: The root Tk window (needed to access the clipboard).
        text: The text to copy.
    """
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Required for clipboard to persist after window closes
