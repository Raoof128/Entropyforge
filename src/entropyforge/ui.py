# -------------------------------------------------------------------------- //
# UI — CUSTOMTKINTER //
# -------------------------------------------------------------------------- //

from __future__ import annotations

import contextlib
import logging
from collections.abc import Callable
from tkinter import TclError, messagebox
from typing import Any, Literal, TypeAlias

import customtkinter as ctk

from entropyforge.config import save_settings
from entropyforge.crypto_core import (
    MAX_ALPHANUMERIC_LENGTH,
    MAX_HEX_BYTES,
    CryptoCoreError,
    entropy_bits_alphanumeric,
    entropy_bits_hex_key,
    entropy_bits_uniform_range,
    generate_alphanumeric,
    generate_hex_key,
    generate_secure_int_inclusive,
    paranoid_hex_bytes,
    paranoid_integer_range,
    paranoid_password_length,
    parse_positive_int,
    parse_strict_int,
)
from entropyforge.i18n import is_rtl, load_locale, t

logger = logging.getLogger("entropyforge")

_MODE_PASSWORD = "password"
_MODE_HEX = "hex"
_MODE_INTEGERS = "integers"

_ENTROPY_CAP_BITS = 256.0
_BUTTON_MIN_HEIGHT = 44
_OUTPUT_MIN_HEIGHT = 120
_NARROW_BREAKPOINT_PX = 480

ParsedRequest: TypeAlias = (
    tuple[Literal["password"], int]
    | tuple[Literal["hex"], int]
    | tuple[Literal["integers"], int, int]
)


def _hint_label(
    parent: ctk.CTkFrame,
    key: str,
    *,
    rtl: bool,
    **kwargs: object,
) -> ctk.CTkLabel:
    text = t(key).format(**kwargs) if kwargs else t(key)
    anchor = "e" if rtl else "w"
    justify = "right" if rtl else "left"
    return ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(size=11),
        text_color=("gray60", "gray55"),
        anchor=anchor,
        justify=justify,
    )


def _mode_values() -> tuple[str, ...]:
    return (_MODE_PASSWORD, _MODE_HEX, _MODE_INTEGERS)


def _mode_label(mode: str) -> str:
    if mode == _MODE_PASSWORD:
        return t("mode.password")
    if mode == _MODE_HEX:
        return t("mode.hex")
    if mode == _MODE_INTEGERS:
        return t("mode.integers")
    return mode


