from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
from datetime import datetime

# Import enhanced modules
from student import Student
from train import Train
from face_recognition import Face_Recognitions
from attendece import Attendance

# ─────────────────────────────────────────────
#  COLOUR PALETTE  (unified across all modules)
# ─────────────────────────────────────────────
BG_DARK        = "#0A0E1A"
BG_CARD        = "#111827"
BG_SURFACE     = "#1A2235"
ACCENT_CYAN    = "#00D4FF"
ACCENT_TEAL    = "#00F5C4"
ACCENT_PURPLE  = "#7C3AED"
TEXT_PRIMARY   = "#F0F4FF"
TEXT_SECONDARY = "#8B9DC3"
TEXT_DIM       = "#4B5E82"
BORDER_GLOW    = "#1E3A5F"
INPUT_BG       = "#0D1526"

FONT_TITLE   = ("Courier New", 26, "bold")
FONT_SECTION = ("Courier New", 11, "bold")
FONT_LABEL   = ("Consolas", 10, "bold")
FONT_BTN     = ("Courier New", 11, "bold")
FONT_SMALL   = ("Consolas", 9)
FONT_CARD    = ("Courier New", 10, "bold")


# ─────────────────────────────────────────────
#  MODULE CARD CONFIG
# ─────────────────────────────────────────────
MODULES = [
    {
        "key":   "student",
        "icon":  "👤",
        "title": "STUDENT DETAILS",
        "sub":   "Manage student records,\ncapture photo samples",
        "color": ACCENT_CYAN,
        "tag":   "CRUD",
        "cmd":   "student_details",
    },
    {
        "key":   "face",
        "icon":  "🔍",
        "title": "FACE DETECTOR",
        "sub":   "Live recognition engine,\nmark attendance in real-time",
        "color": ACCENT_TEAL,
        "tag":   "LIVE",
        "cmd":   "face_data",
    },
    {
        "key":   "attendance",
        "icon":  "📋",
        "title": "ATTENDANCE",
        "sub":   "View & export attendance\nreports and CSV logs",
        "color": "#FFA500",
        "tag":   "REPORT",
        "cmd":   "attendance_data",
    },
    {
        "key":   "help",
        "icon":  "💬",
        "title": "HELP DESK",
        "sub":   "Documentation, guides\nand system support",
        "color": "#FF6B6B",
        "tag":   "INFO",
        "cmd":   "help_desk",
    },
    {
        "key":   "train",
        "icon":  "⚡",
        "title": "TRAIN MODEL",
        "sub":   "Train LBPH classifier\nfrom captured face samples",
        "color": ACCENT_PURPLE,
        "tag":   "ML",
        "cmd":   "train_data",
    },
    {
        "key":   "photos",
        "icon":  "🖼",
        "title": "PHOTO SAMPLES",
        "sub":   "Browse captured face\nsample images in data/",
        "color": "#00D4FF",
        "tag":   "DATA",
        "cmd":   "open_ing",
    },
    {
        "key":   "developer",
        "icon":  "🛠",
        "title": "DEVELOPER",
        "sub":   "System info, build details\nand diagnostics",
        "color": TEXT_SECONDARY,
        "tag":   "SYS",
        "cmd":   "developer_info",
    },
    {
        "key":   "exit",
        "icon":  "⏻",
        "title": "EXIT SYSTEM",
        "sub":   "Safely quit the\napplication",
        "color": "#FF4757",
        "tag":   "EXIT",
        "cmd":   "exit_app",
    },
]


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x820+0+0")
        self.root.title("Face Recognition Attendance System")
        self.root.config(bg=BG_DARK)
        self.root.resizable(True, True)

        self._build_header()
        self._build_system_bar()
        self._build_grid()
        self._build_footer()

    # ── HEADER ───────────────────────────────────
    def _build_header(self):
        hdr = Canvas(self.root, width=1530, height=130,
                     bg=BG_DARK, highlightthickness=0)
        hdr.place(x=0, y=0)

        # Grid background
        for i in range(0, 1530, 50):
            hdr.create_line(i, 0, i, 130, fill="#0D1A2E", width=1)
        for j in range(0, 130, 25):
            hdr.create_line(0, j, 1530, j, fill="#0D1A2E", width=1)

        # Accent side bars
        hdr.create_rectangle(0,    0, 6,    130, fill=ACCENT_CYAN,  outline="")
        hdr.create_rectangle(1524, 0, 1530, 130, fill=ACCENT_TEAL,  outline="")

        # Bottom glow line
        hdr.create_rectangle(0, 127, 1530, 130, fill=ACCENT_CYAN, outline="")

        # Corner brackets — top-left
        pts_tl = [
            [(8,8),(8,35)],   [(8,8),(35,8)],
            [(8,122),(8,95)], [(8,122),(35,122)],
        ]
        # Corner brackets — top-right
        pts_tr = [
            [(1522,8),(1522,35)],   [(1522,8),(1495,8)],
            [(1522,122),(1522,95)], [(1522,122),(1495,122)],
        ]
        for grp in [pts_tl, pts_tr]:
            for p in grp:
                hdr.create_line(*p[0], *p[1], fill=ACCENT_TEAL, width=2)

        # Dot matrix left decoration
        for row in range(3):
            for col in range(8):
                hdr.create_oval(
                    45 + col*14, 14 + row*14,
                    49 + col*14, 18 + row*14,
                    fill=BORDER_GLOW, outline="")

        # Dot matrix right decoration
        for row in range(3):
            for col in range(8):
                hdr.create_oval(
                    1375 + col*14, 14 + row*14,
                    1379 + col*14, 18 + row*14,
                    fill=BORDER_GLOW, outline="")

        # Main title
        hdr.create_text(765, 45,
            text="◈  FACE RECOGNITION ATTENDANCE SYSTEM  ◈",
            font=("Courier New", 26, "bold"),
            fill=ACCENT_CYAN, anchor="center")

        hdr.create_text(765, 78,
            text="[ BIOMETRIC STUDENT ATTENDANCE — AI POWERED MODULE ]",
            font=("Courier New", 11),
            fill=TEXT_SECONDARY, anchor="center")

        hdr.create_text(765, 100,
            text="─" * 100,
            font=("Courier New", 8),
            fill=TEXT_DIM, anchor="center")

        # Version tag
        hdr.create_rectangle(1380, 90, 1520, 108, fill=INPUT_BG, outline=BORDER_GLOW)
        hdr.create_text(1450, 99,
            text="v2.0  |  PSIT  |  2026",
            font=("Consolas", 8), fill=TEXT_DIM, anchor="center")

    # ── SYSTEM STATUS BAR ────────────────────────
    def _build_system_bar(self):
        bar = Frame(self.root, bg=BG_SURFACE, height=36)
        bar.place(x=0, y=130, width=1530, height=36)

        # Left — module status pills
        pills = [
            ("◉ STUDENT DB",  ACCENT_CYAN),
            ("◉ CLASSIFIER",  ACCENT_TEAL),
            ("◉ CAMERA",      ACCENT_PURPLE),
            ("◉ CSV LOGGER",  "#FFA500"),
        ]
        for i, (text, color) in enumerate(pills):
            pill = Frame(bar, bg=INPUT_BG, bd=1, relief="solid")
            pill.place(x=10 + i*160, y=6, width=150, height=24)
            Label(pill, text=text, font=("Consolas", 8, "bold"),
                  fg=color, bg=INPUT_BG).place(x=8, y=4)

        # Right — live clock
        self.clock_var = StringVar()
        Label(bar, textvariable=self.clock_var,
              font=("Consolas", 9), fg=TEXT_SECONDARY,
              bg=BG_SURFACE, anchor="e", padx=14).place(
              x=1200, y=8, width=320, height=20)
        self._tick_clock()

    def _tick_clock(self):
        self.clock_var.set(datetime.now().strftime("%A, %d %b %Y   |   %H:%M:%S"))
        self.root.after(1000, self._tick_clock)

    # ── MODULE GRID ──────────────────────────────
    def _build_grid(self):
        grid_frame = Frame(self.root, bg=BG_DARK)
        grid_frame.place(x=0, y=174, width=1530, height=608)

        # 4 columns × 2 rows
        cols, rows = 4, 2
        card_w = 340
        card_h = 280
        pad_x  = (1530 - cols * card_w) // (cols + 1)
        pad_y  = (608  - rows * card_h) // (rows + 1)

        for idx, mod in enumerate(MODULES):
            row = idx // cols
            col = idx % cols
            x = pad_x + col * (card_w + pad_x)
            y = pad_y + row * (card_h + pad_y)
            self._make_card(grid_frame, mod, x, y, card_w, card_h)

    def _make_card(self, parent, mod, x, y, w, h):
        color = mod["color"]
        cmd   = getattr(self, mod["cmd"])

        # Outer card frame
        card = Frame(parent, bg=BG_CARD, bd=0, cursor="hand2")
        card.place(x=x, y=y, width=w, height=h)

        # Top accent bar
        accent_bar = Frame(card, bg=color, height=3)
        accent_bar.pack(fill=X, side=TOP)

        # Inner body
        body = Frame(card, bg=BG_CARD)
        body.pack(fill=BOTH, expand=True, padx=1, pady=1)

        # Border canvas (simulate glow border)
        border = Canvas(card, bg=BG_CARD, highlightthickness=1,
                        highlightbackground=BORDER_GLOW, width=w-2, height=h-4)
        border.place(x=1, y=3)

        # Tag pill (top-right)
        tag_lbl = Label(border, text=mod["tag"],
                        font=("Consolas", 8, "bold"),
                        fg=color, bg=INPUT_BG,
                        padx=6, pady=2, relief="flat")
        tag_lbl.place(x=w-70, y=10)

        # Icon
        icon_lbl = Label(border, text=mod["icon"],
                         font=("Segoe UI Emoji", 36),
                         fg=color, bg=BG_CARD)
        icon_lbl.place(x=20, y=16)

        # Title
        title_lbl = Label(border, text=mod["title"],
                          font=("Courier New", 13, "bold"),
                          fg=TEXT_PRIMARY, bg=BG_CARD, anchor="w")
        title_lbl.place(x=20, y=82)

        # Separator line
        sep = Canvas(border, bg=BG_CARD, highlightthickness=0, height=2)
        sep.place(x=20, y=108, width=w-50)
        sep.create_line(0, 1, w-50, 1, fill=BORDER_GLOW, width=1)

        # Subtitle
        sub_lbl = Label(border, text=mod["sub"],
                        font=("Consolas", 9),
                        fg=TEXT_SECONDARY, bg=BG_CARD,
                        justify=LEFT, anchor="nw")
        sub_lbl.place(x=20, y=118)

        # Arrow indicator
        arrow_lbl = Label(border, text="▸  OPEN MODULE",
                          font=("Consolas", 8, "bold"),
                          fg=color, bg=BG_CARD)
        arrow_lbl.place(x=20, y=175)

        # Launch button
        launch_btn = Button(border, text="LAUNCH  →",
                            command=cmd,
                            font=("Courier New", 10, "bold"),
                            bg=color, fg=BG_DARK,
                            relief="flat", bd=0,
                            cursor="hand2", padx=10)
        launch_btn.place(x=20, y=210, width=w-50, height=36)

        # Hover effects — entire card lights up
        def on_enter(e, b=border, c=color, lb=launch_btn):
            b.config(highlightbackground=c)
            lb.config(bg=TEXT_PRIMARY)

        def on_leave(e, b=border, c=color, lb=launch_btn):
            b.config(highlightbackground=BORDER_GLOW)
            lb.config(bg=c)

        for widget in [card, border, icon_lbl, title_lbl,
                       sub_lbl, arrow_lbl, sep, tag_lbl]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", lambda e, c=cmd: c())

        launch_btn.bind("<Enter>", on_enter)
        launch_btn.bind("<Leave>", on_leave)

    # ── FOOTER ───────────────────────────────────
    def _build_footer(self):
        footer = Frame(self.root, bg=BG_SURFACE, height=22)
        footer.place(x=0, y=798, width=1530, height=22)

        # Left dot
        Label(footer, text="◉  SYSTEM ONLINE",
              font=("Consolas", 9), fg=ACCENT_TEAL,
              bg=BG_SURFACE, padx=12).pack(side=LEFT)

        # Separator dots
        Label(footer,
              text="▪  Student Module  ▪  Face Recognition  ▪  Attendance  ▪  Training  ▪",
              font=("Consolas", 8), fg=TEXT_DIM,
              bg=BG_SURFACE).pack(side=LEFT, padx=20)

        # Right — author
        Label(footer,
              text="Pranveer Singh Institute of Technology  |  Kanpur, UP  ▪ ",
              font=("Consolas", 9), fg=TEXT_DIM,
              bg=BG_SURFACE, padx=10).pack(side=RIGHT)

    # ── MODULE LAUNCHERS ─────────────────────────
    def _open_module(self, cls):
        win = Toplevel(self.root)
        win.focus_force()
        cls(win)

    def student_details(self):
        self._open_module(Student)

    def train_data(self):
        self._open_module(Train)

    def face_data(self):
        self._open_module(Face_Recognitions)

    def attendance_data(self):
        self._open_module(Attendance)

    def open_ing(self):
        try:
            os.startfile("data")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error",
                f"Could not open data folder:\n{e}", parent=self.root)

    def help_desk(self):
        from tkinter import messagebox
        messagebox.showinfo("Help Desk",
            "◈  FACE RECOGNITION ATTENDANCE SYSTEM\n\n"
            "▸  Student Details  — Add/Edit/Delete student records & capture photos\n"
            "▸  Face Detector   — Start live face recognition & auto-mark attendance\n"
            "▸  Train Model     — Train LBPH classifier from captured photo samples\n"
            "▸  Attendance      — View, filter & export attendance reports\n"
            "▸  Photo Samples   — Browse captured face images in the data/ folder\n\n"
            "WORKFLOW:\n"
            "  1. Add Student  →  2. Take Photo (100 samples)\n"
            "  3. Train Model  →  4. Start Face Detector\n\n"
            "For issues, check Classifier.xml exists before running Face Detector.",
            parent=self.root)

    def developer_info(self):
        from tkinter import messagebox
        import sys, cv2
        messagebox.showinfo("Developer Info",
            f"◈  SYSTEM INFORMATION\n\n"
            f"▸  Python      : {sys.version.split()[0]}\n"
            f"▸  OpenCV      : {cv2.__version__}\n"
            f"▸  Tkinter     : {TkVersion}\n"
            f"▸  Platform    : {sys.platform}\n\n"
            f"◈  PROJECT INFO\n\n"
            f"▸  Module      : Face Recognition Attendance\n"
            f"▸  Institute   : Pranveer Singh Institute of Technology\n"
            f"▸  Location    : Kanpur, Uttar Pradesh\n"
            f"▸  Build       : v2.0  |  2026",
            parent=self.root)

    def exit_app(self):
        from tkinter import messagebox
        if messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=self.root):
            self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()