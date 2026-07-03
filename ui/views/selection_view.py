# ui/views/selection_view.py
"""
SelectionView — Algorithm selection screen.

Displayed first; the user picks a cipher before proceeding.
"""

import customtkinter as ctk
from typing import Callable

from utils.theme import AppTheme
from ui.widgets.algorithm_card import AlgorithmCard


class SelectionView(ctk.CTkFrame):
    """
    Full-screen algorithm selection panel.

    Shows all available cipher cards. Selecting one triggers the
    provided callback and enables the 'Continue' button.
    """

    def __init__(
        self,
        parent,
        algorithm_names: list,
        algorithm_descriptions: dict,
        on_algorithm_selected: Callable[[str], None],
        on_continue: Callable[[], None],
        on_toggle_theme: Callable[[], None],
        theme: AppTheme,
        **kwargs,
    ) -> None:
        super().__init__(parent, fg_color="transparent", **kwargs)

        self._theme = theme
        self._on_algorithm_selected = on_algorithm_selected
        self._on_continue = on_continue
        self._on_toggle_theme = on_toggle_theme
        self._cards: dict[str, AlgorithmCard] = {}
        self._selected_name: str | None = None

        self._build_ui(algorithm_names, algorithm_descriptions)

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------

    def _build_ui(self, names: list, descriptions: dict) -> None:
        """Build the complete selection view layout."""
        self.grid_columnconfigure(0, weight=1)

        # ── Hero header ───────────────────────────────────────────────
        self._build_header()

        # ── Algorithm cards grid ──────────────────────────────────────
        cards_container = ctk.CTkFrame(self, fg_color="transparent")
        cards_container.grid(row=1, column=0, sticky="nsew", padx=40, pady=(0, 24))
        cards_container.grid_columnconfigure((0, 1), weight=1)

        for index, name in enumerate(names):
            desc = descriptions.get(name, "")
            color = self._theme.get_algorithm_color(name)
            card = AlgorithmCard(
                parent=cards_container,
                name=name,
                description=desc,
                accent_color=color,
                on_select=self._handle_selection,
                theme=self._theme,
            )
            row, col = divmod(index, 2)
            card.grid(row=row, column=col, sticky="ew", padx=8, pady=8)
            self._cards[name] = card

        # Let the cards container fill the remaining space
        cards_container.grid(row=1, column=0, sticky="nsew", padx=40, pady=(0, 40))


    def _build_header(self) -> None:
        """Build the title and subtitle header section."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=40, pady=(40, 32))

        # Lock icon + title
        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.pack(fill="x")

        ctk.CTkLabel(
            title_row,
            text="🔐",
            font=ctk.CTkFont(size=self._theme.font_size_hero),
        ).pack(side="left", padx=(0, 12))

        title_col = ctk.CTkFrame(title_row, fg_color="transparent")
        title_col.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            title_col,
            text="Encryption Algorithms Suite",
            font=ctk.CTkFont(
                family=self._theme.font_family,
                size=self._theme.font_size_2xl,
                weight="bold",
            ),
            text_color=self._theme.text_primary,
            anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_col,
            text="Select a cipher algorithm to get started",
            font=ctk.CTkFont(
                family=self._theme.font_family,
                size=self._theme.font_size_base,
            ),
            text_color=self._theme.text_secondary,
            anchor="w",
        ).pack(anchor="w")

        # Theme toggle button on the right
        self._theme_btn = ctk.CTkButton(
            title_row,
            text="☀️ / 🌙",
            font=ctk.CTkFont(size=self._theme.font_size_base),
            fg_color=self._theme.bg_secondary,
            hover_color=self._theme.bg_hover,
            text_color=self._theme.text_primary,
            width=50,
            height=36,
            corner_radius=8,
            command=self._on_toggle_theme,
        )
        self._theme_btn.pack(side="right", padx=(10, 0))

        # Separator
        ctk.CTkFrame(
            header, height=1, fg_color=self._theme.border_color
        ).pack(fill="x", pady=(16, 0))

    # ------------------------------------------------------------------
    # Event Handlers
    # ------------------------------------------------------------------

    def _handle_selection(self, name: str) -> None:
        """Select the algorithm and immediately transition to the workspace view."""
        self._selected_name = name
        self._on_algorithm_selected(name)
        self._on_continue()

