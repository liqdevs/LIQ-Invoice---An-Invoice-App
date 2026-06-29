import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
import tkinter as tk
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageTk
import json
import os
import sys
import datetime
import io
import uuid

from i18n import I18n

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

ACCENT = "#2563EB"
ACCENT_HOVER = "#1D4ED8"
BG = "#F8FAFC"
CARD = "#FFFFFF"
TEXT = "#0F172A"
TEXT2 = "#64748B"
BORDER = "#E2E8F0"
SUCCESS = "#10B981"
DANGER = "#EF4444"
WARNING = "#F59E0B"

                                                   
DARK_BG = "#0F172A"
DARK_CARD = "#1E293B"
DARK_TEXT = "#F1F5F9"
DARK_TEXT2 = "#94A3B8"
DARK_BORDER = "#334155"

                                                                         
                                                                        
STATUS_UNPAID = "unpaid"
STATUS_PAID = "paid"
STATUS_CANCELLED = "cancelled"
STATUS_ORDER = [STATUS_UNPAID, STATUS_PAID, STATUS_CANCELLED]

SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".liq_invoice_settings.json")
HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".liq_invoice_history.json")

                                                                                
                                                                               
                                                                           
                                                             
                                                                                
def get_resource_dir():
    """Return the directory to look for bundled resources (fonts, icons) in.

    - When running from source (`python invoice_app.py`), this is simply the
      folder containing this .py file.
    - When running from a PyInstaller --onefile .exe, PyInstaller unpacks
      bundled data (added via --add-data) into a temporary folder and
      exposes its path as sys._MEIPASS at runtime. Resources must be read
      from there instead, since the .py file itself doesn't really "exist"
      as a separate file inside the frozen executable.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


APP_DIR = get_resource_dir()
FONT_DIR = os.path.join(APP_DIR, "fonts")
FONT_REGULAR_PATH = os.path.join(FONT_DIR, "DejaVuSans.ttf")
FONT_BOLD_PATH = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

PDF_FONT_REGULAR = "Helvetica"
PDF_FONT_BOLD = "Helvetica-Bold"


def register_pdf_fonts():
    """Register a Unicode/Cyrillic-capable font with ReportLab, falling back
    to the built-in Helvetica only if the bundled font files are missing."""
    global PDF_FONT_REGULAR, PDF_FONT_BOLD
    try:
        if os.path.exists(FONT_REGULAR_PATH) and os.path.exists(FONT_BOLD_PATH):
            pdfmetrics.registerFont(TTFont("DejaVuSans", FONT_REGULAR_PATH))
            pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", FONT_BOLD_PATH))
            PDF_FONT_REGULAR = "DejaVuSans"
            PDF_FONT_BOLD = "DejaVuSans-Bold"
    except Exception:
                                                                          
                                                               
        PDF_FONT_REGULAR = "Helvetica"
        PDF_FONT_BOLD = "Helvetica-Bold"


register_pdf_fonts()


def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def save_settings(data):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def load_history():
    """Load the invoice history list. Each entry is a plain dict:
    {id, inv_number, client_name, date, due_date, currency, grand,
     status, pdf_path, created_at}. Returns [] on any error so a
     corrupted/missing file never crashes the app."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
    except Exception:
        pass
    return []


def save_history(entries):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


class ItemRow(ctk.CTkFrame):
    def __init__(self, parent, index, on_delete, on_change, i18n, colors):
        super().__init__(parent, fg_color="transparent")
        self.index = index
        self.on_delete = on_delete
        self.on_change = on_change
        self.i18n = i18n
        self.colors = colors
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        self.num_lbl = ctk.CTkLabel(self, text=f"{index+1}.", width=28,
                                     font=ctk.CTkFont("Segoe UI", 13), text_color=colors["text2"])
        self.num_lbl.grid(row=0, column=0, padx=(0, 4), pady=4, sticky="w")

        self.desc = ctk.CTkEntry(self, placeholder_text=i18n.t("item_desc_placeholder"),
                                  font=ctk.CTkFont("Segoe UI", 13),
                                  border_color=colors["border"], fg_color=colors["card"],
                                  text_color=colors["text"], corner_radius=8, height=36)
        self.desc.grid(row=0, column=1, padx=4, pady=4, sticky="ew")
        self.desc.bind("<KeyRelease>", lambda e: self.on_change())

        self.qty = ctk.CTkEntry(self, placeholder_text=i18n.t("item_qty_placeholder"), width=70,
                                 font=ctk.CTkFont("Segoe UI", 13),
                                 border_color=colors["border"], fg_color=colors["card"],
                                 text_color=colors["text"], corner_radius=8, height=36)
        self.qty.grid(row=0, column=2, padx=4, pady=4)
        self.qty.bind("<KeyRelease>", lambda e: self.on_change())

        self.price = ctk.CTkEntry(self, placeholder_text=i18n.t("item_price_placeholder"), width=100,
                                   font=ctk.CTkFont("Segoe UI", 13),
                                   border_color=colors["border"], fg_color=colors["card"],
                                   text_color=colors["text"], corner_radius=8, height=36)
        self.price.grid(row=0, column=3, padx=4, pady=4)
        self.price.bind("<KeyRelease>", lambda e: self.on_change())

        self.total_lbl = ctk.CTkLabel(self, text="0.00", width=90,
                                       font=ctk.CTkFont("Segoe UI", 13, "bold"),
                                       text_color=colors["text"], anchor="e")
        self.total_lbl.grid(row=0, column=4, padx=(4, 4), pady=4)

        danger_hover_bg = colors.get("danger_hover", "#FEE2E2")
        self.del_btn = ctk.CTkButton(self, text="✕", width=32, height=32, corner_radius=8,
                                      fg_color="transparent", border_width=1,
                                      border_color=colors["border"], text_color=colors["text2"],
                                      hover_color=danger_hover_bg, font=ctk.CTkFont("Segoe UI", 12),
                                      command=lambda: self.on_delete(self))
        self.del_btn.grid(row=0, column=5, padx=(4, 0), pady=4)

    def get_data(self):
        desc = self.desc.get().strip()
        try:
            qty = float(self.qty.get().strip().replace(",", ".") or "0")
        except Exception:
            qty = 0
        try:
            price = float(self.price.get().strip().replace(",", ".") or "0")
        except Exception:
            price = 0
        total = qty * price
        self.total_lbl.configure(text=f"{total:,.2f}")
        return desc, qty, price, total

    def refresh_text(self):
        self.desc.configure(placeholder_text=self.i18n.t("item_desc_placeholder"))
        self.qty.configure(placeholder_text=self.i18n.t("item_qty_placeholder"))
        self.price.configure(placeholder_text=self.i18n.t("item_price_placeholder"))


