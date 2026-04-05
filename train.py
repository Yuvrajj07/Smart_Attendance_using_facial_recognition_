from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os
import numpy as np
import threading
import time
from datetime import datetime

# ─────────────────────────────────────────────
#  COLOUR PALETTE  (matches student.py theme)
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
BTN_GREEN      = "#00F5C4"
BTN_RED        = "#FF4757"
BTN_BLUE       = "#00D4FF"
BTN_PURPLE     = "#7C3AED"

FONT_TITLE   = ("Courier New", 28, "bold")
FONT_SECTION = ("Courier New", 11, "bold")
FONT_LABEL   = ("Consolas", 10, "bold")
FONT_INPUT   = ("Consolas", 10)
FONT_BTN     = ("Courier New", 12, "bold")
FONT_MONO    = ("Courier New", 10)
FONT_SMALL   = ("Consolas", 9)


def neon_button(parent, text, cmd, color=BTN_BLUE, width=18):
    btn = Button(parent, text=text, command=cmd,
                 font=FONT_BTN, bg=color, fg=BG_DARK,
                 activebackground=TEXT_PRIMARY, activeforeground=BG_DARK,
                 relief="flat", bd=0, cursor="hand2",
                 width=width, pady=8)
    def on_enter(e): btn.config(bg=TEXT_PRIMARY)
    def on_leave(e): btn.config(bg=color)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def apply_styles():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Cyan.Horizontal.TProgressbar",
        troughcolor=INPUT_BG, background=ACCENT_CYAN,
        bordercolor=BORDER_GLOW, lightcolor=ACCENT_CYAN,
        darkcolor=ACCENT_CYAN, thickness=18)
    style.configure("Tech.Treeview",
        background=BG_CARD, foreground=TEXT_PRIMARY,
        fieldbackground=BG_CARD, rowheight=22,
        font=FONT_SMALL, bordercolor=BORDER_GLOW)
    style.configure("Tech.Treeview.Heading",
        background=BG_SURFACE, foreground=ACCENT_CYAN,
        font=("Courier New", 9, "bold"), relief="flat")
    style.map("Tech.Treeview",
        background=[("selected", BORDER_GLOW)],
        foreground=[("selected", ACCENT_CYAN)])
    style.configure("Tech.Vertical.TScrollbar",
        background=BG_SURFACE, troughcolor=BG_DARK,
        arrowcolor=ACCENT_CYAN, bordercolor=BG_DARK)


