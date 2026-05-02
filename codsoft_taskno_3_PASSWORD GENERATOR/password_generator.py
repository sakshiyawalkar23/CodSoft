import tkinter as tk
from tkinter import messagebox
import random
import string

# ─────────────────────────────────────────────
#  COLORS & FONTS
# ─────────────────────────────────────────────
BG      = "#0d0d0d"   # window background
CARD    = "#1e1e1e"   # entry / button background
ACCENT  = "#00e5ff"   # cyan highlight color
TEXT    = "#f0f0f0"   # main text
MUTED   = "#888888"   # secondary text
BORDER  = "#2a2a2a"   # divider / border color
GREEN   = "#00e676"   # copied / strong feedback

FONT_BIG   = ("Courier New", 18, "bold")
FONT_NORM  = ("Courier New", 10)
FONT_MONO  = ("Courier New", 12, "bold")
FONT_BTN   = ("Courier New", 10, "bold")
FONT_SMALL = ("Courier New", 8)

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_strength(password):
    """
    Rate password strength on a 0-4 scale.
    Returns (score, label_text, bar_color).
    """
    score = 0
    if len(password) >= 8:                              score += 1
    if len(password) >= 14:                             score += 1
    if any(c.isdigit() for c in password):              score += 1
    if any(c in string.punctuation for c in password):  score += 1

    labels = ["Weak",    "Fair",    "Good",    "Strong",  "Fortress"]
    colors = ["#ff1744", "#ff9100", "#ffea00", "#76ff03", GREEN]
    return score, labels[score], colors[score]


def copy_to_clipboard(root, text):
    """Copy text to the system clipboard."""
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()


# ─────────────────────────────────────────────
#  MAIN APPLICATION CLASS
# ─────────────────────────────────────────────

class PasswordGeneratorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("PASSFORGE")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # Center window on screen
        W, H = 480, 510
        sx = (root.winfo_screenwidth()  - W) // 2
        sy = (root.winfo_screenheight() - H) // 2
        root.geometry(f"{W}x{H}+{sx}+{sy}")

        self._build_ui()
        self.generate()   # show a password immediately on launch

    # ──────────────────────────────────────────
    #  BUILD ALL WIDGETS
    # ──────────────────────────────────────────

    def _build_ui(self):

        # ── HEADER ──────────────────────────────
        tk.Label(self.root, text="⬡ PASSFORGE", font=FONT_BIG,
                 fg=ACCENT, bg=BG).pack(pady=(12, 0))
        tk.Label(self.root, text="Password Generator", font=FONT_SMALL,
                 fg=MUTED, bg=BG).pack()

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=24, pady=8)

        # ── LENGTH SLIDER ───────────────────────
        self.length_var = tk.IntVar(value=16)

        length_row = tk.Frame(self.root, bg=BG)
        length_row.pack(fill="x", padx=24)
        tk.Label(length_row, text="Length:", font=FONT_NORM,
                 fg=MUTED, bg=BG).pack(side="left")

        # Shows the current numeric value next to the label
        self.len_label = tk.Label(length_row, text="16",
                                  font=("Courier New", 12, "bold"),
                                  fg=ACCENT, bg=BG, width=3, anchor="e")
        self.len_label.pack(side="right")

        tk.Scale(
            self.root, from_=4, to=64, orient="horizontal",
            variable=self.length_var, showvalue=False,
            bg=BG, fg=ACCENT, troughcolor="#252525",
            highlightthickness=0, bd=0, activebackground=ACCENT, sliderrelief="flat",
            command=lambda v: self.len_label.config(text=str(int(float(v))))
        ).pack(fill="x", padx=24, pady=(3, 2))

        # Quick-set preset buttons (click to jump to a length)
        preset_row = tk.Frame(self.root, bg=BG)
        preset_row.pack(pady=(0, 6))
        for val in [8, 12, 16, 24, 32, 64]:
            tk.Button(
                preset_row, text=str(val), font=FONT_SMALL,
                fg=MUTED, bg=CARD, bd=0, padx=7, pady=2, cursor="hand2",
                activebackground=ACCENT, activeforeground=BG,
                command=lambda v=val: [self.length_var.set(v),
                                       self.len_label.config(text=str(v))]
            ).pack(side="left", padx=2)

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=24, pady=6)

        # ── CHECKBOXES (Character Sets) ─────────
        tk.Label(self.root, text="Include:", font=FONT_NORM,
                 fg=MUTED, bg=BG).pack(anchor="w", padx=24)

        # Each BooleanVar controls whether that character type is included
        self.use_upper   = tk.BooleanVar(value=True)
        self.use_lower   = tk.BooleanVar(value=True)
        self.use_digits  = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.no_ambig    = tk.BooleanVar(value=False)  # strip O,0,l,I,1

        options = [
            (self.use_upper,   "A–Z  Uppercase"),
            (self.use_lower,   "a–z  Lowercase"),
            (self.use_digits,  "0–9  Numbers"),
            (self.use_symbols, "!@#  Symbols"),
            (self.no_ambig,    "⊘   Exclude ambiguous chars (O,0,l,I,1)"),
        ]

        check_frame = tk.Frame(self.root, bg=BG)
        check_frame.pack(anchor="w", padx=24, pady=(2, 0))

        for var, label in options:
            self._make_checkbox(check_frame, var, label)

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=24, pady=8)

        # ── PASSWORD OUTPUT BOX ─────────────────
        self.pwd_var = tk.StringVar()

        # Bordered card that holds the password entry
        out_card = tk.Frame(self.root, bg=CARD, highlightthickness=1,
                            highlightbackground=BORDER)
        out_card.pack(fill="x", padx=24)

        tk.Entry(
            out_card, textvariable=self.pwd_var, font=FONT_MONO,
            fg=TEXT, bg=CARD, bd=0, relief="flat",
            readonlybackground=CARD, state="readonly",
            justify="center", highlightthickness=0
        ).pack(fill="x", padx=12, pady=9)

        # Thin colored bar showing strength level
        bar_bg = tk.Frame(self.root, bg="#252525", height=4)
        bar_bg.pack(fill="x", padx=24)
        bar_bg.pack_propagate(False)
        self.strength_bar = tk.Frame(bar_bg, bg=ACCENT, height=4)
        self.strength_bar.place(x=0, y=0, height=4)

        # Strength text (e.g. "Strength: Strong")
        self.strength_label = tk.Label(self.root, text="", font=FONT_SMALL,
                                       fg=MUTED, bg=BG, anchor="w")
        self.strength_label.pack(anchor="w", padx=24, pady=(2, 4))

        # ── ACTION BUTTONS ──────────────────────
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill="x", padx=24, pady=(2, 0))

        # Generate button — solid cyan, most prominent
        tk.Button(
            btn_frame, text="⚡ GENERATE", font=FONT_BTN,
            fg=BG, bg=ACCENT, bd=0, relief="flat", pady=8, cursor="hand2",
            activebackground="#00bcd4", activeforeground=BG,
            command=self.generate
        ).pack(fill="x", pady=(0, 5))

        # Copy button — outlined style
        self.copy_btn = tk.Button(
            btn_frame, text="⧉ COPY TO CLIPBOARD", font=FONT_BTN,
            fg=ACCENT, bg=CARD, bd=0, relief="flat", pady=7, cursor="hand2",
            activebackground=BORDER, activeforeground=ACCENT,
            command=self._copy
        )
        self.copy_btn.pack(fill="x")

        # Small status line at the bottom
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.root, textvariable=self.status_var, font=FONT_SMALL,
                 fg=MUTED, bg=BG).pack(pady=5)

    # ──────────────────────────────────────────
    #  CUSTOM CHECKBOX WIDGET
    # ──────────────────────────────────────────

    def _make_checkbox(self, parent, var, label):
        """
        Build one toggle row with a clickable box icon and label.
        ▣ = checked (cyan),  ▢ = unchecked (grey)
        """
        row = tk.Frame(parent, bg=BG)
        row.pack(anchor="w", pady=1)

        box = tk.Label(row, font=("Courier New", 11), bg=BG, cursor="hand2",
                       text="▣" if var.get() else "▢",
                       fg=ACCENT if var.get() else MUTED)
        box.pack(side="left", padx=(0, 6))

        txt = tk.Label(row, text=label, font=FONT_NORM, fg=TEXT, bg=BG, cursor="hand2")
        txt.pack(side="left")

        def toggle(e=None):
            var.set(not var.get())
            box.config(text="▣" if var.get() else "▢",
                       fg=ACCENT if var.get() else MUTED)

        # Both the icon and text are clickable
        box.bind("<Button-1>", toggle)
        txt.bind("<Button-1>", toggle)

    # ──────────────────────────────────────────
    #  UPDATE STRENGTH BAR
    # ──────────────────────────────────────────

    def _update_strength(self, password):
        """Fill and color the strength bar based on password score."""
        score, label, color = get_strength(password)
        total = self.strength_bar.master.winfo_width()
        fill  = int(total * score / 4) if total > 1 else 0
        self.strength_bar.place(x=0, y=0, height=4, width=fill)
        self.strength_bar.config(bg=color)
        self.strength_label.config(text=f"Strength: {label}", fg=color)

    # ──────────────────────────────────────────
    #  GENERATE PASSWORD
    # ──────────────────────────────────────────

    def generate(self):
        length = self.length_var.get()

        # Step 1: Build pool from checked character sets
        charset = ""
        if self.use_upper.get():   charset += string.ascii_uppercase
        if self.use_lower.get():   charset += string.ascii_lowercase
        if self.use_digits.get():  charset += string.digits
        if self.use_symbols.get(): charset += string.punctuation

        if not charset:
            messagebox.showwarning("Nothing selected",
                                   "Please enable at least one character set.")
            return

        # Step 2: Strip ambiguous characters if option is on
        ambiguous = "O0lI1|`\"'" if self.no_ambig.get() else ""
        if ambiguous:
            charset = "".join(c for c in charset if c not in ambiguous)

        if not charset:
            messagebox.showwarning("Empty charset",
                                   "No characters left after removing ambiguous ones.")
            return

        # Step 3: Guarantee at least one char from each enabled set
        def filtered(chars):
            return "".join(c for c in chars if c not in ambiguous)

        guaranteed = []
        if self.use_upper.get()   and filtered(string.ascii_uppercase): guaranteed.append(random.choice(filtered(string.ascii_uppercase)))
        if self.use_lower.get()   and filtered(string.ascii_lowercase): guaranteed.append(random.choice(filtered(string.ascii_lowercase)))
        if self.use_digits.get()  and filtered(string.digits):          guaranteed.append(random.choice(filtered(string.digits)))
        if self.use_symbols.get() and filtered(string.punctuation):     guaranteed.append(random.choice(filtered(string.punctuation)))

        # Step 4: Fill the rest randomly, shuffle, and join
        remaining = [random.choice(charset) for _ in range(length - len(guaranteed))]
        all_chars = guaranteed + remaining
        random.shuffle(all_chars)
        password = "".join(all_chars)

        # Step 5: Display and update the strength indicator
        self.pwd_var.set(password)
        self.root.update_idletasks()
        self._update_strength(password)
        self.status_var.set(f"✓  {length}-character password generated")

    # ──────────────────────────────────────────
    #  COPY TO CLIPBOARD
    # ──────────────────────────────────────────

    def _copy(self):
        password = self.pwd_var.get()
        if not password:
            self.status_var.set("Generate a password first.")
            return

        copy_to_clipboard(self.root, password)
        self.status_var.set("✔  Copied to clipboard!")

        # Flash the button green, then revert after 1.8 seconds
        self.copy_btn.config(text="✔  COPIED!", fg=GREEN, bg="#0a2a1a")
        self.root.after(1800, lambda: self.copy_btn.config(
            text="⧉ COPY TO CLIPBOARD", fg=ACCENT, bg=CARD))


# ─────────────────────────────────────────────
#  ENTRY POINT — runs when you execute the file
# ─────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app  = PasswordGeneratorApp(root)
    root.mainloop()
