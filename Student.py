from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import cv2
import math
import time


# ─────────────────────────────────────────────
#  COLOUR PALETTE  (deep-space tech aesthetic)
# ─────────────────────────────────────────────
BG_DARK       = "#0A0E1A"   # near-black deep navy
BG_CARD       = "#111827"   # card background
BG_SURFACE    = "#1A2235"   # slightly lighter surface
ACCENT_CYAN   = "#00D4FF"   # electric cyan
ACCENT_TEAL   = "#00F5C4"   # mint-teal glow
ACCENT_PURPLE = "#7C3AED"   # vivid purple for highlights
TEXT_PRIMARY  = "#F0F4FF"   # bright white-blue
TEXT_SECONDARY= "#8B9DC3"   # muted steel blue
TEXT_DIM      = "#4B5E82"   # dim labels
BORDER_GLOW   = "#1E3A5F"   # subtle border
INPUT_BG      = "#0D1526"   # input field bg
BTN_SAVE      = "#00D4FF"
BTN_UPDATE    = "#7C3AED"
BTN_DELETE    = "#FF4757"
BTN_RESET     = "#00F5C4"
SUCCESS_GREEN = "#00F5C4"
ERROR_RED     = "#FF4757"

# ─────────────────────────────────────────────
#  FONTS
# ─────────────────────────────────────────────
FONT_TITLE  = ("Courier New", 26, "bold")
FONT_SECTION= ("Courier New", 11, "bold")
FONT_LABEL  = ("Consolas", 10, "bold")
FONT_INPUT  = ("Consolas", 10)
FONT_BTN    = ("Courier New", 10, "bold")
FONT_HEAD   = ("Courier New", 9, "bold")


def apply_global_style():
    """Apply ttk styles globally."""
    style = ttk.Style()
    style.theme_use("clam")

    # ── Combobox ──
    style.configure("Tech.TCombobox",
        fieldbackground=INPUT_BG,
        background=INPUT_BG,
        foreground=ACCENT_CYAN,
        selectbackground=BG_SURFACE,
        selectforeground=ACCENT_CYAN,
        bordercolor=BORDER_GLOW,
        arrowcolor=ACCENT_CYAN,
        font=FONT_INPUT)
    style.map("Tech.TCombobox",
        fieldbackground=[("readonly", INPUT_BG)],
        foreground=[("readonly", ACCENT_CYAN)])

    # ── Entry ──
    style.configure("Tech.TEntry",
        fieldbackground=INPUT_BG,
        foreground=TEXT_PRIMARY,
        bordercolor=BORDER_GLOW,
        insertcolor=ACCENT_CYAN,
        font=FONT_INPUT)

    # ── Scrollbar ──
    style.configure("Tech.Vertical.TScrollbar",
        background=BG_SURFACE, troughcolor=BG_DARK,
        arrowcolor=ACCENT_CYAN, bordercolor=BG_DARK)
    style.configure("Tech.Horizontal.TScrollbar",
        background=BG_SURFACE, troughcolor=BG_DARK,
        arrowcolor=ACCENT_CYAN, bordercolor=BG_DARK)

    # ── Treeview ──
    style.configure("Tech.Treeview",
        background=BG_CARD,
        foreground=TEXT_PRIMARY,
        fieldbackground=BG_CARD,
        rowheight=26,
        font=FONT_INPUT,
        bordercolor=BORDER_GLOW)
    style.configure("Tech.Treeview.Heading",
        background=BG_SURFACE,
        foreground=ACCENT_CYAN,
        font=FONT_HEAD,
        relief="flat",
        bordercolor=BORDER_GLOW)
    style.map("Tech.Treeview",
        background=[("selected", "#1E3A5F")],
        foreground=[("selected", ACCENT_CYAN)])
    style.map("Tech.Treeview.Heading",
        background=[("active", BORDER_GLOW)])

    # ── Radiobutton ──
    style.configure("Tech.TRadiobutton",
        background=BG_SURFACE,
        foreground=TEXT_SECONDARY,
        font=FONT_LABEL,
        indicatorcolor=ACCENT_CYAN)
    style.map("Tech.TRadiobutton",
        background=[("active", BG_SURFACE)],
        foreground=[("active", ACCENT_CYAN)])