class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x820+0+0")
        self.root.title("Face Recognition — Train Dataset")
        self.root.config(bg=BG_DARK)
        self.root.resizable(True, True)

        apply_styles()

        # State vars
        self.is_training     = False
        self.status_var      = StringVar(value="◉  System Ready — Awaiting training command")
        self.progress_var    = IntVar(value=0)
        self.total_var       = StringVar(value="—")
        self.trained_var     = StringVar(value="—")
        self.eta_var         = StringVar(value="—")
        self.accuracy_var    = StringVar(value="—")
        self.data_dir        = "data"

        self._build_header()
        self._build_main()
        self._scan_data_dir()

    # ── HEADER ───────────────────────────────────
    def _build_header(self):
        hdr = Canvas(self.root, width=1530, height=110,
                     bg=BG_DARK, highlightthickness=0)
        hdr.place(x=0, y=0)

        for i in range(0, 1530, 50):
            hdr.create_line(i, 0, i, 110, fill="#0D1A2E", width=1)
        for j in range(0, 110, 25):
            hdr.create_line(0, j, 1530, j, fill="#0D1A2E", width=1)

        hdr.create_rectangle(0,    0, 5,    110, fill=ACCENT_CYAN,   outline="")
        hdr.create_rectangle(1525, 0, 1530, 110, fill=ACCENT_TEAL,   outline="")
        hdr.create_rectangle(0,  107, 1530, 110, fill=ACCENT_CYAN,   outline="")

        # Corner brackets
        for x0, x1 in [(8, 30), (1500, 1522)]:
            for pts in [
                [(x0,10),(x0,30)], [(x0,10),(x0+22,10)],
                [(x1,10),(x1,30)], [(x1-22,10),(x1,10)],
                [(x0,100),(x0,80)], [(x0,100),(x0+22,100)],
                [(x1,100),(x1,80)], [(x1-22,100),(x1,100)],
            ]:
                hdr.create_line(*pts[0], *pts[1], fill=ACCENT_TEAL, width=2)

        hdr.create_text(765, 38,
            text="◈  FACE RECOGNITION — MODEL TRAINING MODULE  ◈",
            font=("Courier New", 22, "bold"), fill=ACCENT_CYAN, anchor="center")
        hdr.create_text(765, 66,
            text="[ LBPH FACE RECOGNIZER — DATASET TRAINER ]",
            font=("Courier New", 11), fill=TEXT_SECONDARY, anchor="center")
        hdr.create_text(765, 87,
            text="─" * 90,
            font=("Courier New", 8), fill=TEXT_DIM, anchor="center")

        # Status bar
        sb = Frame(self.root, bg=BG_SURFACE, height=22)
        sb.place(x=0, y=798, width=1530, height=22)
        Label(sb, textvariable=self.status_var,
              font=("Consolas", 9), fg=ACCENT_TEAL,
              bg=BG_SURFACE, anchor="w", padx=12).pack(side=LEFT)
        self.clock_var = StringVar()
        Label(sb, textvariable=self.clock_var,
              font=("Consolas", 9), fg=TEXT_SECONDARY,
              bg=BG_SURFACE, anchor="e", padx=12).pack(side=RIGHT)
        self._tick_clock()

    def _tick_clock(self):
        self.clock_var.set(datetime.now().strftime("  %A, %d %b %Y   |   %H:%M:%S  "))
        self.root.after(1000, self._tick_clock)

    # ── MAIN LAYOUT ──────────────────────────────
    def _build_main(self):
        main = Frame(self.root, bg=BG_DARK)
        main.place(x=10, y=118, width=1510, height=672)

        # LEFT: Controls + progress + log
        left = LabelFrame(main,
            text="  ◈  TRAINING CONTROLS  ",
            font=FONT_SECTION, fg=ACCENT_CYAN,
            bg=BG_SURFACE, bd=1, relief="solid", labelanchor="nw")
        left.place(x=0, y=0, width=560, height=665)
        self._build_controls(left)

        # CENTRE: Live preview canvas
        mid = LabelFrame(main,
            text="  ◈  LIVE SAMPLE PREVIEW  ",
            font=FONT_SECTION, fg=ACCENT_CYAN,
            bg=BG_SURFACE, bd=1, relief="solid", labelanchor="nw")
        mid.place(x=568, y=0, width=480, height=665)
        self._build_preview(mid)

        # RIGHT: Dataset inspector
        right = LabelFrame(main,
            text="  ◈  DATASET INSPECTOR  ",
            font=FONT_SECTION, fg=ACCENT_CYAN,
            bg=BG_SURFACE, bd=1, relief="solid", labelanchor="nw")
        right.place(x=1056, y=0, width=454, height=665)
        self._build_inspector(right)

    # ── CONTROLS PANEL ───────────────────────────
    def _build_controls(self, parent):
        # Stat cards row
        cards_frame = Frame(parent, bg=BG_SURFACE)
        cards_frame.place(x=8, y=10, width=540, height=80)

        self.card_defs = [
            ("TOTAL IMAGES", self.total_var,   ACCENT_CYAN,   0),
            ("STUDENTS",     self.trained_var, ACCENT_TEAL,   135),
            ("ETA",          self.eta_var,     ACCENT_PURPLE, 270),
            ("ACCURACY",     self.accuracy_var,BTN_GREEN,     405),
        ]
        for label, var, color, xpos in self.card_defs:
            c = Frame(cards_frame, bg=INPUT_BG, bd=1, relief="solid")
            c.place(x=xpos, y=0, width=132, height=78)
            Label(c, text=label, font=("Consolas", 7, "bold"),
                  fg=TEXT_DIM, bg=INPUT_BG).place(x=8, y=8)
            Label(c, textvariable=var, font=("Courier New", 18, "bold"),
                  fg=color, bg=INPUT_BG).place(x=8, y=26)

        # Data directory selector
        dir_frame = Frame(parent, bg=BG_CARD, bd=1, relief="solid")
        dir_frame.place(x=8, y=100, width=540, height=55)
        Label(dir_frame, text="▸  DATA DIRECTORY",
              font=("Consolas", 8, "bold"), fg=TEXT_DIM, bg=BG_CARD).place(x=10, y=6)
        self.dir_var = StringVar(value=os.path.abspath(self.data_dir))
        dir_entry = Entry(dir_frame, textvariable=self.dir_var,
                          font=FONT_SMALL, bg=INPUT_BG, fg=ACCENT_CYAN,
                          relief="flat", bd=0, insertbackground=ACCENT_CYAN)
        dir_entry.place(x=10, y=26, width=420, height=22)
        btn_browse = Button(dir_frame, text="BROWSE",
                            font=("Consolas", 8, "bold"),
                            bg=ACCENT_PURPLE, fg="white",
                            relief="flat", bd=0, cursor="hand2",
                            command=self._browse_dir)
        btn_browse.place(x=440, y=24, width=90, height=24)

        # Progress section
        prog_frame = LabelFrame(parent,
            text="  ◦  TRAINING PROGRESS  ",
            font=("Consolas", 8, "bold"), fg=ACCENT_TEAL,
            bg=BG_CARD, bd=1, relief="solid", labelanchor="nw")
        prog_frame.place(x=8, y=165, width=540, height=130)

        # Overall progress
        Label(prog_frame, text="OVERALL",
              font=("Consolas", 8, "bold"), fg=TEXT_DIM, bg=BG_CARD).place(x=10, y=8)
        self.overall_bar = ttk.Progressbar(prog_frame, variable=self.progress_var,
                                           maximum=100, mode="determinate",
                                           style="Cyan.Horizontal.TProgressbar")
        self.overall_bar.place(x=10, y=24, width=450, height=18)
        self.pct_lbl = Label(prog_frame, text="0%",
                             font=("Courier New", 10, "bold"),
                             fg=ACCENT_CYAN, bg=BG_CARD)
        self.pct_lbl.place(x=468, y=22)

        # Current file label
        Label(prog_frame, text="CURRENT FILE",
              font=("Consolas", 8, "bold"), fg=TEXT_DIM, bg=BG_CARD).place(x=10, y=52)
        self.current_file_var = StringVar(value="—")
        Label(prog_frame, textvariable=self.current_file_var,
              font=FONT_SMALL, fg=TEXT_SECONDARY, bg=BG_CARD,
              anchor="w").place(x=10, y=68, width=520, height=16)

        # Elapsed time
        Label(prog_frame, text="ELAPSED",
              font=("Consolas", 8, "bold"), fg=TEXT_DIM, bg=BG_CARD).place(x=10, y=92)
        self.elapsed_var = StringVar(value="00:00")
        Label(prog_frame, textvariable=self.elapsed_var,
              font=("Courier New", 10, "bold"), fg=ACCENT_PURPLE, bg=BG_CARD).place(x=80, y=90)

        # Main TRAIN button
        self.train_btn = neon_button(parent, "⚡  TRAIN MODEL",
                                     self._start_training_thread,
                                     color=ACCENT_CYAN, width=30)
        self.train_btn.place(x=8, y=308, width=540, height=52)

        # Secondary buttons
        sec_frame = Frame(parent, bg=BG_DARK)
        sec_frame.place(x=8, y=368, width=540, height=44)

        scan_btn = neon_button(sec_frame, "🔍  SCAN DATA DIR",
                               self._scan_data_dir, color=ACCENT_TEAL, width=18)
        scan_btn.pack(side=LEFT, expand=True, fill=X, padx=(0, 5))

        verify_btn = neon_button(sec_frame, "✔  VERIFY MODEL",
                                 self._verify_model, color=ACCENT_PURPLE, width=18)
        verify_btn.pack(side=LEFT, expand=True, fill=X)

        # Training log
        log_frame = LabelFrame(parent,
            text="  ◦  TRAINING LOG  ",
            font=("Consolas", 8, "bold"), fg=ACCENT_TEAL,
            bg=BG_CARD, bd=1, relief="solid", labelanchor="nw")
        log_frame.place(x=8, y=422, width=540, height=230)

        log_scroll = ttk.Scrollbar(log_frame, orient=VERTICAL,
                                   style="Tech.Vertical.TScrollbar")
        log_scroll.pack(side=RIGHT, fill=Y)

        self.log_text = Text(log_frame, bg=INPUT_BG, fg=ACCENT_TEAL,
                             font=("Consolas", 8), relief="flat",
                             bd=0, insertbackground=ACCENT_CYAN,
                             yscrollcommand=log_scroll.set,
                             state=DISABLED, wrap=WORD)
        self.log_text.pack(fill=BOTH, expand=1, padx=4, pady=4)
        log_scroll.config(command=self.log_text.yview)

        # Text tags
        self.log_text.tag_config("info",    foreground=ACCENT_TEAL)
        self.log_text.tag_config("success", foreground=BTN_GREEN)
        self.log_text.tag_config("warn",    foreground="#FFA500")
        self.log_text.tag_config("error",   foreground=BTN_RED)
        self.log_text.tag_config("dim",     foreground=TEXT_DIM)

        self._log("System initialised.", "info")
        self._log("Waiting for training command...", "dim")

    # ── LIVE PREVIEW PANEL ───────────────────────
    def _build_preview(self, parent):
        # Canvas for showing face samples during training
        self.preview_canvas = Canvas(parent, width=456, height=400,
                                     bg="#050810", highlightthickness=1,
                                     highlightbackground=BORDER_GLOW)
        self.preview_canvas.place(x=8, y=10)
        self._draw_idle_canvas()

        # Sample info below canvas
        info = Frame(parent, bg=BG_CARD, bd=1, relief="solid")
        info.place(x=8, y=420, width=456, height=60)

        Label(info, text="SAMPLE ID", font=("Consolas", 8, "bold"),
              fg=TEXT_DIM, bg=BG_CARD).place(x=10, y=8)
        self.sample_id_var = StringVar(value="—")
        Label(info, textvariable=self.sample_id_var,
              font=("Courier New", 16, "bold"), fg=ACCENT_CYAN,
              bg=BG_CARD).place(x=10, y=24)

        Label(info, text="FILENAME", font=("Consolas", 8, "bold"),
              fg=TEXT_DIM, bg=BG_CARD).place(x=160, y=8)
        self.sample_file_var = StringVar(value="—")
        Label(info, textvariable=self.sample_file_var,
              font=FONT_SMALL, fg=TEXT_SECONDARY, bg=BG_CARD).place(x=160, y=24)

        # Student breakdown mini chart
        chart_frame = LabelFrame(parent,
            text="  ◦  SAMPLES PER STUDENT  ",
            font=("Consolas", 8, "bold"), fg=ACCENT_TEAL,
            bg=BG_CARD, bd=1, relief="solid", labelanchor="nw")
        chart_frame.place(x=8, y=490, width=456, height=165)

        self.chart_canvas = Canvas(chart_frame, bg=BG_CARD,
                                   highlightthickness=0, height=140)
        self.chart_canvas.pack(fill=X, padx=6, pady=4)

    def _draw_idle_canvas(self):
        self.preview_canvas.delete("all")
        # Grid lines
        for i in range(0, 460, 30):
            self.preview_canvas.create_line(i, 0, i, 400, fill="#0D1A2E", width=1)
        for j in range(0, 400, 30):
            self.preview_canvas.create_line(0, j, 460, j, fill="#0D1A2E", width=1)
        # Centre icon
        self.preview_canvas.create_text(228, 160, text="◈",
            font=("Courier New", 72), fill=TEXT_DIM, anchor="center")
        self.preview_canvas.create_text(228, 250,
            text="SAMPLE PREVIEW",
            font=("Courier New", 14, "bold"), fill=TEXT_DIM, anchor="center")
        self.preview_canvas.create_text(228, 278,
            text="Faces will appear here during training",
            font=("Courier New", 9), fill="#2A3A52", anchor="center")

    # ── DATASET INSPECTOR ────────────────────────
    def _build_inspector(self, parent):
        # Summary
        summary = Frame(parent, bg=BG_SURFACE)
        summary.place(x=8, y=10, width=434, height=55)

        self.img_count_var = StringVar(value="0 images")
        self.std_count_var = StringVar(value="0 students")

        Label(summary, textvariable=self.img_count_var,
              font=("Courier New", 14, "bold"), fg=ACCENT_CYAN,
              bg=BG_SURFACE).place(x=10, y=8)
        Label(summary, textvariable=self.std_count_var,
              font=("Courier New", 14, "bold"), fg=ACCENT_TEAL,
              bg=BG_SURFACE).place(x=220, y=8)

        Label(summary, text="ready to train",
              font=FONT_SMALL, fg=TEXT_DIM, bg=BG_SURFACE).place(x=10, y=30)

        # File list table
        tbl = Frame(parent, bg=BG_CARD, bd=1, relief="solid")
        tbl.place(x=8, y=74, width=434, height=430)

        scy = ttk.Scrollbar(tbl, orient=VERTICAL, style="Tech.Vertical.TScrollbar")
        scy.pack(side=RIGHT, fill=Y)

        self.file_table = ttk.Treeview(tbl,
            columns=("file", "sid", "size"),
            show="headings",
            yscrollcommand=scy.set,
            style="Tech.Treeview")
        scy.config(command=self.file_table.yview)
        self.file_table.pack(fill=BOTH, expand=1)

        self.file_table.heading("file", text="FILENAME")
        self.file_table.heading("sid",  text="STUDENT ID")
        self.file_table.heading("size", text="RESOLUTION")
        self.file_table.column("file", width=180)
        self.file_table.column("sid",  width=90)
        self.file_table.column("size", width=90)

        self.file_table.tag_configure("odd",  background="#0F1A2E")
        self.file_table.tag_configure("even", background=BG_CARD)

        # Classifier status
        clf_frame = Frame(parent, bg=BG_CARD, bd=1, relief="solid")
        clf_frame.place(x=8, y=514, width=434, height=80)

        Label(clf_frame, text="▸  CLASSIFIER STATUS",
              font=("Consolas", 8, "bold"), fg=TEXT_DIM, bg=BG_CARD).place(x=10, y=8)

        self.clf_status_var = StringVar(value="Not trained yet")
        self.clf_status_color = StringVar()
        self.clf_lbl = Label(clf_frame, textvariable=self.clf_status_var,
                             font=("Courier New", 11, "bold"),
                             fg=BTN_RED, bg=BG_CARD)
        self.clf_lbl.place(x=10, y=26)

        self.clf_size_var = StringVar(value="")
        Label(clf_frame, textvariable=self.clf_size_var,
              font=FONT_SMALL, fg=TEXT_DIM, bg=BG_CARD).place(x=10, y=50)

        self._check_classifier_status()

        # Refresh button
        ref_btn = neon_button(parent, "↺  REFRESH INSPECTOR",
                              self._scan_data_dir, color=BORDER_GLOW, width=24)
        ref_btn.place(x=8, y=604, width=434, height=40)

    # ── HELPER FUNCTIONS ─────────────────────────
    def _log(self, msg, tag="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state=NORMAL)
        self.log_text.insert(END, f"[{ts}]  {msg}\n", tag)
        self.log_text.see(END)
        self.log_text.config(state=DISABLED)

    def _set_status(self, msg):
        self.status_var.set(f"◉  {msg}")

    def _browse_dir(self):
        from tkinter import filedialog
        d = filedialog.askdirectory(title="Select Data Directory", parent=self.root)
        if d:
            self.data_dir = d
            self.dir_var.set(d)
            self._scan_data_dir()

    def _check_classifier_status(self):
        clf_path = "Classifier.xml"
        if os.path.exists(clf_path):
            size_kb = os.path.getsize(clf_path) / 1024
            mtime = datetime.fromtimestamp(os.path.getmtime(clf_path))
            self.clf_status_var.set("✓  Classifier.xml found")
            self.clf_lbl.config(fg=BTN_GREEN)
            self.clf_size_var.set(f"{size_kb:.1f} KB  —  Last trained: {mtime.strftime('%d %b %Y  %H:%M')}")
        else:
            self.clf_status_var.set("✗  Classifier.xml not found")
            self.clf_lbl.config(fg=BTN_RED)
            self.clf_size_var.set("Run training to generate the classifier.")

    def _verify_model(self):
        if not os.path.exists("Classifier.xml"):
            messagebox.showerror("Not Found",
                "Classifier.xml not found.\nPlease train the model first.", parent=self.root)
            return
        try:
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("Classifier.xml")
            self._log("✓  Classifier.xml loaded and verified successfully.", "success")
            self._set_status("Model verified — Classifier.xml is valid.")
            messagebox.showinfo("Verified",
                "Classifier.xml is valid and ready for face recognition!",
                parent=self.root)
        except Exception as e:
            self._log(f"✗  Verification failed: {e}", "error")
            messagebox.showerror("Error", f"Classifier verification failed:\n{e}", parent=self.root)

    def _scan_data_dir(self):
        """Scan data directory and populate the inspector table."""
        self.file_table.delete(*self.file_table.get_children())
        self._draw_bar_chart({})

        data_dir = self.dir_var.get() if hasattr(self, 'dir_var') else self.data_dir

        if not os.path.exists(data_dir):
            self.img_count_var.set("0 images")
            self.std_count_var.set("0 students")
            self.total_var.set("0")
            self.trained_var.set("0")
            self._log(f"✗  Data directory not found: {data_dir}", "error")
            return

        files = [f for f in os.listdir(data_dir)
                 if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

        student_counts = {}
        valid_files = []

        for i, fname in enumerate(sorted(files)):
            fpath = os.path.join(data_dir, fname)
            try:
                parts = fname.split('.')
                sid = parts[1] if len(parts) >= 3 else "?"
                img = Image.open(fpath)
                w, h = img.size
                res = f"{w}×{h}"
                tag = "odd" if i % 2 else "even"
                self.file_table.insert("", END,
                    values=(fname, sid, res), tags=(tag,))
                student_counts[sid] = student_counts.get(sid, 0) + 1
                valid_files.append(fpath)
            except Exception:
                pass

        n_imgs = len(valid_files)
        n_students = len(student_counts)
        self.img_count_var.set(f"{n_imgs} images")
        self.std_count_var.set(f"{n_students} students")
        self.total_var.set(str(n_imgs))
        self.trained_var.set(str(n_students))

        self._draw_bar_chart(student_counts)
        self._check_classifier_status()
        self._log(f"Scanned: {n_imgs} images across {n_students} student(s).", "info")
        self._set_status(f"Dataset scanned — {n_imgs} images, {n_students} students.")

    def _draw_bar_chart(self, student_counts):
        """Draw a simple bar chart of samples per student."""
        c = self.chart_canvas
        c.delete("all")
        if not student_counts:
            c.create_text(220, 60, text="No data",
                font=("Consolas", 9), fill=TEXT_DIM, anchor="center")
            return

        max_val = max(student_counts.values(), default=1)
        bar_w = max(12, min(40, 400 // max(len(student_counts), 1) - 4))
        colors = [ACCENT_CYAN, ACCENT_TEAL, ACCENT_PURPLE,
                  "#FF6B6B", "#FFA500", "#00D4FF", "#7C3AED"]
        chart_h = 110

        for i, (sid, count) in enumerate(sorted(student_counts.items())):
            x = 10 + i * (bar_w + 6)
            bar_h = int((count / max_val) * chart_h)
            y_top = chart_h - bar_h + 10
            color = colors[i % len(colors)]

            c.create_rectangle(x, y_top, x + bar_w, chart_h + 10,
                                fill=color, outline="", width=0)
            c.create_text(x + bar_w // 2, y_top - 4,
                text=str(count), font=("Consolas", 7), fill=color, anchor="s")
            c.create_text(x + bar_w // 2, chart_h + 18,
                text=f"#{sid}", font=("Consolas", 7), fill=TEXT_DIM, anchor="n")

    # ── TRAINING ─────────────────────────────────
    def _start_training_thread(self):
        if self.is_training:
            return
        t = threading.Thread(target=self.train_classifier, daemon=True)
        t.start()

    def train_classifier(self):
        self.is_training = True
        self.root.after(0, lambda: self.train_btn.config(
            state=DISABLED, bg="#1A3A2A", text="⏳  TRAINING IN PROGRESS..."))
        self._log("═" * 42, "dim")
        self._log("Training initiated.", "info")

        data_dir = self.dir_var.get() if hasattr(self, 'dir_var') else self.data_dir

        # Validate data dir
        if not os.path.exists(data_dir):
            self.root.after(0, lambda: messagebox.showerror(
                "Error", f"Data directory not found:\n{data_dir}", parent=self.root))
            self._log(f"✗  Directory not found: {data_dir}", "error")
            self._reset_train_btn()
            return

        path = [os.path.join(data_dir, f)
                for f in os.listdir(data_dir)
                if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

        if not path:
            self.root.after(0, lambda: messagebox.showerror(
                "Error", "No image files found in data directory!", parent=self.root))
            self._log("✗  No images found.", "error")
            self._reset_train_btn()
            return

        total = len(path)
        self._log(f"Found {total} image(s) to process.", "info")
        self.root.after(0, lambda: self.eta_var.set(f"~{total//10 + 1}s"))

        faces, ids = [], []
        start_time = time.time()

        for idx, image_path in enumerate(path):
            try:
                fname = os.path.basename(image_path)
                parts = fname.split('.')
                sid = int(parts[1]) if len(parts) >= 3 else 0

                img = Image.open(image_path).convert('L')
                img_np = np.array(img, 'uint8')

                faces.append(img_np)
                ids.append(sid)

                # Update progress
                pct = int(((idx + 1) / total) * 100)
                elapsed = time.time() - start_time
                elapsed_str = f"{int(elapsed//60):02d}:{int(elapsed%60):02d}"

                self.root.after(0, lambda p=pct, f=fname, e=elapsed_str, s=sid: (
                    self.progress_var.set(p),
                    self.pct_lbl.config(text=f"{p}%"),
                    self.current_file_var.set(f),
                    self.elapsed_var.set(e),
                    self.sample_id_var.set(str(s)),
                    self.sample_file_var.set(f),
                    self._set_status(f"Processing {idx+1}/{total} — {f}")
                ))

                # Show preview (every 5th frame to avoid lag)
                if idx % 5 == 0:
                    self.root.after(0, lambda im=img_np: self._show_preview(im))

                # Log every 50 images
                if (idx + 1) % 50 == 0:
                    self._log(f"Processed {idx+1}/{total} images...", "dim")

            except Exception as e:
                self._log(f"⚠  Skipped {os.path.basename(image_path)}: {e}", "warn")
                continue

        if not faces:
            self._log("✗  No valid faces extracted.", "error")
            self._reset_train_btn()
            return

        self._log(f"Extracted {len(faces)} face samples. Starting LBPH training...", "info")
        self._set_status("Training LBPH classifier...")

        try:
            ids_np = np.array(ids)
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids_np)
            clf.write("Classifier.xml")

            elapsed_total = time.time() - start_time
            elapsed_str = f"{int(elapsed_total//60):02d}:{int(elapsed_total%60):02d}"

            self._log("═" * 42, "dim")
            self._log(f"✓  Training complete!", "success")
            self._log(f"✓  {len(faces)} samples, {len(set(ids))} student(s)", "success")
            self._log(f"✓  Classifier saved: Classifier.xml", "success")
            self._log(f"✓  Total time: {elapsed_str}", "success")

            self.root.after(0, lambda: (
                self.progress_var.set(100),
                self.pct_lbl.config(text="100%"),
                self.accuracy_var.set("✓"),
                self.elapsed_var.set(elapsed_str),
                self._set_status(f"Training complete — {len(faces)} samples, {len(set(ids))} student(s). Saved to Classifier.xml"),
                self._check_classifier_status(),
                messagebox.showinfo("Training Complete",
                    f"✓  Model trained successfully!\n\n"
                    f"▸  Samples processed : {len(faces)}\n"
                    f"▸  Students trained  : {len(set(ids))}\n"
                    f"▸  Time taken        : {elapsed_str}\n"
                    f"▸  Saved to          : Classifier.xml",
                    parent=self.root)
            ))

        except Exception as e:
            self._log(f"✗  Training failed: {e}", "error")
            self.root.after(0, lambda: messagebox.showerror(
                "Training Failed", f"Error during training:\n{e}", parent=self.root))

        self._reset_train_btn()
        self.is_training = False
        cv2.destroyAllWindows()

    def _show_preview(self, img_np):
        """Display a grayscale face sample on the preview canvas."""
        try:
            h, w = img_np.shape
            max_w, max_h = 456, 400
            scale = min(max_w / w, max_h / h)
            new_w, new_h = int(w * scale), int(h * scale)
            resized = cv2.resize(img_np, (new_w, new_h))
            pil_img = Image.fromarray(resized)
            photo = ImageTk.PhotoImage(pil_img)
            x = (max_w - new_w) // 2
            y = (max_h - new_h) // 2
            self.preview_canvas.delete("all")
            self.preview_canvas.image = photo
            self.preview_canvas.create_rectangle(0, 0, max_w, max_h,
                fill="#050810", outline="")
            self.preview_canvas.create_image(x, y, image=photo, anchor=NW)
            # HUD
            self.preview_canvas.create_rectangle(0, 0, max_w, 22,
                fill="#0A0E1A", outline="")
            self.preview_canvas.create_text(8, 11,
                text="PROCESSING SAMPLE",
                font=("Consolas", 8), fill=ACCENT_CYAN, anchor="w")
        except Exception:
            pass

    def _reset_train_btn(self):
        self.root.after(0, lambda: self.train_btn.config(
            state=NORMAL, bg=ACCENT_CYAN, text="⚡  TRAIN MODEL"))
        self.is_training = False


if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()