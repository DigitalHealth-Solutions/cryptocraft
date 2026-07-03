# ui/widgets/algorithm_card.py
"""
AlgorithmCard — a clickable card widget for algorithm selection.

Explicit Binding Strategy:
  We bind mouse events (click, enter, leave) directly to the card frame
  and all of its child widgets (accent bar, content frame, title, description)
  using CustomTkinter's public .bind() method.
  
  To prevent "TypeError: missing required positional argument: 'e'" when
  CustomTkinter's event wrappers call callbacks with varying numbers of arguments,
  we define all lambda listeners with *args.
"""

import customtkinter as ctk
from typing import Callable

from utils.theme import AppTheme


class AlgorithmCard(ctk.CTkFrame):
    """
    A styled, clickable card representing a single cipher algorithm.
    Binds click and hover events explicitly to all visible components.
    """

    def __init__(
        self,
        parent,
        name: str,
        description: str,
        accent_color: str,
        on_select: Callable[[str], None],
        theme: AppTheme,
        **kwargs,
    ) -> None:
        super().__init__(
            parent,
            fg_color=theme.bg_secondary,
            corner_radius=theme.border_radius,
            border_width=2,
            border_color=theme.border_color,
            **kwargs,
        )
        self._theme = theme
        self._name = name
        self._accent = accent_color
        self._on_select = on_select
        self._selected = False

        self._build_ui(description)
        self._bind_explicit_events()

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------

    def _build_ui(self, description: str) -> None:
        """Construct the card's visual layout."""
        # Left colored accent bar
        self._accent_bar = ctk.CTkFrame(
            self,
            width=5,
            fg_color=self._accent,
            corner_radius=4,
        )
        self._accent_bar.pack(side="left", fill="y", padx=(0, 0), pady=0)
        self._accent_bar.pack_propagate(False)

        # Content container
        self._content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._content_frame.pack(side="left", fill="both", expand=True, padx=16, pady=14)

        # Algorithm name
        self._name_label = ctk.CTkLabel(
            self._content_frame,
            text=self._name,
            font=ctk.CTkFont(
                family=self._theme.font_family,
                size=self._theme.font_size_lg,
                weight="bold",
            ),
            text_color=self._theme.text_primary,
            anchor="w",
        )
        self._name_label.pack(fill="x")

        # Description
        self._desc_label = ctk.CTkLabel(
            self._content_frame,
            text=description,
            font=ctk.CTkFont(
                family=self._theme.font_family,
                size=self._theme.font_size_sm,
            ),
            text_color=self._theme.text_secondary,
            anchor="w",
            wraplength=330,
            justify="left",
        )
        self._desc_label.pack(fill="x", pady=(3, 0))

    # ------------------------------------------------------------------
    # Explicit Event Binding
    # ------------------------------------------------------------------

    def _bind_explicit_events(self) -> None:
        """
        Bind events explicitly to all visible widgets of this card.
        Uses *args to safely accept zero or more positional parameters.
        """
        widgets = [
            self,
            self._accent_bar,
            self._content_frame,
            self._name_label,
            self._desc_label,
        ]

        for widget in widgets:
            widget.bind("<Button-1>", lambda *args: self._on_click())
            widget.bind("<Enter>",    lambda *args: self._on_hover())
            widget.bind("<Leave>",    lambda *args: self._on_leave())

    # ------------------------------------------------------------------
    # Event Handlers
    # ------------------------------------------------------------------

    def _on_click(self) -> None:
        """Fired when the card or any of its children is clicked."""
        self._on_select(self._name)

    def _on_hover(self) -> None:
        """Highlight the card on mouse hover."""
        if not self._selected:
            self.configure(fg_color=self._theme.bg_hover)

    def _on_leave(self) -> None:
        """Remove highlight only if the mouse has completely left the card bounding box."""
        if self._selected:
            return
        try:
            ptr_x, ptr_y = self.winfo_pointerxy()
            card_x  = self.winfo_rootx()
            card_y  = self.winfo_rooty()
            card_x2 = card_x + self.winfo_width()
            card_y2 = card_y + self.winfo_height()
            
            still_inside = (card_x <= ptr_x <= card_x2) and (card_y <= ptr_y <= card_y2)
            if not still_inside:
                self.configure(fg_color=self._theme.bg_secondary)
        except Exception:
            self.configure(fg_color=self._theme.bg_secondary)

    # ------------------------------------------------------------------
    # Public Selection State API
    # ------------------------------------------------------------------

    def set_selected(self, selected: bool) -> None:
        """Highlight or restore the card state."""
        self._selected = selected
        if selected:
            self.configure(
                fg_color=self._theme.bg_hover,
                border_color=self._accent,
            )
            self._name_label.configure(text_color=self._accent)
        else:
            self.configure(
                fg_color=self._theme.bg_secondary,
                border_color=self._theme.border_color,
            )
            self._name_label.configure(text_color=self._theme.text_primary)
