# ui/app_window.py
"""
AppWindow — root application window and view orchestrator.

Responsibilities:
  - Initialize and configure the CustomTkinter root window
  - Own the CipherController instance
  - Manage view transitions (SelectionView ↔ CipherView)
  - Route user actions from views to the controller and back

This is the single place that knows about both views and the controller.
"""

import customtkinter as ctk

from controllers import CipherController
from utils.theme import AppTheme
from utils.clipboard import copy_to_clipboard
from ui.views.selection_view import SelectionView
from ui.views.cipher_view import CipherView


class AppWindow(ctk.CTk):
    """
    Main application window.

    Serves as the top-level orchestrator: it owns the controller,
    creates both views, and handles navigation between them.
    """

    WINDOW_TITLE = "🔐 Encryption Algorithms Suite"
    WINDOW_SIZE  = "920x680"
    MIN_SIZE     = (820, 580)

    def __init__(self) -> None:
        super().__init__()

        # ── App-level configuration ───────────────────────────────────
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._theme = AppTheme()
        self._controller = CipherController()
        self._active_view: ctk.CTkFrame | None = None

        self._configure_window()
        self._build_background()
        self._show_selection_view()

    # ------------------------------------------------------------------
    # Window setup
    # ------------------------------------------------------------------

    def _configure_window(self) -> None:
        """Set window title, size, background and icon."""
        self.title(self.WINDOW_TITLE)
        self.geometry(self.WINDOW_SIZE)
        self.minsize(*self.MIN_SIZE)
        self.configure(fg_color=self._theme.bg_primary)
        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) // 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) // 2
        self.geometry(f"+{x}+{y}")

    def _build_background(self) -> None:
        """Create the main content container that fills the window."""
        self._container = ctk.CTkFrame(self, fg_color=self._theme.bg_primary)
        self._container.pack(fill="both", expand=True)
        self._container.grid_columnconfigure(0, weight=1)
        self._container.grid_rowconfigure(0, weight=1)

    # ------------------------------------------------------------------
    # View management
    # ------------------------------------------------------------------

    def _show_selection_view(self) -> None:
        """Replace current view with the algorithm selection screen."""
        self._clear_active_view()

        # Gather cipher metadata from the controller
        names = self._controller.get_algorithm_names()
        descriptions = {
            name: self._get_cipher_description(name) for name in names
        }

        self._active_view = SelectionView(
            parent=self._container,
            algorithm_names=names,
            algorithm_descriptions=descriptions,
            on_algorithm_selected=self._handle_algorithm_selected,
            on_continue=self._show_cipher_view,
            on_toggle_theme=self.toggle_theme,
            theme=self._theme,
        )
        self._active_view.grid(row=0, column=0, sticky="nsew")

    def _show_cipher_view(self) -> None:
        """Replace current view with the cipher workspace."""
        self._clear_active_view()

        self._cipher_view = CipherView(
            parent=self._container,
            on_encrypt=self._handle_encrypt,
            on_decrypt=self._handle_decrypt,
            on_back=self._show_selection_view,
            on_copy=self._handle_copy,
            on_generate_key=self._handle_generate_key,
            on_toggle_theme=self.toggle_theme,
            theme=self._theme,
        )
        self._cipher_view.grid(row=0, column=0, sticky="nsew")
        self._active_view = self._cipher_view

        # Populate view with the selected algorithm's info
        self._refresh_cipher_view_header()


    def _clear_active_view(self) -> None:
        """Destroy the currently displayed view if any."""
        if self._active_view is not None:
            self._active_view.destroy()
            self._active_view = None

    # ------------------------------------------------------------------
    # Controller interaction handlers
    # ------------------------------------------------------------------

    def _handle_algorithm_selected(self, name: str) -> None:
        """Called when user clicks an algorithm card."""
        self._controller.select_algorithm(name)

    def _handle_encrypt(self, text: str, key: str) -> None:
        """Dispatch encryption and display result."""
        result = self._controller.encrypt(text, key)
        self._cipher_view.display_result(
            output=result.output,
            operation="encrypt",
            success=result.success,
            error=result.error_message or "",
        )

    def _handle_decrypt(self, text: str, key: str) -> None:
        """Dispatch decryption and display result."""
        result = self._controller.decrypt(text, key)
        self._cipher_view.display_result(
            output=result.output,
            operation="decrypt",
            success=result.success,
            error=result.error_message or "",
        )

    def _handle_copy(self, text: str) -> None:
        """Copy output text to the clipboard."""
        copy_to_clipboard(self, text)

    def _handle_generate_key(self) -> str:
        """Query the controller to generate a key for the active cipher."""
        return self._controller.generate_active_key()

    def toggle_theme(self) -> None:
        """Toggle appearance mode between light and dark."""
        current_mode = ctk.get_appearance_mode().lower()
        new_mode = "light" if current_mode == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _refresh_cipher_view_header(self) -> None:
        """Update cipher view header to reflect active algorithm."""
        name = self._controller.get_active_name()
        description = self._controller.get_active_description()
        key_hint = self._controller.get_active_key_hint()
        color = self._theme.get_algorithm_color(name)

        self._cipher_view.update_algorithm(name, description, key_hint, color)

    def _get_cipher_description(self, name: str) -> str:
        """Temporarily select cipher to read its description, then restore state."""
        current = self._controller.get_active_name()
        self._controller.select_algorithm(name)
        desc = self._controller.get_active_description()
        # Restore previous selection
        if current != "None":
            self._controller.select_algorithm(current)
        return desc
