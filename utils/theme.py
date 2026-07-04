# utils/theme.py
"""
Centralized theme/design-token definitions.

All colors, fonts, and spacing live here so the entire UI
stays visually consistent and is easy to restyle.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class AppTheme:
    """
    Immutable design-token container.

    Usage:
        theme = AppTheme()
        some_widget.configure(fg_color=theme.bg_primary)
    """

    # ── Background hierarchy ──────────────────────────────────────────
    bg_primary: tuple   = ("#F8FAFC", "#0D0F1A")   # (Light background, Dark background)
    bg_secondary: tuple = ("#FFFFFF", "#13162B")   # (Light Card, Dark Card)
    bg_surface: tuple   = ("#F1F5F9", "#1C2040")   # (Light Input, Dark Input)
    bg_hover: tuple     = ("#E2E8F0", "#252A50")   # Hover state

    # ── Accent palette ───────────────────────────────────────────────
    accent_primary: tuple   = ("#4F46E5", "#6C63FF")   # Primary accent
    accent_secondary: tuple = ("#8B5CF6", "#A78BFA")
    accent_success: tuple   = ("#059669", "#34D399")   # Emerald
    accent_danger: tuple    = ("#DC2626", "#F87171")   # Red
    accent_warning: tuple   = ("#D97706", "#FBBF24")   # Amber
    accent_info: tuple      = ("#2563EB", "#60A5FA")   # Blue

    # ── Text ─────────────────────────────────────────────────────────
    text_primary: tuple   = ("#0F172A", "#F1F5F9")   # Main text
    text_secondary: tuple = ("#475569", "#94A3B8")   # Subtext / labels
    text_muted: tuple     = ("#94A3B8", "#475569")   # Placeholder

    # ── Borders ──────────────────────────────────────────────────────
    border_color: tuple  = ("#E2E8F0", "#2D3560")
    border_radius: int   = 12           # px, used in corner_radius

    # ── Typography ───────────────────────────────────────────────────
    font_family: str      = "Segoe UI"
    font_size_xs: int     = 10
    font_size_sm: int     = 12
    font_size_base: int   = 14
    font_size_lg: int     = 16
    font_size_xl: int     = 20
    font_size_2xl: int    = 26
    font_size_hero: int   = 36

    # ── Spacing ──────────────────────────────────────────────────────
    pad_xs: int  = 4
    pad_sm: int  = 8
    pad_md: int  = 16
    pad_lg: int  = 24
    pad_xl: int  = 32

    # ── Algorithm badge colors ────────────────────────────────────────
    @property
    def algorithm_colors(self) -> Dict[str, str]:
        return {
            "Caesar Cipher":   "#F59E0B",
            "Vigenère Cipher": "#10B981",
            "Hill Cipher":     "#3B82F6",
            "DES":             "#EF4444",
            "AES":             "#8B5CF6",
            "RSA":             "#06B6D4",   # Cyan — asymmetric / modern
        }

    def get_algorithm_color(self, name: str) -> str:
        return self.algorithm_colors.get(name, self.accent_primary)