def run_app(settings: dict[str, Any]) -> None:
    if settings.get("high_contrast"):
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    rtl = is_rtl()

    root = ctk.CTk()
    root.title(t("app.title"))
    root.geometry("700x620")
    root.minsize(560, 500)

    outer = ctk.CTkFrame(root)
    outer.pack(fill="both", expand=True, padx=16, pady=16)

    banner_frame: ctk.CTkFrame | None = None
    if not settings.get("first_run_banner_dismissed", False):
        banner_frame = ctk.CTkFrame(outer)
        banner_frame.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(
            banner_frame,
            text=t("banner.text"),
            anchor="e" if rtl else "w",
            justify="right" if rtl else "left",
            wraplength=640,
        ).pack(fill="x", padx=8, pady=8)
        bf = banner_frame

        def _dismiss_banner() -> None:
            settings["first_run_banner_dismissed"] = True
            save_settings(settings)
            bf.pack_forget()

        ctk.CTkButton(
            bf,
            text=t("banner.dismiss"),
            command=_dismiss_banner,
            height=_BUTTON_MIN_HEIGHT - 8,
        ).pack(anchor="w" if rtl else "e", padx=8, pady=(0, 8))

    main = ctk.CTkFrame(outer)
    main.pack(fill="both", expand=True)
    main.grid_columnconfigure(0, weight=1)
    main.grid_rowconfigure(4, weight=1)

    mode_section = ctk.CTkFrame(main, fg_color="transparent")
    mode_section.grid(row=0, column=0, sticky="ew", pady=(0, 8))
    mode_section.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        mode_section,
        text=t("label.generation_mode"),
        anchor="e" if rtl else "w",
    ).grid(row=0, column=0, sticky="e" if rtl else "w")

    mode_row = ctk.CTkFrame(mode_section, fg_color="transparent")
    mode_row.grid(row=1, column=0, sticky="ew", pady=(6, 0))

    mode_var = ctk.StringVar(value=_MODE_PASSWORD)

    params_frame = ctk.CTkFrame(main)
    params_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
    params_frame.grid_columnconfigure(0, weight=1)

    pw_row = ctk.CTkFrame(params_frame, fg_color="transparent")
    pw_top = ctk.CTkFrame(pw_row, fg_color="transparent")
    pw_top.pack(fill="x")
    pw_len_entry = ctk.CTkEntry(pw_top, width=120, height=_BUTTON_MIN_HEIGHT - 8)
    pw_len_entry.insert(0, t("default.password_length"))
    if rtl:
        pw_len_entry.pack(side="right", padx=(8, 0))
        ctk.CTkLabel(pw_top, text=t("label.password_length"), anchor="e").pack(
            side="right",
        )
    else:
        ctk.CTkLabel(pw_top, text=t("label.password_length")).pack(
            side="left",
            padx=(0, 8),
        )
        pw_len_entry.pack(side="left")
    _hint_label(
        pw_row,
        "hint.password_length_max",
        rtl=rtl,
        max=MAX_ALPHANUMERIC_LENGTH,
    ).pack(fill="x", pady=(6, 0))

    hex_row = ctk.CTkFrame(params_frame, fg_color="transparent")
    hex_top = ctk.CTkFrame(hex_row, fg_color="transparent")
    hex_top.pack(fill="x")
    hex_bytes_entry = ctk.CTkEntry(hex_top, width=120, height=_BUTTON_MIN_HEIGHT - 8)
    hex_bytes_entry.insert(0, t("default.hex_bytes"))
    if rtl:
        hex_bytes_entry.pack(side="right", padx=(8, 0))
        ctk.CTkLabel(hex_top, text=t("label.hex_bytes"), anchor="e").pack(side="right")
    else:
        ctk.CTkLabel(hex_top, text=t("label.hex_bytes")).pack(side="left", padx=(0, 8))
        hex_bytes_entry.pack(side="left")
    _hint_label(hex_row, "hint.hex_bytes_max", rtl=rtl, max=MAX_HEX_BYTES).pack(
        fill="x",
        pady=(6, 0),
    )

    int_row = ctk.CTkFrame(params_frame, fg_color="transparent")
    int_top = ctk.CTkFrame(int_row, fg_color="transparent")
    int_top.pack(fill="x")
    min_entry = ctk.CTkEntry(int_top, width=100, height=_BUTTON_MIN_HEIGHT - 8)
    min_entry.insert(0, t("default.min_int"))
    max_entry = ctk.CTkEntry(int_top, width=100, height=_BUTTON_MIN_HEIGHT - 8)
    max_entry.insert(0, t("default.max_int"))
    if rtl:
        max_entry.pack(side="right", padx=(8, 0))
        ctk.CTkLabel(int_top, text=t("label.max"), anchor="e").pack(side="right", padx=(0, 8))
        min_entry.pack(side="right", padx=(12, 0))
        ctk.CTkLabel(int_top, text=t("label.min"), anchor="e").pack(side="right", padx=(0, 8))
    else:
        ctk.CTkLabel(int_top, text=t("label.min")).pack(side="left", padx=(0, 8))
        min_entry.pack(side="left", padx=(0, 12))
        ctk.CTkLabel(int_top, text=t("label.max")).pack(side="left", padx=(0, 8))
        max_entry.pack(side="left")
    _hint_label(int_row, "hint.integers_range", rtl=rtl).pack(fill="x", pady=(6, 0))

    current_mode: list[str] = [_MODE_PASSWORD]

    def _focus_for_mode(mode: str) -> None:
        if mode == _MODE_PASSWORD:
            root.after(10, pw_len_entry.focus_set)
        elif mode == _MODE_HEX:
            root.after(10, hex_bytes_entry.focus_set)
        else:
            root.after(10, min_entry.focus_set)

    def _on_mode_change(mode: str) -> None:
        current_mode[0] = mode
        mode_var.set(mode)
        for child in params_frame.winfo_children():
            child.pack_forget()
        if mode == _MODE_PASSWORD:
            pw_row.pack(fill="x", pady=4)
        elif mode == _MODE_HEX:
            hex_row.pack(fill="x", pady=4)
        else:
            int_row.pack(fill="x", pady=4)
        _focus_for_mode(mode)

    _mode_order = list(reversed(_mode_values())) if rtl else list(_mode_values())
    _ps = "right" if rtl else "left"
    _pad_m = (16, 0) if rtl else (0, 16)
    for m in _mode_order:
        ctk.CTkRadioButton(
            mode_row,
            text=_mode_label(m),
            variable=mode_var,
            value=m,
            command=lambda mm=m: _on_mode_change(mm),
            font=ctk.CTkFont(size=13),
        ).pack(side=_ps, padx=_pad_m)

    _on_mode_change(_MODE_PASSWORD)

    preset_row = ctk.CTkFrame(main, fg_color="transparent")
    preset_row.grid(row=2, column=0, sticky="ew", pady=(0, 8))
    ctk.CTkLabel(
        preset_row,
        text=t("label.presets"),
        anchor="e" if rtl else "w",
    ).pack(
        side="right" if rtl else "left",
        padx=(12, 0) if rtl else (0, 12),
    )

    def _preset_password_16() -> None:
        _on_mode_change(_MODE_PASSWORD)
        pw_len_entry.delete(0, "end")
        pw_len_entry.insert(0, "16")

    def _preset_hex_wpa() -> None:
        _on_mode_change(_MODE_HEX)
        hex_bytes_entry.delete(0, "end")
        hex_bytes_entry.insert(0, "32")

    def _preset_dice() -> None:
        _on_mode_change(_MODE_INTEGERS)
        min_entry.delete(0, "end")
        min_entry.insert(0, "1")
        max_entry.delete(0, "end")
        max_entry.insert(0, "6")

    _preset_side = "right" if rtl else "left"
    _preset_pad = (8, 0) if rtl else (0, 8)
    _presets: list[tuple[str, Callable[[], None]]] = [
        ("preset.password_16", _preset_password_16),
        ("preset.hex_wpa", _preset_hex_wpa),
        ("preset.dice", _preset_dice),
    ]
    if rtl:
        _presets.reverse()
    for key, cmd in _presets:
        ctk.CTkButton(
            preset_row,
            text=t(key),
            command=cmd,
            height=_BUTTON_MIN_HEIGHT - 6,
        ).pack(side=_preset_side, padx=_preset_pad)

    out_header = ctk.CTkFrame(main, fg_color="transparent")
    out_header.grid(row=3, column=0, sticky="ew", pady=(0, 4))
    out_tools = ctk.CTkFrame(out_header, fg_color="transparent")
    out_label = ctk.CTkLabel(
        out_header,
        text=t("label.output"),
        anchor="e" if rtl else "w",
    )
    if rtl:
        out_header.grid_columnconfigure(1, weight=1)
        out_tools.grid(row=0, column=0, sticky="w")
        out_label.grid(row=0, column=1, sticky="e")
    else:
        out_header.grid_columnconfigure(0, weight=1)
        out_label.grid(row=0, column=0, sticky="w")
        out_tools.grid(row=0, column=1, sticky="e")

    output_box = ctk.CTkTextbox(
        main,
        height=_OUTPUT_MIN_HEIGHT,
        wrap="char",
        font=ctk.CTkFont(size=13),
    )
    output_box.grid(row=4, column=0, sticky="nsew", pady=(0, 8))
    if rtl:
        with contextlib.suppress(AttributeError, TclError):
            output_box._textbox.configure(autoseparators=True)

    hide_var = ctk.BooleanVar(value=False)
    plain_output: list[str | None] = [None]

    def _refresh_output_display() -> None:
        plain = plain_output[0]
        output_box.delete("1.0", "end")
        if plain is None:
            return
        if hide_var.get():
            output_box.insert("1.0", "•" * len(plain))
        else:
            output_box.insert("1.0", plain)

    def _toggle_hide() -> None:
        _refresh_output_display()

    hide_switch = ctk.CTkSwitch(
        out_tools,
        text=t("label.hide_output"),
        variable=hide_var,
        command=_toggle_hide,
    )

    def _clear_output() -> None:
        plain_output[0] = None
        output_box.delete("1.0", "end")
        entropy_text.set(f"{t('entropy.label')}: {t('common.em_dash')}")
        entropy_bar.set(0)
        status_var.set(t("status.cleared"))

    def _parse_request() -> ParsedRequest:
        mode = mode_var.get()
        if mode == _MODE_PASSWORD:
            n = parse_positive_int(pw_len_entry.get(), error_key="error.length_invalid")
            return ("password", n)
        if mode == _MODE_HEX:
            nb = parse_positive_int(hex_bytes_entry.get(), error_key="error.hex_bytes_invalid")
            return ("hex", nb)
        lo = parse_strict_int(min_entry.get())
        hi = parse_strict_int(max_entry.get())
        return ("integers", lo, hi)

    def _paranoid_confirm(req: ParsedRequest) -> bool:
        if not settings.get("paranoid_confirm", True):
            return True
        if req[0] == "password":
            n = req[1]
            if not paranoid_password_length(n):
                return True
            return messagebox.askokcancel(
                t("dialog.paranoid.title"),
                t("dialog.paranoid.message_password").format(length=n),
                parent=root,
            )
        if req[0] == "hex":
            b = req[1]
            if not paranoid_hex_bytes(b):
                return True
            return messagebox.askokcancel(
                t("dialog.paranoid.title"),
                t("dialog.paranoid.message_hex").format(bytes=b),
                parent=root,
            )
        lo, hi = req[1], req[2]
        if not paranoid_integer_range(lo, hi):
            return True
        span = hi - lo + 1
        return messagebox.askokcancel(
            t("dialog.paranoid.title"),
            t("dialog.paranoid.message_integers").format(span=span),
            parent=root,
        )

    entropy_block = ctk.CTkFrame(main, fg_color="transparent")
    entropy_block.grid(row=5, column=0, sticky="ew", pady=(0, 8))
    entropy_block.grid_columnconfigure(0, weight=1)

    entropy_row = ctk.CTkFrame(entropy_block, fg_color="transparent")
    entropy_row.pack(fill="x")
    entropy_row.grid_columnconfigure(0, weight=1)

    entropy_text = ctk.StringVar(
        value=f"{t('entropy.label')}: {t('common.em_dash')}",
    )
    entropy_label = ctk.CTkLabel(entropy_row, textvariable=entropy_text)
    entropy_bar = ctk.CTkProgressBar(entropy_row, width=220, height=16)
    entropy_bar.set(0)
    if rtl:
        entropy_bar.grid(row=0, column=0, sticky="w", padx=(0, 12))
        entropy_label.grid(row=0, column=1, sticky="e")
    else:
        entropy_label.grid(row=0, column=0, sticky="w")
        entropy_bar.grid(row=0, column=1, sticky="e", padx=(12, 0))

    _hint_label(entropy_block, "entropy.hint_bar", rtl=rtl).pack(fill="x", pady=(8, 0))

    layout_narrow = [False]

    def _apply_entropy_layout() -> None:
        w = root.winfo_width()
        if w < 120:
            return
        narrow = w < _NARROW_BREAKPOINT_PX
        if narrow == layout_narrow[0]:
            return
        layout_narrow[0] = narrow
        entropy_label.grid_forget()
        entropy_bar.grid_forget()
        if narrow:
            entropy_label.grid(row=0, column=0, sticky="ew")
            entropy_bar.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        else:
            entropy_row.grid_columnconfigure(0, weight=1)
            if rtl:
                entropy_bar.grid(row=0, column=0, sticky="w", padx=(0, 12))
                entropy_label.grid(row=0, column=1, sticky="e")
            else:
                entropy_label.grid(row=0, column=0, sticky="w")
                entropy_bar.grid(row=0, column=1, sticky="e", padx=(12, 0))

    root.bind("<Configure>", lambda _e: _apply_entropy_layout())

    status_var = ctk.StringVar(value=t("status.ready"))

    def _set_entropy_display(bits: float) -> None:
        entropy_text.set(f"{t('entropy.label')}: {bits:.2f}")
        ratio = min(1.0, max(0.0, bits / _ENTROPY_CAP_BITS))
        entropy_bar.set(ratio)

    clipboard_job: list[str | None] = [None]

    def _schedule_clipboard_clear() -> None:
        if clipboard_job[0] is not None:
            with contextlib.suppress(TclError, ValueError):
                root.after_cancel(clipboard_job[0])
            clipboard_job[0] = None
        secs = float(settings.get("clipboard_clear_seconds") or 0)
        if secs <= 0:
            return

        def _do_clear() -> None:
            with contextlib.suppress(TclError):
                root.clipboard_clear()
            clipboard_job[0] = None

        clipboard_job[0] = root.after(int(secs * 1000), _do_clear)

    def _generate() -> None:
        status_var.set(t("status.ready"))
        try:
            req = _parse_request()
        except CryptoCoreError as err:
            output_box.delete("1.0", "end")
            output_box.insert("1.0", t(err.message_key))
            entropy_text.set(f"{t('entropy.label')}: {t('common.em_dash')}")
            entropy_bar.set(0)
            plain_output[0] = None
            return

        if not _paranoid_confirm(req):
            status_var.set(t("status.ready"))
            return

        try:
            if req[0] == "password":
                n = req[1]
                out = generate_alphanumeric(n)
                bits = entropy_bits_alphanumeric(length=n)
            elif req[0] == "hex":
                nb = req[1]
                out = generate_hex_key(nb)
                bits = entropy_bits_hex_key(num_bytes=nb)
            else:
                lo, hi = req[1], req[2]
                out = str(generate_secure_int_inclusive(lo, hi))
                count = hi - lo + 1
                bits = entropy_bits_uniform_range(count=count)

            plain_output[0] = out
            hide_var.set(False)
            _refresh_output_display()
            _set_entropy_display(bits)
        except CryptoCoreError as err:
            plain_output[0] = None
            output_box.delete("1.0", "end")
            output_box.insert("1.0", t(err.message_key))
            entropy_text.set(f"{t('entropy.label')}: {t('common.em_dash')}")
            entropy_bar.set(0)
        except Exception:
            logger.exception("Generate failed")
            plain_output[0] = None
            status_var.set(t("error.unexpected"))

    _tool_side = "right" if rtl else "left"
    _tool_pad = (8, 0) if rtl else (0, 8)
    ctk.CTkButton(
        out_tools,
        text=t("button.clear"),
        command=_clear_output,
        height=_BUTTON_MIN_HEIGHT - 6,
        width=88,
    ).pack(side=_tool_side, padx=_tool_pad)
    ctk.CTkButton(
        out_tools,
        text=t("button.regenerate"),
        command=_generate,
        height=_BUTTON_MIN_HEIGHT - 6,
        width=120,
    ).pack(side=_tool_side, padx=_tool_pad)
    hide_switch.pack(side=_tool_side, padx=(0, 0))

    btn_row = ctk.CTkFrame(main, fg_color="transparent")
    btn_row.grid(row=6, column=0, sticky="ew", pady=(0, 4))

    gen_btn = ctk.CTkButton(
        btn_row,
        text=t("button.generate"),
        command=_generate,
        height=_BUTTON_MIN_HEIGHT,
    )
    _btn_side = "right" if rtl else "left"
    _btn_pad = (8, 0) if rtl else (0, 8)

    def _copy() -> None:
        plain = plain_output[0]
        text = plain if plain is not None else output_box.get("1.0", "end-1c")
        if not text.strip():
            status_var.set(t("status.copy_skipped_empty"))
            return
        try:
            root.clipboard_clear()
            root.clipboard_append(text)
            root.update()
            status_var.set(t("status.copied"))
            _schedule_clipboard_clear()
        except TclError:
            status_var.set(t("status.ready"))

    copy_btn = ctk.CTkButton(
        btn_row,
        text=t("button.copy"),
        command=_copy,
        height=_BUTTON_MIN_HEIGHT,
    )

    def _open_settings() -> None:
        win = ctk.CTkToplevel(root)
        win.title(t("settings.title"))
        win.geometry("420x360")
        win.transient(root)
        win.grab_set()

        loc_var = ctk.StringVar(value=str(settings.get("locale", "en")))
        _sa = "e" if rtl else "w"
        ctk.CTkLabel(win, text=t("settings.locale")).pack(anchor=_sa, padx=16, pady=(16, 4))
        ctk.CTkOptionMenu(
            win,
            values=["en", "ar"],
            variable=loc_var,
        ).pack(fill="x", padx=16)

        hc_var = ctk.BooleanVar(value=bool(settings.get("high_contrast")))
        ctk.CTkSwitch(win, text=t("settings.high_contrast"), variable=hc_var).pack(
            anchor=_sa,
            padx=16,
            pady=12,
        )

        par_var = ctk.BooleanVar(value=bool(settings.get("paranoid_confirm", True)))
        ctk.CTkSwitch(win, text=t("settings.paranoid"), variable=par_var).pack(
            anchor=_sa,
            padx=16,
            pady=8,
        )

        ctk.CTkLabel(win, text=t("settings.clipboard_clear")).pack(
            anchor=_sa,
            padx=16,
            pady=(12, 4),
        )
        clip_entry = ctk.CTkEntry(win)
        clip_entry.insert(0, str(settings.get("clipboard_clear_seconds", 0)))
        clip_entry.pack(fill="x", padx=16)

        def _save_settings_action() -> None:
            settings["locale"] = loc_var.get()
            settings["high_contrast"] = hc_var.get()
            settings["paranoid_confirm"] = par_var.get()
            try:
                settings["clipboard_clear_seconds"] = int(clip_entry.get().strip() or "0")
            except ValueError:
                settings["clipboard_clear_seconds"] = 0
            save_settings(settings)
            load_locale(str(settings["locale"]))
            if settings.get("high_contrast"):
                ctk.set_appearance_mode("light")
            else:
                ctk.set_appearance_mode("dark")
            status_var.set(t("settings.saved"))
            messagebox.showinfo(
                t("settings.title"),
                t("settings.restart_notice"),
                parent=win,
            )
            win.destroy()

        ctk.CTkButton(
            win,
            text=t("settings.save"),
            command=_save_settings_action,
            height=_BUTTON_MIN_HEIGHT - 4,
        ).pack(pady=20)

    settings_btn = ctk.CTkButton(
        btn_row,
        text=t("button.settings"),
        command=_open_settings,
        height=_BUTTON_MIN_HEIGHT,
    )
    if rtl:
        settings_btn.pack(side=_btn_side, padx=_btn_pad)
        copy_btn.pack(side=_btn_side, padx=_btn_pad)
        gen_btn.pack(side=_btn_side, padx=_btn_pad)
    else:
        gen_btn.pack(side=_btn_side, padx=_btn_pad)
        copy_btn.pack(side=_btn_side, padx=_btn_pad)
        settings_btn.pack(side=_btn_side, padx=_btn_pad)

    shortcut_hint = _hint_label(main, "hint.shortcuts", rtl=rtl)
    shortcut_hint.grid(row=7, column=0, sticky="ew", pady=(0, 4))

    status = ctk.CTkLabel(
        main,
        textvariable=status_var,
        anchor="e" if rtl else "w",
        text_color=("gray55", "gray60"),
        font=ctk.CTkFont(size=12),
    )
    status.grid(row=8, column=0, sticky="ew", pady=(4, 0))

    def _bind_enter(widget: ctk.CTkEntry) -> None:
        def _handler(_event: object) -> str:
            _generate()
            return "break"

        widget.bind("<Return>", _handler)

    for entry in (pw_len_entry, hex_bytes_entry, min_entry, max_entry):
        _bind_enter(entry)

    root.bind("<Command-Return>", lambda _e: _generate())
    root.bind("<Control-Return>", lambda _e: _generate())

    root.mainloop()