class SettingsPopover(ctk.CTkToplevel):
    """Small popover with Theme and Language controls, opened from the gear icon."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.config(bg=app.colors["border"])

        self.card = ctk.CTkFrame(self, fg_color=app.colors["card"], corner_radius=12,
                                  border_width=1, border_color=app.colors["border"])
        self.card.pack(padx=1, pady=1, fill="both", expand=True)

        t = app.i18n.t
        ctk.CTkLabel(self.card, text=t("preferences"),
                     font=ctk.CTkFont("Segoe UI", 13, "bold"),
                     text_color=app.colors["text"]).grid(row=0, column=0, columnspan=2,
                                                          padx=16, pady=(14, 6), sticky="w")

        ctk.CTkLabel(self.card, text=t("theme").upper(),
                     font=ctk.CTkFont("Segoe UI", 10, "bold"),
                     text_color=app.colors["text2"]).grid(row=1, column=0, columnspan=2,
                                                           padx=16, pady=(4, 4), sticky="w")

        theme_values = [t("theme_light"), t("theme_dark"), t("theme_system")]
        self._theme_map = {
            t("theme_light"): "light",
            t("theme_dark"): "dark",
            t("theme_system"): "system",
        }
        current_label = {
            "light": t("theme_light"),
            "dark": t("theme_dark"),
            "system": t("theme_system"),
        }.get(app.appearance_mode, t("theme_light"))

        self.theme_var = ctk.StringVar(value=current_label)
        theme_menu = ctk.CTkSegmentedButton(self.card, values=theme_values,
                                             variable=self.theme_var,
                                             font=ctk.CTkFont("Segoe UI", 12),
                                             selected_color=app.accent_color,
                                             selected_hover_color=ACCENT_HOVER,
                                             command=self._on_theme_change)
        theme_menu.grid(row=2, column=0, columnspan=2, padx=16, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(self.card, text=t("language").upper(),
                     font=ctk.CTkFont("Segoe UI", 10, "bold"),
                     text_color=app.colors["text2"]).grid(row=3, column=0, columnspan=2,
                                                           padx=16, pady=(4, 4), sticky="w")

        from i18n import LANGUAGES
        self._lang_labels = list(LANGUAGES.values())
        self._lang_codes = list(LANGUAGES.keys())
        current_lang_label = LANGUAGES.get(app.i18n.lang, "English")

        self.lang_var = ctk.StringVar(value=current_lang_label)
        lang_menu = ctk.CTkOptionMenu(self.card, values=self._lang_labels,
                                       variable=self.lang_var,
                                       font=ctk.CTkFont("Segoe UI", 12),
                                       fg_color=app.colors["bg"],
                                       button_color=app.accent_color,
                                       button_hover_color=ACCENT_HOVER,
                                       dropdown_fg_color=app.colors["card"],
                                       corner_radius=8, height=34,
                                       command=self._on_lang_change)
        lang_menu.grid(row=4, column=0, columnspan=2, padx=16, pady=(0, 6), sticky="ew")

        ctk.CTkLabel(self.card, text=t("more_settings_soon"),
                     font=ctk.CTkFont("Segoe UI", 10), text_color=app.colors["text2"]
                     ).grid(row=5, column=0, columnspan=2, padx=16, pady=(2, 14), sticky="w")

        self.card.grid_columnconfigure(0, weight=1)

        self.bind("<FocusOut>", self._maybe_close)
        self.after(50, lambda: self.focus_force())
        self._closed = False

    def _on_theme_change(self, label):
        mode = self._theme_map.get(label, "light")
        self.app.set_appearance_mode(mode)

    def _on_lang_change(self, label):
        if label in self._lang_labels:
            idx = self._lang_labels.index(label)
            code = self._lang_codes[idx]
            self.app.i18n.set_lang(code)
            self.app.settings["language"] = code
            save_settings(self.app.settings)
        self._close()

    def _maybe_close(self, e=None):
        self.after(120, self._check_focus)

    def _check_focus(self):
        try:
            if self.focus_get() is None:
                self._close()
        except Exception:
            self._close()

    def _close(self):
        if not self._closed:
            self._closed = True
            try:
                self.destroy()
            except Exception:
                pass


class InvoiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.settings = load_settings()

        self.i18n = I18n(self.settings.get("language", "en"))
        self.i18n.on_change(self._on_lang_changed)

        self.appearance_mode = self.settings.get("appearance", "light")
        ctk.set_appearance_mode("dark" if self.appearance_mode == "dark" else
                                 ("light" if self.appearance_mode == "light" else "system"))
        self._refresh_color_palette()

        self.title(self.i18n.t("app_title"))
        self.geometry("1100x780")
        self.minsize(920, 660)
        self.configure(fg_color=self.colors["bg"])
        self.resizable(True, True)

        self.accent_color = self.settings.get("accent", ACCENT)
        self.currency = self.settings.get("currency", "$")
        self.tax_rate = self.settings.get("tax_rate", 20)
        self.item_rows = []
        self.logo_path = self.settings.get("logo_path", "")

        self._settings_popover = None
        self._form_state = {}
        self.current_tab = "new"                     
        self.history = load_history()
        self._history_search = ""

        self._build_ui()
        self._restore_sender()
        self._update_totals()

                                                                            
    def _refresh_color_palette(self):
        is_dark = (ctk.get_appearance_mode() == "Dark")
        if is_dark:
            self.colors = {
                "bg": DARK_BG, "card": DARK_CARD, "text": DARK_TEXT,
                "text2": DARK_TEXT2, "border": DARK_BORDER,
                "header_bg": "#0B1220", "danger_hover": "#3F1D1D",
                "status_unpaid_bg": "#3F2D0E", "status_unpaid_text": "#FBBF24",
                "status_paid_bg": "#0F3D2B", "status_paid_text": "#34D399",
                "status_cancelled_bg": "#3F1D1D", "status_cancelled_text": "#F87171",
            }
        else:
            self.colors = {
                "bg": BG, "card": CARD, "text": TEXT,
                "text2": TEXT2, "border": BORDER,
                "header_bg": "#F1F5F9", "danger_hover": "#FEE2E2",
                "status_unpaid_bg": "#FEF3C7", "status_unpaid_text": "#B45309",
                "status_paid_bg": "#D1FAE5", "status_paid_text": "#047857",
                "status_cancelled_bg": "#FEE2E2", "status_cancelled_text": "#B91C1C",
            }

    def set_appearance_mode(self, mode):
        """mode: 'light' | 'dark' | 'system'"""
        self.appearance_mode = mode
        ctk.set_appearance_mode(mode)
        self.settings["appearance"] = mode
        save_settings(self.settings)
        self._refresh_color_palette()
        self._rebuild_ui()

    def _snapshot_form_state(self):
        """Capture all current form values into a plain dict BEFORE the
        underlying widgets get destroyed. Reading from a destroyed Tk widget
        raises TclError, which previously aborted _build_main partway
        through (causing items/totals/notes to silently disappear after a
        theme or language switch). All rebuild logic must read from this
        snapshot instead of from old widget references."""
        state = {}

        def safe_get(attr):
            widget = getattr(self, attr, None)
            if widget is None:
                return None
            try:
                return widget.get().strip()
            except Exception:
                return None

        for attr in ["sender_name", "sender_addr", "sender_email", "sender_phone",
                     "client_name", "client_email", "client_addr", "client_inn",
                     "inv_number", "inv_date", "inv_due", "inv_project"]:
            val = safe_get(attr)
            if val:
                state[attr] = val

        if hasattr(self, "notes"):
            try:
                state["notes"] = self.notes.get("0.0", "end").strip()
            except Exception:
                pass

        items = []
        for row in getattr(self, "item_rows", []):
            try:
                items.append((row.desc.get(), row.qty.get(), row.price.get()))
            except Exception:
                pass
        if items:
            state["items"] = items

        if hasattr(self, "tax_entry"):
            try:
                state["tax_value"] = self.tax_entry.get().strip()
            except Exception:
                pass

        self._form_state = state

    def _rebuild_ui(self):
        self._snapshot_form_state()
        for child in list(self.winfo_children()):
            child.destroy()
                                                                            
                                                                    
                                                                           
                                                                        
                                                                           
                                                                  
        for attr in ("lbl_subtotal", "lbl_tax", "lbl_total", "lbl_tax_caption",
                     "_history_rows_frame", "_history_list_card", "_history_search_entry"):
            if hasattr(self, attr):
                delattr(self, attr)
        self.configure(fg_color=self.colors["bg"])
        self._build_ui()
        if self.current_tab == "new":
            self._restore_sender()
            self._update_totals()

    def _switch_tab(self, tab_key):
        if self.current_tab == tab_key:
            return
        self.current_tab = tab_key
        self._rebuild_ui()

    def _on_lang_changed(self):
        self.title(self.i18n.t("app_title"))
        self._rebuild_ui()

                                                                              
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=0, minsize=260)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()

    def _build_sidebar(self):
        t = self.i18n.t
        c = self.colors
        sidebar = ctk.CTkFrame(self, fg_color=c["card"], corner_radius=0, width=260,
                                border_width=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(11, weight=1)
        self.sidebar = sidebar

        logo_frame = ctk.CTkFrame(sidebar, fg_color=self.accent_color,
                                   corner_radius=0, height=64)
        logo_frame.grid(row=0, column=0, sticky="ew", pady=(0, 0))
        logo_frame.grid_propagate(False)
        logo_frame.grid_columnconfigure(0, weight=1)
        logo_frame.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(logo_frame, text=t("app_brand"),
                     font=ctk.CTkFont("Segoe UI", 18, "bold"),
                     text_color="white").grid(row=0, column=0, padx=(20, 4), pady=18, sticky="w")

                                                                         
                                                           
        gear_btn = ctk.CTkButton(logo_frame, text="⚙", width=36, height=36,
                                  corner_radius=18, fg_color="#3B7AE8",
                                  hover_color="#5C8FEC", text_color="white",
                                  font=ctk.CTkFont("Segoe UI", 16),
                                  command=self._open_settings_popover)
        gear_btn.grid(row=0, column=1, padx=(0, 16), pady=18, sticky="e")
        self.gear_btn = gear_btn

                                                                       
                                                          
        tabs_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        tabs_frame.grid(row=1, column=0, padx=16, pady=(14, 8), sticky="ew")
        tabs_frame.columnconfigure(0, weight=1)
        tabs_frame.columnconfigure(1, weight=1)

        def make_tab_btn(col, label, tab_key):
            is_active = (self.current_tab == tab_key)
            btn = ctk.CTkButton(
                tabs_frame, text=label, height=34,
                font=ctk.CTkFont("Segoe UI", 12, "bold" if is_active else "normal"),
                corner_radius=8,
                fg_color=self.accent_color if is_active else "transparent",
                text_color="white" if is_active else c["text2"],
                hover_color=ACCENT_HOVER if is_active else c["bg"],
                border_width=0 if is_active else 1,
                border_color=c["border"],
                command=lambda: self._switch_tab(tab_key))
            btn.grid(row=0, column=col, padx=(0, 4) if col == 0 else (4, 0), sticky="ew")
            return btn

        make_tab_btn(0, t("tab_new_invoice"), "new")
        make_tab_btn(1, t("tab_history"), "history")

        if self.current_tab != "new":
                                                                        
                                                                          
            sidebar.grid_columnconfigure(0, weight=1)
            return

        def section(parent, title, row):
            ctk.CTkLabel(parent, text=title.upper(),
                         font=ctk.CTkFont("Segoe UI", 10, "bold"),
                         text_color=c["text2"]).grid(row=row, column=0, padx=20, pady=(16, 4), sticky="w")

        section(sidebar, t("your_company"), 2)

        self.sender_name = ctk.CTkEntry(sidebar, placeholder_text=t("company_name"),
                                         font=ctk.CTkFont("Segoe UI", 13),
                                         border_color=c["border"], fg_color=c["bg"], text_color=c["text"],
                                         corner_radius=8, height=36, width=220)
        self.sender_name.grid(row=3, column=0, padx=20, pady=(0, 6), sticky="ew")

        self.sender_addr = ctk.CTkEntry(sidebar, placeholder_text=t("address_tax_id"),
                                         font=ctk.CTkFont("Segoe UI", 13),
                                         border_color=c["border"], fg_color=c["bg"], text_color=c["text"],
                                         corner_radius=8, height=36)
        self.sender_addr.grid(row=4, column=0, padx=20, pady=(0, 6), sticky="ew")

        self.sender_email = ctk.CTkEntry(sidebar, placeholder_text=t("email"),
                                          font=ctk.CTkFont("Segoe UI", 13),
                                          border_color=c["border"], fg_color=c["bg"], text_color=c["text"],
                                          corner_radius=8, height=36)
        self.sender_email.grid(row=5, column=0, padx=20, pady=(0, 6), sticky="ew")

        self.sender_phone = ctk.CTkEntry(sidebar, placeholder_text=t("phone"),
                                          font=ctk.CTkFont("Segoe UI", 13),
                                          border_color=c["border"], fg_color=c["bg"], text_color=c["text"],
                                          corner_radius=8, height=36)
        self.sender_phone.grid(row=6, column=0, padx=20, pady=(0, 6), sticky="ew")

        logo_btn = ctk.CTkButton(sidebar, text=f"🖼  {t('upload_logo')}", height=34,
                                  font=ctk.CTkFont("Segoe UI", 12),
                                  fg_color="transparent", border_width=1,
                                  border_color=c["border"], text_color=c["text2"],
                                  hover_color=c["bg"], corner_radius=8,
                                  command=self._pick_logo)
        logo_btn.grid(row=7, column=0, padx=20, pady=(0, 4), sticky="ew")

        self.logo_lbl = ctk.CTkLabel(sidebar, text="", font=ctk.CTkFont("Segoe UI", 11),
                                      text_color=SUCCESS)
        self.logo_lbl.grid(row=8, column=0, padx=20, pady=(0, 4), sticky="w")
        if self.logo_path and os.path.exists(self.logo_path):
            self.logo_lbl.configure(text=f"✓ {os.path.basename(self.logo_path)}")

        section(sidebar, t("settings"), 9)

        settings_inner = ctk.CTkFrame(sidebar, fg_color="transparent")
        settings_inner.grid(row=10, column=0, padx=20, pady=(0, 8), sticky="ew")
        settings_inner.columnconfigure(0, weight=1)
        settings_inner.columnconfigure(1, weight=1)

        ctk.CTkLabel(settings_inner, text=t("currency"),
                     font=ctk.CTkFont("Segoe UI", 12), text_color=c["text2"]).grid(row=0, column=0, sticky="w", pady=(0, 2))
        ctk.CTkLabel(settings_inner, text=t("tax_rate"),
                     font=ctk.CTkFont("Segoe UI", 12), text_color=c["text2"]).grid(row=0, column=1, sticky="w", padx=(8, 0), pady=(0, 2))

        self.currency_var = ctk.StringVar(value=self.currency)
        cur_menu = ctk.CTkOptionMenu(settings_inner, values=["$", "€", "£", "₴", "₽", "zł"],
                                      variable=self.currency_var,
                                      font=ctk.CTkFont("Segoe UI", 13),
                                      fg_color=c["bg"], button_color=self.accent_color,
                                      button_hover_color=ACCENT_HOVER,
                                      dropdown_fg_color=c["card"], corner_radius=8, height=34,
                                      command=lambda v: (setattr(self, 'currency', v), self._update_totals()))
        cur_menu.grid(row=1, column=0, sticky="ew", pady=(0, 6))

        self.tax_entry = ctk.CTkEntry(settings_inner, width=70,
                                       font=ctk.CTkFont("Segoe UI", 13),
                                       border_color=c["border"], fg_color=c["bg"], text_color=c["text"],
                                       corner_radius=8, height=34)
        self.tax_entry.insert(0, self._form_state.get("tax_value") or str(self.tax_rate))
        self.tax_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(0, 6))
        self.tax_entry.bind("<KeyRelease>", lambda e: self._update_totals())

        accent_btn = ctk.CTkButton(settings_inner, text=f"🎨  {t('accent_color')}", height=34,
                                    font=ctk.CTkFont("Segoe UI", 12),
                                    fg_color="transparent", border_width=1,
                                    border_color=c["border"], text_color=c["text2"],
                                    hover_color=c["bg"], corner_radius=8,
                                    command=self._pick_accent)
        accent_btn.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 0))

        sidebar.grid_columnconfigure(0, weight=1)

        spacer = ctk.CTkFrame(sidebar, fg_color="transparent")
        spacer.grid(row=11, column=0, sticky="nsew")

        save_btn = ctk.CTkButton(sidebar, text=f"💾  {t('save_company_data')}",
                                  height=38, font=ctk.CTkFont("Segoe UI", 13, "bold"),
                                  fg_color=self.accent_color, hover_color=ACCENT_HOVER,
                                  corner_radius=8, command=self._save_sender)
        save_btn.grid(row=12, column=0, padx=20, pady=(0, 20), sticky="ew")

    def _open_settings_popover(self):
        if self._settings_popover is not None:
            try:
                self._settings_popover.destroy()
            except Exception:
                pass
            self._settings_popover = None
            return

        self.update_idletasks()
        x = self.gear_btn.winfo_rootx() - 140
        y = self.gear_btn.winfo_rooty() + self.gear_btn.winfo_height() + 6

        pop = SettingsPopover(self, self)
        pop.geometry(f"260x270+{x}+{y}")
        self._settings_popover = pop

        def on_destroy(e):
            self._settings_popover = None
        pop.bind("<Destroy>", on_destroy)

    def _build_main(self):
        c = self.colors
        main = ctk.CTkScrollableFrame(self, fg_color=c["bg"], corner_radius=0,
                                       scrollbar_button_color=c["border"],
                                       scrollbar_button_hover_color=c["text2"])
        main.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        main.grid_columnconfigure(0, weight=1)
        self.main_frame = main

        if self.current_tab == "history":
            self._build_history_tab(main)
        else:
            self._build_new_invoice_tab(main)

    def _build_new_invoice_tab(self, main):
        t = self.i18n.t
        c = self.colors

        top_bar = ctk.CTkFrame(main, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 0))
        top_bar.columnconfigure(0, weight=1)

        ctk.CTkLabel(top_bar, text=t("new_invoice"),
                     font=ctk.CTkFont("Segoe UI", 26, "bold"),
                     text_color=c["text"]).grid(row=0, column=0, sticky="w")

        btn_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        btn_frame.grid(row=0, column=1, sticky="e")

        ctk.CTkButton(btn_frame, text=f"🖨  {t('preview')}", height=38, width=160,
                      font=ctk.CTkFont("Segoe UI", 13),
                      fg_color="transparent", border_width=1.5,
                      border_color=self.accent_color, text_color=self.accent_color,
                      hover_color=c["bg"], corner_radius=8,
                      command=self._preview).grid(row=0, column=0, padx=(0, 10))

        self.pdf_btn = ctk.CTkButton(btn_frame, text=f"📄  {t('create_pdf')}", height=38, width=160,
                                      font=ctk.CTkFont("Segoe UI", 13, "bold"),
                                      fg_color=self.accent_color, hover_color=ACCENT_HOVER,
                                      corner_radius=8, command=self._generate_pdf)
        self.pdf_btn.grid(row=0, column=1)

        self._build_client_section(main)
        self._build_invoice_meta(main)
        self._build_items_section(main)
        self._build_totals(main)
        self._build_notes(main)

    def _build_history_tab(self, main):
        t = self.i18n.t
        c = self.colors

        top_bar = ctk.CTkFrame(main, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 0))
        top_bar.columnconfigure(0, weight=1)

        ctk.CTkLabel(top_bar, text=t("history_title"),
                     font=ctk.CTkFont("Segoe UI", 26, "bold"),
                     text_color=c["text"]).grid(row=0, column=0, sticky="w")

        search_entry = ctk.CTkEntry(top_bar, placeholder_text=t("history_search_placeholder"),
                                     width=260, height=38,
                                     font=ctk.CTkFont("Segoe UI", 13),
                                     border_color=c["border"], fg_color=c["card"], text_color=c["text"],
                                     corner_radius=8)
        search_entry.grid(row=0, column=1, sticky="e")
        if self._history_search:
            search_entry.insert(0, self._history_search)

        def on_search(_e=None):
            self._history_search = search_entry.get().strip().lower()
            self._refresh_history_list()
        search_entry.bind("<KeyRelease>", on_search)
        self._history_search_entry = search_entry

        list_card = ctk.CTkFrame(main, fg_color=c["card"], corner_radius=12,
                                  border_width=1, border_color=c["border"])
        list_card.grid(row=1, column=0, sticky="ew", padx=32, pady=(16, 28))
        list_card.grid_columnconfigure(0, weight=1)
        self._history_list_card = list_card

        header = ctk.CTkFrame(list_card, fg_color=c["header_bg"], corner_radius=6)
        header.grid(row=0, column=0, padx=20, pady=(20, 4), sticky="ew")
        widths = [(t("history_col_date"), 100), (t("history_col_number"), 90),
                  (t("history_col_client"), 0), (t("history_col_amount"), 110),
                  (t("history_col_status"), 150)]
        header.grid_columnconfigure(2, weight=1)
        for col, (text, w) in enumerate(widths):
            ctk.CTkLabel(header, text=text, font=ctk.CTkFont("Segoe UI", 11, "bold"),
                         text_color=c["text2"], width=w,
                         anchor="w").grid(row=0, column=col, padx=(12 if col == 0 else 8, 8), pady=8, sticky="w")

        self._history_rows_frame = ctk.CTkFrame(list_card, fg_color="transparent")
        self._history_rows_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self._history_rows_frame.grid_columnconfigure(0, weight=1)

        self._refresh_history_list()

    def _filtered_history(self):
        q = (self._history_search or "").strip().lower()
        if not q:
            return list(self.history)
        out = []
        for e in self.history:
            if q in str(e.get("client_name", "")).lower() or q in str(e.get("inv_number", "")).lower():
                out.append(e)
        return out

    def _refresh_history_list(self):
        """Redraw just the row list (used after search/status/delete changes),
        without tearing down the whole window like _rebuild_ui does."""
        frame = getattr(self, "_history_rows_frame", None)
        if frame is None:
            return
        for child in list(frame.winfo_children()):
            child.destroy()

        t = self.i18n.t
        c = self.colors
        entries = self._filtered_history()

        if not entries:
            ctk.CTkLabel(frame, text=t("history_empty"),
                         font=ctk.CTkFont("Segoe UI", 13), text_color=c["text2"],
                         justify="center").grid(row=0, column=0, pady=40)
            return

        for i, entry in enumerate(entries):
            self._build_history_row(frame, i, entry)

    def _build_history_row(self, parent, row_idx, entry):
        t = self.i18n.t
        c = self.colors

        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.grid(row=row_idx, column=0, sticky="ew", pady=3)
        row.grid_columnconfigure(2, weight=1)

        date_str = entry.get("date", "") or "—"
        ctk.CTkLabel(row, text=date_str, font=ctk.CTkFont("Segoe UI", 12),
                     text_color=c["text2"], width=100, anchor="w").grid(row=0, column=0, padx=(0, 8), sticky="w")

        ctk.CTkLabel(row, text=f"#{entry.get('inv_number', '')}", font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=c["text"], width=90, anchor="w").grid(row=0, column=1, padx=(0, 8), sticky="w")

        client = entry.get("client_name") or "—"
        ctk.CTkLabel(row, text=client, font=ctk.CTkFont("Segoe UI", 12),
                     text_color=c["text"], anchor="w").grid(row=0, column=2, padx=(0, 8), sticky="w")

        cur = entry.get("currency", "$")
        amount = entry.get("grand", 0)
        ctk.CTkLabel(row, text=f"{cur}{amount:,.2f}", font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=c["text"], width=110, anchor="w").grid(row=0, column=3, padx=(0, 8), sticky="w")

        status = entry.get("status", STATUS_UNPAID)
        status_labels = {
            STATUS_UNPAID: t("status_unpaid"),
            STATUS_PAID: t("status_paid"),
            STATUS_CANCELLED: t("status_cancelled"),
        }
        status_colors = {
            STATUS_UNPAID: ("status_unpaid_bg", "status_unpaid_text"),
            STATUS_PAID: ("status_paid_bg", "status_paid_text"),
            STATUS_CANCELLED: ("status_cancelled_bg", "status_cancelled_text"),
        }
        bg_key, text_key = status_colors.get(status, status_colors[STATUS_UNPAID])

        status_menu = ctk.CTkOptionMenu(
            row, values=[status_labels[s] for s in STATUS_ORDER],
            width=140, height=30, corner_radius=15,
            font=ctk.CTkFont("Segoe UI", 11, "bold"),
            fg_color=c[bg_key], text_color=c[text_key],
            button_color=c[bg_key], button_hover_color=c[bg_key],
            dropdown_fg_color=c["card"], dropdown_text_color=c["text"],
            dropdown_hover_color=c["bg"],
        )
        status_menu.set(status_labels[status])
        reverse_map = {v: k for k, v in status_labels.items()}

        def on_status_change(label, entry_id=entry.get("id")):
            new_status = reverse_map.get(label, STATUS_UNPAID)
            self._set_history_status(entry_id, new_status)
            for e in self.history:
                if e.get("id") == entry_id:
                    e["status"] = new_status
            self._refresh_history_list()

        status_menu.configure(command=on_status_change)
        status_menu.grid(row=0, column=4, padx=(0, 8), sticky="w")

        open_btn = ctk.CTkButton(row, text=f"📂 {t('open_pdf')}", width=110, height=30,
                                  corner_radius=8, font=ctk.CTkFont("Segoe UI", 11),
                                  fg_color="transparent", border_width=1,
                                  border_color=c["border"], text_color=c["text2"],
                                  hover_color=c["bg"],
                                  command=lambda e=entry: self._open_history_pdf(e))
        open_btn.grid(row=0, column=5, padx=(0, 4), sticky="e")

        del_btn = ctk.CTkButton(row, text="✕", width=30, height=30, corner_radius=8,
                                 fg_color="transparent", border_width=1,
                                 border_color=c["border"], text_color=c["text2"],
                                 hover_color=c["danger_hover"],
                                 command=lambda eid=entry.get("id"): self._delete_history_entry(eid))
        del_btn.grid(row=0, column=6, sticky="e")

    def _card(self, parent, row, title=None):
        c = self.colors
        card = ctk.CTkFrame(parent, fg_color=c["card"], corner_radius=12,
                             border_width=1, border_color=c["border"])
        card.grid(row=row, column=0, sticky="ew", padx=32, pady=(16, 0))
        card.grid_columnconfigure(0, weight=1)
        if title:
            ctk.CTkLabel(card, text=title,
                         font=ctk.CTkFont("Segoe UI", 12, "bold"),
                         text_color=c["text2"]).grid(row=0, column=0, padx=20, pady=(14, 8), sticky="w")
        return card

    def _build_client_section(self, parent):
        t = self.i18n.t
        c = self.colors
        card = self._card(parent, 1, t("recipient_client"))
        card.grid_columnconfigure((0, 1), weight=1)

        self.client_name = ctk.CTkEntry(card, placeholder_text=t("client_company_name"),
                                         font=ctk.CTkFont("Segoe UI", 14),
                                         border_color=c["border"], fg_color=c["bg"], text_color=c["text"],
                                         corner_radius=8, height=40)
        self.client_name.grid(row=1, column=0, padx=(20, 8), pady=(0, 10), sticky="ew")

        self.client_email = ctk.CTkEntry(card, placeholder_text=t("client_email"),
                                          font=ctk.CTkFont("Segoe UI", 13),
                                          border_color=c["border"], fg_color=c["bg"], text_color=c["text"],
                                          corner_radius=8, height=40)
        self.client_email.grid(row=1, column=1, padx=(8, 20), pady=(0, 10), sticky="ew")

        self.client_addr = ctk.CTkEntry(card, placeholder_text=t("client_address"),
                                         font=ctk.CTkFont("Segoe UI", 13),
                                         border_color=c["border"], fg_color=c["bg"], text_color=c["text"],
                                         corner_radius=8, height=40)
        self.client_addr.grid(row=2, column=0, padx=(20, 8), pady=(0, 14), sticky="ew")

        self.client_inn = ctk.CTkEntry(card, placeholder_text=t("client_tax_id"),
                                        font=ctk.CTkFont("Segoe UI", 13),
                                        border_color=c["border"], fg_color=c["bg"], text_color=c["text"],
                                        corner_radius=8, height=40)
        self.client_inn.grid(row=2, column=1, padx=(8, 20), pady=(0, 14), sticky="ew")

                                                                           
        for attr in ("client_name", "client_email", "client_addr", "client_inn"):
            val = self._form_state.get(attr)
            if val:
                getattr(self, attr).insert(0, val)

    def _build_invoice_meta(self, parent):
        t = self.i18n.t
        c = self.colors
        card = self._card(parent, 2, t("invoice_details"))
        card.grid_columnconfigure((0, 1, 2, 3), weight=1)

        fields = [
            (t("invoice_number"), "inv_number", "001"),
            (t("issue_date"), "inv_date", datetime.date.today().strftime("%Y-%m-%d")),
            (t("due_date"), "inv_due", (datetime.date.today() + datetime.timedelta(days=14)).strftime("%Y-%m-%d")),
            (t("project_order"), "inv_project", ""),
        ]
        for i, (label, attr, default) in enumerate(fields):
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont("Segoe UI", 11),
                         text_color=c["text2"]).grid(row=1, column=i, padx=(20 if i == 0 else 8, 8), pady=(0, 2), sticky="w")
            entry = ctk.CTkEntry(card, font=ctk.CTkFont("Segoe UI", 13),
                                  border_color=c["border"], fg_color=c["bg"], text_color=c["text"],
                                  corner_radius=8, height=38)
                                                                                    
                                                                                  
                                                                           
            value = self._form_state.get(attr, default)
            entry.insert(0, value if value else default)
            entry.grid(row=2, column=i,
                       padx=(20 if i == 0 else 8, 20 if i == 3 else 8),
                       pady=(0, 14), sticky="ew")
            setattr(self, attr, entry)

    def _build_items_section(self, parent):
        t = self.i18n.t
        c = self.colors
        card = self._card(parent, 3, t("invoice_items"))
        self.items_card = card

        header = ctk.CTkFrame(card, fg_color=c["header_bg"], corner_radius=6)
        header.grid(row=1, column=0, padx=20, pady=(0, 4), sticky="ew")
        header.grid_columnconfigure(1, weight=3)
        header.grid_columnconfigure(2, weight=1)
        header.grid_columnconfigure(3, weight=1)
        header.grid_columnconfigure(4, weight=1)

        for col, (text, w) in enumerate([
            (t("col_no"), 28), (t("col_description"), 0), (t("col_qty"), 70),
            (t("col_price"), 100), (t("col_amount"), 90)
        ]):
            ctk.CTkLabel(header, text=text, font=ctk.CTkFont("Segoe UI", 11, "bold"),
                         text_color=c["text2"], width=w,
                         anchor="w" if col < 2 else "e").grid(
                row=0, column=col, padx=(12 if col == 0 else 4, 4), pady=6, sticky="w" if col < 2 else "e")

        self.items_container = ctk.CTkFrame(card, fg_color="transparent")
        self.items_container.grid(row=2, column=0, padx=20, pady=(0, 8), sticky="ew")
        self.items_container.grid_columnconfigure(0, weight=1)

                                                                       
                                                                           
                                                                    
        preserved = self._form_state.get("items", [])
        self.item_rows = []

        if preserved:
            for desc, qty, price in preserved:
                self._add_item(desc, qty, price)
        else:
            self._add_item()
            self._add_item()

        add_btn = ctk.CTkButton(card, text=f"＋  {t('add_item')}", height=36,
                                 font=ctk.CTkFont("Segoe UI", 13),
                                 fg_color="transparent", border_width=1,
                                 border_color=self.accent_color, text_color=self.accent_color,
                                 hover_color=c["bg"], corner_radius=8,
                                 command=lambda: self._add_item())
        add_btn.grid(row=3, column=0, padx=20, pady=(0, 16), sticky="w")

    def _build_totals(self, parent):
        t = self.i18n.t
        c = self.colors
        card = self._card(parent, 4)
        card.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.grid(row=0, column=0, padx=20, pady=16, sticky="e")

        def total_row(row, label, var_name, big=False, colored=False):
            size = 15 if big else 13
            weight = "bold" if big else "normal"
            fg = self.accent_color if colored else (c["text"] if big else c["text2"])

            ctk.CTkLabel(inner, text=label, font=ctk.CTkFont("Segoe UI", size),
                         text_color=c["text2"]).grid(row=row, column=0, padx=(0, 48), pady=3, sticky="w")
            lbl = ctk.CTkLabel(inner, text="0.00", font=ctk.CTkFont("Segoe UI", size, weight),
                                text_color=fg, width=130, anchor="e")
            lbl.grid(row=row, column=1, pady=3, sticky="e")
            setattr(self, var_name, lbl)
            return lbl

        total_row(0, t("subtotal"), "lbl_subtotal")
        self.lbl_tax_caption = ctk.CTkLabel(inner, text=t("tax_label", rate=self.tax_rate),
                                             font=ctk.CTkFont("Segoe UI", 13), text_color=c["text2"])
        self.lbl_tax_caption.grid(row=1, column=0, padx=(0, 48), pady=3, sticky="w")
        self.lbl_tax = ctk.CTkLabel(inner, text="0.00", font=ctk.CTkFont("Segoe UI", 13),
                                     text_color=c["text2"], width=130, anchor="e")
        self.lbl_tax.grid(row=1, column=1, pady=3, sticky="e")

        sep = ctk.CTkFrame(inner, height=1, fg_color=c["border"])
        sep.grid(row=2, column=0, columnspan=2, sticky="ew", pady=6)

        total_row(3, t("total_due"), "lbl_total", big=True, colored=True)

    def _build_notes(self, parent):
        t = self.i18n.t
        c = self.colors
        card = self._card(parent, 5, t("notes_requisites"))

        existing_notes = self._form_state.get("notes")

        self.notes = ctk.CTkTextbox(card, height=90, font=ctk.CTkFont("Segoe UI", 13),
                                     border_color=c["border"], fg_color=c["bg"], text_color=c["text"],
                                     corner_radius=8, border_width=1)
        self.notes.grid(row=1, column=0, padx=20, pady=(0, 16), sticky="ew")
        self.notes.insert("0.0", existing_notes if existing_notes else t("notes_default"))

        ctk.CTkFrame(parent, fg_color="transparent", height=32).grid(row=6, column=0)

    def _add_item(self, desc="", qty="", price=""):
        idx = len(self.item_rows)
        row = ItemRow(self.items_container, idx, self._delete_item, self._update_totals, self.i18n, self.colors)
        row.grid(row=idx, column=0, sticky="ew", pady=2)
        if desc:
            row.desc.insert(0, desc)
        if qty:
            row.qty.insert(0, qty)
        if price:
            row.price.insert(0, price)
        self.item_rows.append(row)
        self._update_totals()

    def _delete_item(self, row):
        if len(self.item_rows) <= 1:
            messagebox.showwarning(self.i18n.t("warning"), self.i18n.t("at_least_one_item"))
            return
        row.destroy()
        self.item_rows.remove(row)
        for i, r in enumerate(self.item_rows):
            r.index = i
        self._update_totals()

    def _update_totals(self):
        if not hasattr(self, "lbl_subtotal"):
                                                                             
                                                                           
                                                                   
            return

        subtotal = 0
        for row in self.item_rows:
            _, _, _, total = row.get_data()
            subtotal += total

        try:
            tax_pct = float(self.tax_entry.get().strip().replace(",", ".") or "0")
        except Exception:
            tax_pct = 0

        tax = subtotal * tax_pct / 100
        grand = subtotal + tax
        cur = self.currency

        try:
            self.lbl_subtotal.configure(text=f"{cur}{subtotal:,.2f}")
            self.lbl_tax.configure(text=f"{cur}{tax:,.2f}")
            self.lbl_total.configure(text=f"{cur}{grand:,.2f}")

            rate_display = int(tax_pct) if tax_pct == int(tax_pct) else tax_pct
            self.lbl_tax_caption.configure(text=self.i18n.t("tax_label", rate=rate_display))
        except Exception:
                                                                        
                                                                          
                                                                           
                                                          
            pass

    def _pick_logo(self):
        t = self.i18n.t
        path = filedialog.askopenfilename(
            title=t("select_logo"),
            filetypes=[(t("images"), "*.png *.jpg *.jpeg *.bmp *.gif")])
        if path:
            self.logo_path = path
            self.logo_lbl.configure(text=f"✓ {os.path.basename(path)}")

    def _pick_accent(self):
        color = colorchooser.askcolor(color=self.accent_color, title=self.i18n.t("select_accent_color"))
        if color[1]:
            self.accent_color = color[1]
            self._rebuild_ui()

    def _save_sender(self):
        try:
            tax = float(self.tax_entry.get().strip().replace(",", ".") or "20")
        except Exception:
            tax = 20
        self.settings.update({
            "sender_name": self.sender_name.get().strip(),
            "sender_addr": self.sender_addr.get().strip(),
            "sender_email": self.sender_email.get().strip(),
            "sender_phone": self.sender_phone.get().strip(),
            "accent": self.accent_color,
            "currency": self.currency_var.get(),
            "tax_rate": tax,
            "logo_path": self.logo_path,
            "language": self.i18n.lang,
            "appearance": self.appearance_mode,
        })
        save_settings(self.settings)
        messagebox.showinfo(self.i18n.t("saved"), self.i18n.t("saved_msg"))

    def _restore_sender(self):
        s = self.settings
        for attr, key in [("sender_name", "sender_name"), ("sender_addr", "sender_addr"),
                           ("sender_email", "sender_email"), ("sender_phone", "sender_phone")]:
            if getattr(self, attr).get().strip():
                continue
                                                                             
                                                                         
                                                                           
            value = self._form_state.get(attr) or s.get(key)
            if value:
                getattr(self, attr).insert(0, value)

    def _collect_data(self):
        items = []
        for row in self.item_rows:
            desc, qty, price, total = row.get_data()
            if desc:
                items.append((desc, qty, price, total))

        try:
            tax_pct = float(self.tax_entry.get().strip().replace(",", ".") or "0")
        except Exception:
            tax_pct = 0

        subtotal = sum(tt for _, _, _, tt in items)
        tax_amt = subtotal * tax_pct / 100
        grand = subtotal + tax_amt

        return {
            "sender_name": self.sender_name.get().strip(),
            "sender_addr": self.sender_addr.get().strip(),
            "sender_email": self.sender_email.get().strip(),
            "sender_phone": self.sender_phone.get().strip(),
            "client_name": self.client_name.get().strip(),
            "client_email": self.client_email.get().strip(),
            "client_addr": self.client_addr.get().strip(),
            "client_inn": self.client_inn.get().strip(),
            "inv_number": self.inv_number.get().strip() or "001",
            "inv_date": self.inv_date.get().strip(),
            "inv_due": self.inv_due.get().strip(),
            "inv_project": self.inv_project.get().strip(),
            "notes": self.notes.get("0.0", "end").strip(),
            "items": items,
            "subtotal": subtotal,
            "tax_pct": tax_pct,
            "tax_amt": tax_amt,
            "grand": grand,
            "currency": self.currency_var.get(),
            "accent": self.accent_color,
            "logo_path": self.logo_path,
            "lang": self.i18n.lang,
        }

    def _preview(self):
        t = self.i18n.t
        data = self._collect_data()
        if not data["items"]:
            messagebox.showwarning(t("warning"), t("no_items_warning"))
            return

        win = ctk.CTkToplevel(self)
        win.title(t("preview_title", num=data['inv_number']))
        win.geometry("680x840")
        win.configure(fg_color=self.colors["card"])
        win.grab_set()

        ctk.CTkLabel(win, text=t("preview_heading"),
                     font=ctk.CTkFont("Segoe UI", 16, "bold"),
                     text_color=self.colors["text"]).pack(pady=(20, 0))
        sub_lbl = ctk.CTkLabel(win, text=t("preview_sub"),
                                font=ctk.CTkFont("Segoe UI", 12), text_color=self.colors["text2"])
        sub_lbl.pack(pady=(2, 12))

        content_frame = ctk.CTkFrame(win, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20)

        loading_lbl = ctk.CTkLabel(content_frame, text=t("generating_preview"),
                                    font=ctk.CTkFont("Segoe UI", 13), text_color=self.colors["text2"])
        loading_lbl.pack(pady=40)

        close_btn = ctk.CTkButton(win, text=f"✕  {t('close')}", height=38, width=160,
                                   font=ctk.CTkFont("Segoe UI", 13),
                                   fg_color="transparent", border_width=1,
                                   border_color=self.colors["border"], text_color=self.colors["text2"],
                                   hover_color=self.colors["bg"], corner_radius=8,
                                   command=win.destroy)
        close_btn.pack(pady=(8, 20))

        def render_and_show():
            buf = io.BytesIO()
            try:
                _render_pdf(data, buf, self.i18n)
                buf.seek(0)
            except Exception as e:
                loading_lbl.configure(text=t("error") + f": {e}")
                return

            try:
                rendered = False
                try:
                    import importlib
                    pdf2image = importlib.import_module("pdf2image")
                    images = pdf2image.convert_from_bytes(buf.getvalue(), dpi=120, first_page=1, last_page=1)
                    img = images[0]
                    w, h = img.size
                    max_w = 620
                    if w > max_w:
                        ratio = max_w / w
                        img = img.resize((max_w, int(h * ratio)), Image.LANCZOS)
                    tk_img = ImageTk.PhotoImage(img)
                    canvas = tk.Canvas(content_frame, width=img.width, height=img.height,
                                        bg="white", highlightthickness=0)
                    canvas.pack(pady=8)
                    canvas.create_image(0, 0, anchor="nw", image=tk_img)
                    canvas.image = tk_img
                    rendered = True
                except Exception:
                    rendered = False

                loading_lbl.destroy()

                if not rendered:
                    ctk.CTkLabel(content_frame, text=t("preview_unavailable"),
                                 font=ctk.CTkFont("Segoe UI", 14),
                                 text_color=self.colors["text2"], justify="center").pack(pady=40)
            except Exception:
                try:
                    loading_lbl.configure(text=t("preview_unavailable"))
                except Exception:
                    pass

        win.after(60, render_and_show)

    def _generate_pdf(self):
        t = self.i18n.t
        data = self._collect_data()
        if not data["items"]:
            messagebox.showwarning(t("warning"), t("no_items_warning"))
            return
        if not data["client_name"]:
            messagebox.showwarning(t("no_client_warning"), t("no_client_msg"))
            return

        default_name = f"Invoice_{data['inv_number']}_{data['client_name']}.pdf".replace(" ", "_")
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[(t("pdf_file"), "*.pdf")],
            title=t("save_invoice_as"))
        if not path:
            return

        try:
            _render_pdf(data, path, self.i18n)
            self._add_to_history(data, path)
            messagebox.showinfo(t("done"),
                                 t("done_msg", path=path, num=data['inv_number'],
                                   currency=data['currency'], amount=f"{data['grand']:,.2f}"))
            if sys.platform == "win32":
                os.startfile(path)
        except Exception as e:
            messagebox.showerror(t("error"), t("error_pdf_msg", err=e))

    def _add_to_history(self, data, pdf_path):
        """Record a freshly generated invoice in the history list with
        status 'unpaid', persisting it to disk immediately."""
        entry = {
            "id": str(uuid.uuid4()),
            "inv_number": data["inv_number"],
            "client_name": data["client_name"],
            "date": data["inv_date"],
            "due_date": data["inv_due"],
            "currency": data["currency"],
            "grand": data["grand"],
            "status": STATUS_UNPAID,
            "pdf_path": pdf_path,
            "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        self.history.insert(0, entry)                
        save_history(self.history)

    def _set_history_status(self, entry_id, new_status):
        for entry in self.history:
            if entry.get("id") == entry_id:
                entry["status"] = new_status
                break
        save_history(self.history)

    def _delete_history_entry(self, entry_id):
        entry = next((e for e in self.history if e.get("id") == entry_id), None)
        if entry is None:
            return
        t = self.i18n.t
        if not messagebox.askyesno(
                t("delete_entry_confirm_title"),
                t("delete_entry_confirm_msg", num=entry.get("inv_number", "")),
        ):
            return
        self.history = [e for e in self.history if e.get("id") != entry_id]
        save_history(self.history)
        self._rebuild_ui()

    def _open_history_pdf(self, entry):
        t = self.i18n.t
        path = entry.get("pdf_path", "")
        if not path or not os.path.exists(path):
            messagebox.showwarning(t("file_missing"), t("file_missing_msg", path=path or "—"))
            return
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                import subprocess
                subprocess.Popen(["open", path])
            else:
                import subprocess
                subprocess.Popen(["xdg-open", path])
        except Exception as e:
            messagebox.showerror(t("error"), str(e))


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _render_pdf(data, output, i18n):
    t = i18n.t
    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    accent_rgb = hex_to_rgb(data.get("accent", ACCENT))
    accent_color_rl = colors.Color(*accent_rgb)
    accent_light = colors.Color(accent_rgb[0], accent_rgb[1], accent_rgb[2], 0.08)

    styles = getSampleStyleSheet()
    body_font = PDF_FONT_REGULAR
    bold_font = PDF_FONT_BOLD

    def sty(name, **kw):
        base = kw.pop("parent", "Normal")
        if "fontName" not in kw:
            kw["fontName"] = body_font
        s = ParagraphStyle(name, parent=styles[base], **kw)
        return s

    story = []

                                                                               
    left_parts = []
    logo_path = data.get("logo_path", "")
    if logo_path and os.path.exists(logo_path):
        try:
            from reportlab.platypus import Image as RLImage
            img = Image.open(logo_path)
            ow, oh = img.size
            target_h = 18 * mm
            target_w = ow * target_h / oh
            if target_w > 50 * mm:
                target_w = 50 * mm
                target_h = oh * target_w / ow
            left_parts.append(RLImage(logo_path, width=target_w, height=target_h))
            left_parts.append(Spacer(1, 3 * mm))
        except Exception:
            pass

    if data["sender_name"]:
        left_parts.append(Paragraph(data["sender_name"],
                                     sty("sname", fontSize=14, fontName=bold_font,
                                         textColor=colors.Color(0.06, 0.09, 0.16))))
    for field in [data["sender_addr"], data["sender_email"], data["sender_phone"]]:
        if field:
            left_parts.append(Paragraph(field, sty("sfield", fontSize=9,
                                                     textColor=colors.Color(0.39, 0.45, 0.55), leading=13)))

    left_cell = left_parts if left_parts else [Paragraph("", styles["Normal"])]

    acc_hex = data.get("accent", ACCENT).lstrip("#")
    inv_label = Paragraph(f"<font color='#{acc_hex}'>{t('pdf_invoice_word')}</font>",
                           sty("invlabel", fontSize=28, leading=34, fontName=bold_font, alignment=TA_RIGHT))
    inv_num = Paragraph(f"<font color='#{acc_hex}'>№ {data['inv_number']}</font>",
                         sty("invnum", fontSize=14, leading=18, alignment=TA_RIGHT))

    meta_lines = []
    for lbl, val in [(t("pdf_date"), data["inv_date"]), (t("pdf_due"), data["inv_due"]),
                      (t("pdf_project"), data["inv_project"])]:
        if val:
            meta_lines.append(Paragraph(f"<b>{lbl}</b>  {val}",
                                         sty("meta", fontSize=9, alignment=TA_RIGHT,
                                             textColor=colors.Color(0.39, 0.45, 0.55), leading=14)))

    right_cell = [inv_label, Spacer(1, 2 * mm), inv_num, Spacer(1, 4 * mm)] + meta_lines

    header_tbl = Table([[left_cell, right_cell]], colWidths=[85 * mm, 85 * mm])
    header_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 6 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.Color(0.89, 0.91, 0.94)))
    story.append(Spacer(1, 6 * mm))

                                                                                
    def party_cell(title, name, *fields):
        parts = [Paragraph(title, sty("ptitle", fontSize=8, fontName=bold_font,
                                      textColor=accent_color_rl, spaceAfter=3))]
        if name:
            parts.append(Paragraph(name, sty("pname", fontSize=11, fontName=bold_font,
                                              textColor=colors.Color(0.06, 0.09, 0.16), spaceAfter=2)))
        for f in fields:
            if f:
                parts.append(Paragraph(f, sty("pf", fontSize=9,
                                               textColor=colors.Color(0.39, 0.45, 0.55), leading=13)))
        return parts

    parties = Table([[
        party_cell(t("pdf_from"), data["sender_name"], data["sender_addr"], data["sender_email"], data["sender_phone"]),
        party_cell(t("pdf_to"), data["client_name"], data["client_addr"], data["client_inn"], data["client_email"])
    ]], colWidths=[85 * mm, 85 * mm])
    parties.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(parties)
    story.append(Spacer(1, 8 * mm))

                                                                                
    cur = data["currency"]
    col_widths = [8 * mm, 85 * mm, 20 * mm, 28 * mm, 29 * mm]

    def hp(txt, align=TA_LEFT):
        return Paragraph(f"<b>{txt}</b>", sty("th", fontSize=9, fontName=bold_font,
                                               alignment=align, textColor=colors.white))

    def cp(txt, align=TA_LEFT, bold=False):
        fn = bold_font if bold else body_font
        return Paragraph(txt, sty("td", fontSize=10, alignment=align,
                                   fontName=fn, textColor=colors.Color(0.06, 0.09, 0.16), leading=13))

    header_row = [hp(t("pdf_no")), hp(t("pdf_description")), hp(t("pdf_qty"), TA_CENTER),
                  hp(t("pdf_price", cur=cur), TA_RIGHT), hp(t("pdf_amount", cur=cur), TA_RIGHT)]

    table_data = [header_row]
    for i, (desc, qty, price, total) in enumerate(data["items"]):
        qty_str = str(int(qty)) if qty == int(qty) else f"{qty:.2f}"
        table_data.append([
            cp(str(i + 1), TA_CENTER),
            cp(desc),
            cp(qty_str, TA_CENTER),
            cp(f"{price:,.2f}", TA_RIGHT),
            cp(f"{total:,.2f}", TA_RIGHT, bold=True),
        ])

    items_tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
    ts = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), accent_color_rl),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.Color(0.97, 0.98, 0.99)]),
        ("FONTNAME", (0, 0), (-1, 0), bold_font),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.89, 0.91, 0.94)),
        ("ROUNDEDCORNERS", [4]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ])
    items_tbl.setStyle(ts)
    story.append(items_tbl)
    story.append(Spacer(1, 6 * mm))

                                                                                
    totals = []
    totals.append([Paragraph(t("pdf_subtotal"), sty("tl", fontSize=10, textColor=colors.Color(0.39, 0.45, 0.55))),
                   Paragraph(f"{cur}{data['subtotal']:,.2f}", sty("tv", fontSize=10, alignment=TA_RIGHT,
                                                                   textColor=colors.Color(0.06, 0.09, 0.16)))])
    if data["tax_pct"]:
        rate_display = data['tax_pct']
        rate_str = f"{rate_display:.0f}" if rate_display == int(rate_display) else f"{rate_display}"
        totals.append([Paragraph(t("pdf_tax", rate=rate_str),
                                  sty("tl2", fontSize=10, textColor=colors.Color(0.39, 0.45, 0.55))),
                       Paragraph(f"{cur}{data['tax_amt']:,.2f}", sty("tv2", fontSize=10, alignment=TA_RIGHT,
                                                                      textColor=colors.Color(0.06, 0.09, 0.16)))])
    totals.append([Paragraph(f"<b>{t('pdf_total')}</b>", sty("tgt", fontSize=13, fontName=bold_font,
                                                              textColor=accent_color_rl)),
                   Paragraph(f"<b>{cur}{data['grand']:,.2f}</b>",
                             sty("tgv", fontSize=13, fontName=bold_font,
                                 alignment=TA_RIGHT, textColor=accent_color_rl))])

    totals_tbl = Table(totals, colWidths=[60 * mm, 40 * mm])
    totals_tbl.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, -1), "RIGHT"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEABOVE", (0, -1), (-1, -1), 0.5, colors.Color(0.89, 0.91, 0.94)),
        ("BACKGROUND", (0, -1), (-1, -1), accent_light),
        ("LEFTPADDING", (0, -1), (-1, -1), 8),
        ("RIGHTPADDING", (0, -1), (-1, -1), 8),
        ("ROUNDEDCORNERS", [4]),
    ]))

    totals_wrapper = Table([[None, totals_tbl]], colWidths=[70 * mm, 100 * mm])
    totals_wrapper.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(totals_wrapper)

                                                                                
    if data["notes"]:
        story.append(Spacer(1, 8 * mm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.Color(0.89, 0.91, 0.94)))
        story.append(Spacer(1, 4 * mm))
        story.append(Paragraph(t("pdf_notes_title"), sty("nlbl", fontSize=8,
                                                          fontName=bold_font,
                                                          textColor=accent_color_rl, spaceAfter=3)))
                                                                            
                                                                       
        safe_notes = (data["notes"]
                      .replace("&", "&amp;")
                      .replace("<", "&lt;")
                      .replace(">", "&gt;")
                      .replace("\n", "<br/>"))
        story.append(Paragraph(safe_notes,
                                sty("notes", fontSize=9, textColor=colors.Color(0.39, 0.45, 0.55), leading=14)))

                                                                                
    story.append(Spacer(1, 10 * mm))
    story.append(HRFlowable(width="100%", thickness=0.3, color=colors.Color(0.89, 0.91, 0.94)))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(t("pdf_footer"),
                            sty("footer", fontSize=8, alignment=TA_CENTER,
                                textColor=colors.Color(0.75, 0.79, 0.85))))

    doc.build(story)


if __name__ == "__main__":
    app = InvoiceApp()
    app.mainloop()