def glow_label(parent, text, font=FONT_LABEL, fg=ACCENT_CYAN, bg=BG_SURFACE):
    return Label(parent, text=text, font=font, fg=fg, bg=bg)


def neon_button(parent, text, cmd, color=BTN_SAVE, width=16):
    """Custom neon-effect button using Canvas."""
    btn = Button(
        parent, text=text, command=cmd,
        font=FONT_BTN,
        bg=color, fg=BG_DARK,
        activebackground=TEXT_PRIMARY, activeforeground=BG_DARK,
        relief="flat", bd=0,
        cursor="hand2",
        width=width,
        pady=5
    )
    # Hover animation
    def on_enter(e): btn.config(bg=TEXT_PRIMARY)
    def on_leave(e): btn.config(bg=color)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def section_frame(parent, title, x, y, w, h):
    """Returns a styled LabelFrame with glowing title."""
    frm = LabelFrame(
        parent, text=f"  ◈  {title}  ",
        font=FONT_SECTION,
        fg=ACCENT_CYAN, bg=BG_SURFACE,
        bd=1, relief="solid",
        highlightbackground=BORDER_GLOW,
        highlightthickness=1,
        labelanchor="nw"
    )
    frm.place(x=x, y=y, width=w, height=h)
    return frm


def draw_header_canvas(parent):
    """Draw a stylised animated header using Canvas."""
    c = Canvas(parent, width=1530, height=120,
               bg=BG_DARK, highlightthickness=0)
    c.place(x=0, y=0)

    # Grid lines
    for i in range(0, 1530, 60):
        c.create_line(i, 0, i, 120, fill="#0D1A2E", width=1)
    for j in range(0, 120, 30):
        c.create_line(0, j, 1530, j, fill="#0D1A2E", width=1)

    # Gradient-ish glow bar at bottom
    for i in range(6):
        c.create_rectangle(0, 114+i//2, 1530, 120,
                            fill=ACCENT_CYAN if i < 2 else BG_DARK,
                            outline="")

    # Side accent rectangles
    c.create_rectangle(0, 0, 6, 120, fill=ACCENT_CYAN, outline="")
    c.create_rectangle(1524, 0, 1530, 120, fill=ACCENT_TEAL, outline="")

    # Title text
    c.create_text(765, 38, text="◈  FACE RECOGNITION ATTENDANCE SYSTEM  ◈",
                  font=("Courier New", 22, "bold"), fill=ACCENT_CYAN,
                  anchor="center")
    c.create_text(765, 72, text="[ Student Management Module ]",
                  font=("Courier New", 12), fill=TEXT_SECONDARY,
                  anchor="center")
    c.create_text(765, 95, text="─────────────────────────────────────────────",
                  font=("Courier New", 10), fill=TEXT_DIM, anchor="center")
    return c


