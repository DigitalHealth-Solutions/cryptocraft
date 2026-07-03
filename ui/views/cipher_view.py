# ui/views/cipher_view.py
"""
CipherView — main encryption/decryption workspace.

Shown after the user selects an algorithm from SelectionView.
"""

import customtkinter as ctk
from typing import Callable

from utils.theme import AppTheme


class CipherView(ctk.CTkFrame):
    """
    Workspace panel for encrypting and decrypting text.

    Contains:
      - Algorithm info header with badge
      - Key input field with hint
      - Plaintext / ciphertext input area
      - Encrypt / Decrypt action buttons
      - Output display with copy button
      - Back navigation button
    """

    def __init__(
        self,
        parent,
        on_encrypt: Callable[[str, str], None],
        on_decrypt: Callable[[str, str], None],
        on_back: Callable[[], None],
        on_copy: Callable[[str], None],
        on_generate_key: Callable[[], str],
        on_toggle_theme: Callable[[], None],
        theme: AppTheme,
        **kwargs,
    ) -> None:
        super().__init__(parent, fg_color="transparent", **kwargs)

        self._theme = theme
        self._on_encrypt = on_encrypt
        self._on_decrypt = on_decrypt
        self._on_back = on_back
        self._on_copy = on_copy
        self._on_generate_key = on_generate_key
        self._on_toggle_theme = on_toggle_theme

        self._build_ui()

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Assemble the cipher workspace layout."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self._build_top_bar()
        self._build_algorithm_info()
        self._build_input_section()
        self._build_output_section()

    def _build_top_bar(self) -> None:
        """Back button + title bar + theme toggle."""
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 0))

        ctk.CTkButton(
            bar,
            text="← Back",
            font=ctk.CTkFont(family=self._theme.font_family, size=self._theme.font_size_base),
            fg_color=self._theme.bg_surface,
            hover_color=self._theme.bg_hover,
            text_color=self._theme.text_secondary,
            corner_radius=8,
            width=90,
            height=36,
            command=self._on_back,
        ).pack(side="left")

        self._page_title = ctk.CTkLabel(
            bar,
            text="",
            font=ctk.CTkFont(
                family=self._theme.font_family,
                size=self._theme.font_size_xl,
                weight="bold",
            ),
            text_color=self._theme.text_primary,
        )
        self._page_title.pack(side="left", padx=20)

        # Theme toggle button
        self._theme_btn = ctk.CTkButton(
            bar,
            text="☀️ / 🌙",
            font=ctk.CTkFont(size=self._theme.font_size_base),
            fg_color=self._theme.bg_surface,
            hover_color=self._theme.bg_hover,
            text_color=self._theme.text_primary,
            width=50,
            height=36,
            corner_radius=8,
            command=self._on_toggle_theme,
        )
        self._theme_btn.pack(side="right")

    def _build_algorithm_info(self) -> None:
        """Algorithm badge, name, and description card."""
        card = ctk.CTkFrame(
            self,
            fg_color=self._theme.bg_secondary,
            corner_radius=self._theme.border_radius,
            border_width=1,
            border_color=self._theme.border_color,
        )
        card.grid(row=1, column=0, sticky="ew", padx=32, pady=(16, 0))
        card.grid_columnconfigure(1, weight=1)

        # Colored circle badge
        self._badge = ctk.CTkLabel(
            card,
            text="●",
            font=ctk.CTkFont(size=28),
            text_color=self._theme.accent_primary,
            width=50,
        )
        self._badge.grid(row=0, column=0, rowspan=2, padx=(20, 0), pady=16)

        self._algo_name_lbl = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(
                family=self._theme.font_family,
                size=self._theme.font_size_lg,
                weight="bold",
            ),
            text_color=self._theme.text_primary,
            anchor="w",
        )
        self._algo_name_lbl.grid(row=0, column=1, sticky="w", padx=(12, 20), pady=(16, 2))

        self._algo_desc_lbl = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(
                family=self._theme.font_family,
                size=self._theme.font_size_sm,
            ),
            text_color=self._theme.text_secondary,
            anchor="w",
            wraplength=600,
            justify="left",
        )
        self._algo_desc_lbl.grid(row=1, column=1, sticky="w", padx=(12, 20), pady=(0, 16))

    def _build_input_section(self) -> None:
        """Key input and text area inputs."""
        section = ctk.CTkFrame(self, fg_color="transparent")
        section.grid(row=2, column=0, sticky="ew", padx=32, pady=(20, 0))
        section.grid_columnconfigure((0, 1), weight=1)

        # Left column: Key input
        key_col = ctk.CTkFrame(section, fg_color="transparent")
        key_col.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        key_col.grid_columnconfigure(0, weight=1)

        self._make_label(key_col, "🔑  Encryption Key").pack(anchor="w", pady=(0, 6))

        # Horizontal container for entry and generate button
        key_row = ctk.CTkFrame(key_col, fg_color="transparent")
        key_row.pack(fill="x")

        self._key_entry = ctk.CTkEntry(
            key_row,
            placeholder_text="Enter key...",
            font=ctk.CTkFont(family=self._theme.font_family, size=self._theme.font_size_base),
            fg_color=self._theme.bg_surface,
            border_color=self._theme.border_color,
            text_color=self._theme.text_primary,
            placeholder_text_color=self._theme.text_muted,
            corner_radius=10,
            height=44,
        )
        self._key_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self._generate_btn = ctk.CTkButton(
            key_row,
            text="⚡ Generate",
            font=ctk.CTkFont(family=self._theme.font_family, size=self._theme.font_size_sm, weight="bold"),
            fg_color=self._theme.accent_primary,
            hover_color=self._theme.accent_secondary,
            text_color=self._theme.text_primary,
            corner_radius=10,
            width=100,
            height=44,
            command=self._handle_generate_key,
        )
        self._generate_btn.pack(side="right")

        self._key_hint_lbl = ctk.CTkLabel(
            key_col,
            text="",
            font=ctk.CTkFont(
                family=self._theme.font_family,
                size=self._theme.font_size_xs,
                slant="italic",
            ),
            text_color=self._theme.accent_info,
            anchor="w",
        )
        self._key_hint_lbl.pack(anchor="w", pady=(4, 0))

        # Right column: Input text
        text_col = ctk.CTkFrame(section, fg_color="transparent")
        text_col.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        text_col.grid_columnconfigure(0, weight=1)

        self._make_label(text_col, "📝  Input Text").pack(anchor="w", pady=(0, 6))

        self._input_text = ctk.CTkTextbox(
            text_col,
            font=ctk.CTkFont(family="Consolas", size=self._theme.font_size_base),
            fg_color=self._theme.bg_surface,
            border_color=self._theme.border_color,
            text_color=self._theme.text_primary,
            corner_radius=10,
            border_width=1,
            height=110,
            wrap="word",
        )
        self._input_text.pack(fill="x")

        # Action buttons row
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.grid(row=3, column=0, sticky="ew", padx=32, pady=(16, 0))

        self._encrypt_btn = ctk.CTkButton(
            btn_row,
            text="⚡  Encrypt",
            font=ctk.CTkFont(
                family=self._theme.font_family,
                size=self._theme.font_size_base,
                weight="bold",
            ),
            fg_color=self._theme.accent_success,
            hover_color="#2DBD8B",
            text_color="#0D0F1A",
            corner_radius=self._theme.border_radius,
            height=46,
            command=self._handle_encrypt,
        )
        self._encrypt_btn.pack(side="left", expand=True, fill="x", padx=(0, 8))

        self._decrypt_btn = ctk.CTkButton(
            btn_row,
            text="🔓  Decrypt",
            font=ctk.CTkFont(
                family=self._theme.font_family,
                size=self._theme.font_size_base,
                weight="bold",
            ),
            fg_color=self._theme.accent_warning,
            hover_color="#E5A91C",
            text_color="#0D0F1A",
            corner_radius=self._theme.border_radius,
            height=46,
            command=self._handle_decrypt,
        )
        self._decrypt_btn.pack(side="left", expand=True, fill="x", padx=(8, 0))

    def _build_output_section(self) -> None:
        """Output area with status badge and copy button."""
        output_frame = ctk.CTkFrame(
            self,
            fg_color=self._theme.bg_secondary,
            corner_radius=self._theme.border_radius,
            border_width=1,
            border_color=self._theme.border_color,
        )
        output_frame.grid(row=4, column=0, sticky="nsew", padx=32, pady=(16, 32))
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(1, weight=1)

        # Output header
        header = ctk.CTkFrame(output_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 0))

        self._output_label = ctk.CTkLabel(
            header,
            text="📤  Output",
            font=ctk.CTkFont(
                family=self._theme.font_family,
                size=self._theme.font_size_base,
                weight="bold",
            ),
            text_color=self._theme.text_secondary,
        )
        self._output_label.pack(side="left")

        self._status_badge = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(
                family=self._theme.font_family,
                size=self._theme.font_size_xs,
                weight="bold",
            ),
            fg_color=self._theme.bg_surface,
            corner_radius=6,
            padx=8,
            pady=2,
        )
        self._status_badge.pack(side="left", padx=10)

        self._copy_btn = ctk.CTkButton(
            header,
            text="📋 Copy",
            font=ctk.CTkFont(family=self._theme.font_family, size=self._theme.font_size_sm),
            fg_color=self._theme.bg_surface,
            hover_color=self._theme.bg_hover,
            text_color=self._theme.text_secondary,
            corner_radius=8,
            height=30,
            width=80,
            command=self._handle_copy,
        )
        self._copy_btn.pack(side="right")

        # Separator
        ctk.CTkFrame(output_frame, height=1, fg_color=self._theme.border_color).grid(
            row=1, column=0, sticky="ew", padx=0, pady=(8, 0)
        )

        # Output textbox
        self._output_text = ctk.CTkTextbox(
            output_frame,
            font=ctk.CTkFont(family="Consolas", size=self._theme.font_size_base),
            fg_color="transparent",
            text_color=self._theme.text_primary,
            corner_radius=0,
            border_width=0,
            height=130,
            wrap="word",
            state="disabled",
        )
        self._output_text.grid(row=2, column=0, sticky="nsew", padx=4, pady=(0, 4))

    # ------------------------------------------------------------------
    # Public interface (called by AppWindow/controller)
    # ------------------------------------------------------------------

    def update_algorithm(self, name: str, description: str, key_hint: str, accent_color: str) -> None:
        """Refresh the view for a newly selected algorithm."""
        self._page_title.configure(text=name)
        self._algo_name_lbl.configure(text=name)
        self._algo_desc_lbl.configure(text=description)
        self._key_hint_lbl.configure(text=f"ℹ  {key_hint}")
        self._badge.configure(text_color=accent_color)
        self._clear_output()

    def display_result(self, output: str, operation: str, success: bool, error: str = "") -> None:
        """Update output area with result and status badge."""
        self._output_text.configure(state="normal")
        self._output_text.delete("1.0", "end")

        if success:
            self._output_text.configure(text_color=self._theme.text_primary)
            self._output_text.insert("1.0", output)
            badge_text = "✓ Encrypted" if operation == "encrypt" else "✓ Decrypted"
            badge_color = self._theme.accent_success if operation == "encrypt" else self._theme.accent_warning
            self._status_badge.configure(text=badge_text, text_color=badge_color)
        else:
            self._output_text.configure(text_color=self._theme.accent_danger)
            self._output_text.insert("1.0", f"✗  {error}")
            self._status_badge.configure(
                text="✗ Error", text_color=self._theme.accent_danger
            )

        self._output_text.configure(state="disabled")

    def get_input_text(self) -> str:
        return self._input_text.get("1.0", "end-1c")

    def get_key(self) -> str:
        return self._key_entry.get()

    def get_output_text(self) -> str:
        return self._output_text.get("1.0", "end-1c")

    # ------------------------------------------------------------------
    # Private event handlers
    # ------------------------------------------------------------------

    def _handle_encrypt(self) -> None:
        self._on_encrypt(self.get_input_text(), self.get_key())

    def _handle_decrypt(self) -> None:
        self._on_decrypt(self.get_input_text(), self.get_key())

    def _handle_generate_key(self) -> None:
        # Call the keygen callback
        generated_key = self._on_generate_key()
        if generated_key:
            # Clear current key entry and insert the generated one
            self._key_entry.delete(0, "end")
            self._key_entry.insert(0, generated_key)

    def _handle_copy(self) -> None:
        self._on_copy(self.get_output_text())
        self._copy_btn.configure(text="✓ Copied!")
        self.after(1500, lambda: self._copy_btn.configure(text="📋 Copy"))

    def _clear_output(self) -> None:
        self._output_text.configure(state="normal")
        self._output_text.delete("1.0", "end")
        self._output_text.configure(state="disabled")
        self._status_badge.configure(text="")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _make_label(self, parent, text: str) -> ctk.CTkLabel:
        return ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(
                family=self._theme.font_family,
                size=self._theme.font_size_sm,
                weight="bold",
            ),
            text_color=self._theme.text_secondary,
        )