class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x820+0+0")
        self.root.title("Face Recognition Attendance System")
        self.root.config(bg=BG_DARK)
        self.root.resizable(True, True)

        apply_global_style()
        self._init_vars()
        self._build_ui()

    # ── Variables ──────────────────────────────
    def _init_vars(self):
        self.var_dep      = StringVar()
        self.var_course   = StringVar()
        self.var_year     = StringVar()
        self.var_semester = StringVar()
        self.var_std_id   = StringVar()
        self.var_std_name = StringVar()
        self.var_div      = StringVar()
        self.var_roll     = StringVar()
        self.var_gender   = StringVar()
        self.var_dob      = StringVar()
        self.var_email    = StringVar()
        self.var_phone    = StringVar()
        self.var_address  = StringVar()
        self.var_teacher  = StringVar()
        self.var_radio1   = StringVar()
        self.var_search   = StringVar()
        self.var_search_by= StringVar()

    # ── Main UI ────────────────────────────────
    def _build_ui(self):
        # Header
        draw_header_canvas(self.root)

        # Status bar
        self.status_var = StringVar(value="◉  System Ready")
        status = Label(self.root, textvariable=self.status_var,
                       font=("Consolas", 9), fg=ACCENT_TEAL, bg=BG_DARK,
                       anchor="w", padx=10)
        status.place(x=0, y=795, width=1530, height=20)

        # Main container
        main = Frame(self.root, bg=BG_DARK)
        main.place(x=10, y=128, width=1510, height=665)

        # ── LEFT PANEL ──
        left = LabelFrame(main,
                          text="  ◈  STUDENT DETAILS  ",
                          font=FONT_SECTION, fg=ACCENT_CYAN,
                          bg=BG_SURFACE, bd=1, relief="solid",
                          labelanchor="nw")
        left.place(x=0, y=0, width=740, height=655)

        self._build_course_section(left)
        self._build_student_section(left)
        self._build_buttons(left)

        # ── RIGHT PANEL ──
        right = LabelFrame(main,
                           text="  ◈  STUDENT RECORDS  ",
                           font=FONT_SECTION, fg=ACCENT_CYAN,
                           bg=BG_SURFACE, bd=1, relief="solid",
                           labelanchor="nw")
        right.place(x=750, y=0, width=755, height=655)

        self._build_search_section(right)
        self._build_table(right)

    # ── Course Info Section ─────────────────────
    def _build_course_section(self, parent):
        frm = LabelFrame(parent,
                         text="  ◦  COURSE INFORMATION  ",
                         font=("Consolas", 9, "bold"),
                         fg=ACCENT_TEAL, bg=BG_CARD,
                         bd=1, relief="solid", labelanchor="nw")
        frm.place(x=8, y=8, width=722, height=115)

        fields = [
            ("Department", self.var_dep,
             ("Select Department","Computer Science","Information Technology","Civil","Mechanical"), 0, 0),
            ("Course", self.var_course,
             ("Select Course","BE/BTech","BBA","BCA","MBA","MCA"), 0, 2),
            ("Year", self.var_year,
             ("Select Year","First Year","Second Year","Third Year","Fourth Year"), 1, 0),
            ("Semester", self.var_semester,
             ("Select Semester","Semester-1","Semester-2","Semester-3","Semester-4",
              "Semester-5","Semester-6","Semester-7","Semester-8"), 1, 2),
        ]

        for label_text, var, values, row, col in fields:
            lbl = Label(frm, text=label_text, font=FONT_LABEL,
                        fg=TEXT_SECONDARY, bg=BG_CARD, anchor="w")
            lbl.grid(row=row, column=col, padx=(12, 4), pady=8, sticky=W)
            cb = ttk.Combobox(frm, textvariable=var,
                              font=FONT_INPUT, state="readonly",
                              width=20, style="Tech.TCombobox")
            cb["values"] = values
            cb.current(0)
            cb.grid(row=row, column=col+1, padx=(0, 15), pady=8, sticky=W)

    # ── Student Info Section ────────────────────
    def _build_student_section(self, parent):
        frm = LabelFrame(parent,
                         text="  ◦  CLASS & PERSONAL INFORMATION  ",
                         font=("Consolas", 9, "bold"),
                         fg=ACCENT_TEAL, bg=BG_CARD,
                         bd=1, relief="solid", labelanchor="nw")
        frm.place(x=8, y=132, width=722, height=370)

        rows = [
            ("Student ID",    self.var_std_id,   None,    0, 0),
            ("Student Name",  self.var_std_name,  None,   0, 2),
            ("Class Division",self.var_div,        None,   1, 0),
            ("Roll No",       self.var_roll,       None,   1, 2),
            ("Gender",        self.var_gender,
             ("Male","Female","Other"),                    2, 0),
            ("Date of Birth", self.var_dob,        None,   2, 2),
            ("Email",         self.var_email,      None,   3, 0),
            ("Phone",         self.var_phone,      None,   3, 2),
            ("Address",       self.var_address,    None,   4, 0),
            ("Teacher",       self.var_teacher,    None,   4, 2),
        ]

        for label_text, var, values, row, col in rows:
            dot_color = ACCENT_CYAN if col == 0 else ACCENT_TEAL
            dot = Label(frm, text="▸", font=("Consolas", 10), fg=dot_color, bg=BG_CARD)
            dot.grid(row=row, column=col, padx=(8, 0), pady=10, sticky=E)

            lbl = Label(frm, text=label_text, font=FONT_LABEL,
                        fg=TEXT_SECONDARY, bg=BG_CARD, anchor="w", width=13)
            lbl.grid(row=row, column=col+1, padx=(0, 4), pady=10, sticky=W)

            if values:
                cb = ttk.Combobox(frm, textvariable=var,
                                  font=FONT_INPUT, state="readonly",
                                  width=18, style="Tech.TCombobox")
                cb["values"] = values
                cb.current(0)
                cb.grid(row=row, column=col+2, padx=(0, 10), pady=10, sticky=W)
            else:
                ent = ttk.Entry(frm, textvariable=var,
                                font=FONT_INPUT, width=20,
                                style="Tech.TEntry")
                ent.grid(row=row, column=col+2, padx=(0, 10), pady=10, sticky=W)

        # Separator line
        sep = Frame(frm, bg=BORDER_GLOW, height=1)
        sep.grid(row=5, column=0, columnspan=6, sticky="ew", padx=8, pady=4)

        # Photo sample radio buttons
        radio_frame = Frame(frm, bg=BG_CARD)
        radio_frame.grid(row=6, column=0, columnspan=6, padx=10, pady=8, sticky=W)

        Label(radio_frame, text="Photo Sample:", font=FONT_LABEL,
              fg=TEXT_SECONDARY, bg=BG_CARD).pack(side=LEFT, padx=(0, 12))

        r1 = ttk.Radiobutton(radio_frame, variable=self.var_radio1,
                             text="◉  Capture Photo", value="Yes",
                             style="Tech.TRadiobutton")
        r1.pack(side=LEFT, padx=(0, 20))

        r2 = ttk.Radiobutton(radio_frame, variable=self.var_radio1,
                             text="◎  No Photo", value="No",
                             style="Tech.TRadiobutton")
        r2.pack(side=LEFT)

    # ── Button Row ──────────────────────────────
    def _build_buttons(self, parent):
        # Action buttons row
        btn_row1 = Frame(parent, bg=BG_DARK, bd=0)
        btn_row1.place(x=8, y=510, width=722, height=44)

        btns1 = [
            ("💾  SAVE",   self.add_data,    BTN_SAVE,   15),
            ("✏  UPDATE", self.update_data,  BTN_UPDATE, 15),
            ("🗑  DELETE", self.delete_data,  BTN_DELETE, 15),
            ("↺  RESET",  self.reset_data,   BTN_RESET,  15),
        ]
        for text, cmd, color, w in btns1:
            b = neon_button(btn_row1, text, cmd, color=color, width=w)
            b.pack(side=LEFT, padx=2, expand=True, fill=X)

        # Photo buttons row
        btn_row2 = Frame(parent, bg=BG_DARK, bd=0)
        btn_row2.place(x=8, y=560, width=722, height=44)

        b3 = neon_button(btn_row2, "📷  TAKE PHOTO SAMPLE",
                         self.take_photo, color="#0EA5E9", width=30)
        b3.pack(side=LEFT, padx=2, expand=True, fill=X)

        b4 = neon_button(btn_row2, "🔄  GENERATE / UPDATE DATASET",
                         self.generate_dataset, color=ACCENT_PURPLE, width=30)
        b4.pack(side=LEFT, padx=2, expand=True, fill=X)

    # ── Search Section ──────────────────────────
    def _build_search_section(self, parent):
        frm = LabelFrame(parent,
                         text="  ◦  SEARCH  ",
                         font=("Consolas", 9, "bold"),
                         fg=ACCENT_TEAL, bg=BG_CARD,
                         bd=1, relief="solid", labelanchor="nw")
        frm.place(x=8, y=8, width=737, height=70)

        Label(frm, text="Search By:", font=FONT_LABEL,
              fg=TEXT_SECONDARY, bg=BG_CARD).grid(row=0, column=0, padx=10, pady=12, sticky=W)

        cb = ttk.Combobox(frm, textvariable=self.var_search_by,
                          font=FONT_INPUT, state="readonly",
                          width=14, style="Tech.TCombobox")
        cb["values"] = ("Select", "Roll_No", "Phone_No")
        cb.current(0)
        cb.grid(row=0, column=1, padx=6, pady=12, sticky=W)

        ent = ttk.Entry(frm, textvariable=self.var_search,
                        font=FONT_INPUT, width=18, style="Tech.TEntry")
        ent.grid(row=0, column=2, padx=6, pady=12, sticky=W)

        sb = neon_button(frm, "🔍 Search",
                         lambda: None, color=ACCENT_CYAN, width=10)
        sb.grid(row=0, column=3, padx=6, pady=8)

        ab = neon_button(frm, "⊞  All",
                         self.fetch_data, color=ACCENT_TEAL, width=8)
        ab.grid(row=0, column=4, padx=6, pady=8)

    # ── Data Table ──────────────────────────────
    def _build_table(self, parent):
        frm = Frame(parent, bg=BG_CARD, bd=1, relief="solid")
        frm.place(x=8, y=88, width=737, height=555)

        cols = ("dep","course","year","sem","id","name",
                "div","roll","gender","dob","email","phone",
                "address","teacher","photo")

        scx = ttk.Scrollbar(frm, orient=HORIZONTAL, style="Tech.Horizontal.TScrollbar")
        scy = ttk.Scrollbar(frm, orient=VERTICAL,   style="Tech.Vertical.TScrollbar")

        self.student_table = ttk.Treeview(
            frm, columns=cols, show="headings",
            xscrollcommand=scx.set, yscrollcommand=scy.set,
            style="Tech.Treeview")

        scx.pack(side=BOTTOM, fill=X)
        scy.pack(side=RIGHT,  fill=Y)
        scx.config(command=self.student_table.xview)
        scy.config(command=self.student_table.yview)
        self.student_table.pack(fill=BOTH, expand=1)

        headers = {
            "dep":"Department","course":"Course","year":"Year","sem":"Semester",
            "id":"Student ID","name":"Name","div":"Division","roll":"Roll No",
            "gender":"Gender","dob":"Date of Birth","email":"Email",
            "phone":"Phone","address":"Address","teacher":"Teacher","photo":"Photo"
        }
        for col, head in headers.items():
            self.student_table.heading(col, text=head)
            self.student_table.column(col, width=100, minwidth=80)

        # Alternating row tags
        self.student_table.tag_configure("odd",  background="#0F1A2E")
        self.student_table.tag_configure("even", background=BG_CARD)

        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()

    # ────────────────────────────────────────────
    #  DATA FUNCTIONS
    # ────────────────────────────────────────────
    def _set_status(self, msg, color=ACCENT_TEAL):
        self.status_var.set(f"◉  {msg}")

    def add_data(self):
        if self.var_dep.get() == "Select Department" or not self.var_std_name.get() or not self.var_std_id.get():
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
            return
        try:
            conn = mysql.connector.connect(host="localhost", user="root",
                                           password="7700", database="face_recognizer")
            cur = conn.cursor()
            cur.execute("INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (self.var_dep.get(), self.var_course.get(), self.var_year.get(),
                         self.var_semester.get(), self.var_std_id.get(), self.var_std_name.get(),
                         self.var_div.get(), self.var_roll.get(), self.var_gender.get(),
                         self.var_dob.get(), self.var_email.get(), self.var_phone.get(),
                         self.var_address.get(), self.var_teacher.get(), self.var_radio1.get()))
            conn.commit(); conn.close()
            self.fetch_data()
            self._set_status(f"Student '{self.var_std_name.get()}' added successfully.")
            messagebox.showinfo("SUCCESS", "Student detail added successfully", parent=self.root)
        except Exception as e:
            messagebox.showerror("ERROR", f"Due to: {e}", parent=self.root)

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root",
                                           password="7700", database="face_recognizer")
            cur = conn.cursor()
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            for i, row in enumerate(rows):
                tag = "odd" if i % 2 else "even"
                self.student_table.insert("", END, values=row, tags=(tag,))
            conn.commit(); conn.close()
            self._set_status(f"{len(rows)} records loaded.")
        except Exception as e:
            self._set_status(f"DB Error: {e}", ERROR_RED)

    def get_cursor(self, event=""):
        try:
            item = self.student_table.focus()
            data = self.student_table.item(item)["values"]
            if not data: return
            self.var_dep.set(data[0]);  self.var_year.set(data[1])
            self.var_course.set(data[2]); self.var_semester.set(data[3])
            self.var_std_id.set(data[4]); self.var_std_name.set(data[5])
            self.var_div.set(data[6]);   self.var_roll.set(data[7])
            self.var_gender.set(data[8]); self.var_dob.set(data[9])
            self.var_email.set(data[10]); self.var_phone.set(data[11])
            self.var_address.set(data[12]); self.var_teacher.set(data[13])
            self.var_radio1.set(data[14])
        except Exception: pass

    def update_data(self):
        if not self.var_std_id.get():
            messagebox.showerror("Error", "Select a student first", parent=self.root); return
        if messagebox.askyesno("Update", "Update student details?", parent=self.root):
            try:
                conn = mysql.connector.connect(host="localhost", user="root",
                                               password="7700", database="face_recognizer")
                cur = conn.cursor()
                cur.execute("""UPDATE student SET Dep=%s,Course=%s,Year=%s,Semester=%s,
                    Name=%s,Division=%s,Roll=%s,Gender=%s,Dob=%s,Email=%s,
                    Phone=%s,Address=%s,Teacher=%s,PhotoSample=%s WHERE Student_id=%s""",
                    (self.var_dep.get(), self.var_course.get(), self.var_year.get(),
                     self.var_semester.get(), self.var_std_name.get(), self.var_div.get(),
                     self.var_roll.get(), self.var_gender.get(), self.var_dob.get(),
                     self.var_email.get(), self.var_phone.get(), self.var_address.get(),
                     self.var_teacher.get(), self.var_radio1.get(), self.var_std_id.get()))
                conn.commit(); conn.close()
                self.fetch_data()
                self._set_status("Student record updated.")
                messagebox.showinfo("Success", "Student details updated.", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Due to: {e}", parent=self.root)

    def delete_data(self):
        if not self.var_std_id.get():
            messagebox.showerror("Error", "Student ID required", parent=self.root); return
        if messagebox.askyesno("Delete", "Delete this student?", parent=self.root):
            try:
                conn = mysql.connector.connect(host="localhost", user="root",
                                               password="7700", database="face_recognizer")
                cur = conn.cursor()
                cur.execute("DELETE FROM student WHERE Student_id=%s", (self.var_std_id.get(),))
                conn.commit(); conn.close()
                self.fetch_data(); self.reset_data()
                self._set_status("Student record deleted.")
                messagebox.showinfo("Delete", "Student deleted successfully", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Due to: {e}", parent=self.root)

    def reset_data(self):
        self.var_dep.set("Select Department"); self.var_year.set("Select Year")
        self.var_course.set("Select Course"); self.var_semester.set("Select Semester")
        self.var_std_id.set(""); self.var_std_name.set("")
        self.var_div.set(""); self.var_roll.set("")
        self.var_gender.set("Male"); self.var_dob.set("")
        self.var_email.set(""); self.var_phone.set("")
        self.var_address.set(""); self.var_teacher.set("")
        self.var_radio1.set("")
        self._set_status("Form reset.")

    def take_photo(self):
        if self.var_dep.get() == "Select Department" or not self.var_std_name.get() or not self.var_std_id.get():
            messagebox.showerror("Error", "Fill Department, Student ID and Name before capturing photos", parent=self.root)
            return
        try:
            # Get numeric ID for file naming from DB row count
            conn = mysql.connector.connect(host="localhost", user="root",
                                           password="7700", database="face_recognizer")
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM student")
            result = cur.fetchone()
            conn.close()
            img_id_base = result[0] if result else 0

            face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    return img[y:y+h, x:x+w]
                return None

            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Camera Error", "Could not open webcam. Check if it is connected.", parent=self.root)
                return

            img_count = 0
            self._set_status("Camera open — capturing face samples... Press ENTER or capture 100 images to stop.")

            while True:
                ret, frame = cap.read()
                if not ret:
                    messagebox.showerror("Error", "Failed to read from camera.", parent=self.root)
                    break

                cropped = face_cropped(frame)
                if cropped is not None:
                    img_count += 1
                    face = cv2.resize(cropped, (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                    import os
                    os.makedirs("data", exist_ok=True)
                    file_path = f"data/user.{img_id_base}.{img_count}.jpg"
                    cv2.imwrite(file_path, face)

                    # Draw counter on preview
                    preview = face.copy()
                    cv2.putText(preview, f"Captured: {img_count}/100", (10, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(preview, f"ID: {self.var_std_id.get()}", (10, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)
                    cv2.imshow(f"Capturing — {self.var_std_name.get()}", preview)
                else:
                    # Show live feed even when no face detected
                    cv2.putText(frame, "No face detected", (20, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow(f"Capturing — {self.var_std_name.get()}", frame)

                # Stop on Enter key or after 100 images
                if cv2.waitKey(1) == 13 or img_count >= 100:
                    break

            cap.release()
            cv2.destroyAllWindows()

            if img_count > 0:
                self._set_status(f"Photo capture complete — {img_count} images saved for {self.var_std_name.get()}.")
                messagebox.showinfo("Done",
                    f"Successfully captured {img_count} photo samples!\n\nSaved to: data/user.{img_id_base}.*.jpg\n\nNow click 'Generate Dataset' to train the model.",
                    parent=self.root)
            else:
                self._set_status("No photos captured — no face was detected.")
                messagebox.showwarning("No Face Detected",
                    "Camera ran but no face was detected.\n\nTips:\n• Make sure your face is well-lit\n• Sit closer to the camera\n• Check haarcascade_frontalface_default.xml is in the project folder",
                    parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Due to: {e}", parent=self.root)

    def generate_dataset(self):
        if self.var_dep.get() == "Select Department" or not self.var_std_name.get() or not self.var_std_id.get():
            messagebox.showerror("Error", "All Fields are required", parent=self.root); return
        try:
            conn = mysql.connector.connect(host="localhost", user="root",
                                           password="7700", database="face_recognizer")
            cur = conn.cursor()
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            id_ = len(rows)
            cur.execute("""UPDATE student SET Dep=%s,Course=%s,Year=%s,Semester=%s,Name=%s,
                Division=%s,Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Address=%s,
                Teacher=%s,PhotoSample=%s WHERE Student_id=%s""",
                (self.var_dep.get(), self.var_course.get(), self.var_year.get(),
                 self.var_semester.get(), self.var_std_name.get(), self.var_div.get(),
                 self.var_roll.get(), self.var_gender.get(), self.var_dob.get(),
                 self.var_email.get(), self.var_phone.get(), self.var_address.get(),
                 self.var_teacher.get(), self.var_radio1.get(), self.var_std_id.get()))
            conn.commit(); conn.close()
            self.fetch_data(); self.reset_data()

            face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    return img[y:y+h, x:x+w]
                return None

            cap = cv2.VideoCapture(0)
            img_id = 0
            while True:
                ret, frame = cap.read()
                if not ret: break
                cropped = face_cropped(frame)
                if cropped is not None:
                    img_id += 1
                    face = cv2.resize(cropped, (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(f"data/user.{id_}.{img_id}.jpg", face)
                    cv2.putText(face, str(img_id), (50, 50),
                                cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                    cv2.imshow("Capturing Face Samples", face)
                if cv2.waitKey(1) == 13 or img_id == 200: break
            cap.release(); cv2.destroyAllWindows()
            self._set_status(f"Dataset generated: {img_id} images captured.")
            messagebox.showinfo("Done", "Face dataset generation complete!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Due to: {e}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
