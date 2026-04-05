from tkinter import *
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
import mysql.connector
import cv2
import threading
import os
import time

# ─────────────────────────────────────────────
#  COLOUR PALETTE  (matching student.py theme)
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
FONT_BTN     = ("Courier New", 11, "bold")
FONT_MONO    = ("Courier New", 10)


def neon_button(parent, text, cmd, color=BTN_BLUE, width=18, height=1):
    btn = Button(parent, text=text, command=cmd,
                 font=FONT_BTN, bg=color, fg=BG_DARK,
                 activebackground=TEXT_PRIMARY, activeforeground=BG_DARK,
                 relief="flat", bd=0, cursor="hand2",
                 width=width, pady=6)
    def on_enter(e): btn.config(bg=TEXT_PRIMARY)
    def on_leave(e): btn.config(bg=color)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def apply_styles():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Tech.Treeview",
        background=BG_CARD, foreground=TEXT_PRIMARY,
        fieldbackground=BG_CARD, rowheight=24,
        font=FONT_INPUT, bordercolor=BORDER_GLOW)
    style.configure("Tech.Treeview.Heading",
        background=BG_SURFACE, foreground=ACCENT_CYAN,
        font=("Courier New", 9, "bold"), relief="flat")
    style.map("Tech.Treeview",
        background=[("selected", BORDER_GLOW)],
        foreground=[("selected", ACCENT_CYAN)])


class Face_Recognitions:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x820+0+0")
        self.root.title("Face Recognition Attendance System")
        self.root.config(bg=BG_DARK)
        self.root.resizable(True, True)

        apply_styles()

        # State
        self.is_recognizing = False
        self.recognized_ids = set()
        self.attendance_log = []
        self.status_var = StringVar(value="◉  System Ready")
        self.recog_count_var = StringVar(value="0")
        self.confidence_var = StringVar(value="—")
        self.last_name_var = StringVar(value="—")
        self.camera_thread = None

        self._build_header()
        self._build_main()

    # ── HEADER ───────────────────────────────────
    def _build_header(self):
        hdr = Canvas(self.root, width=1530, height=110,
                     bg=BG_DARK, highlightthickness=0)
        hdr.place(x=0, y=0)

        # Grid background
        for i in range(0, 1530, 50):
            hdr.create_line(i, 0, i, 110, fill="#0D1A2E", width=1)
        for j in range(0, 110, 25):
            hdr.create_line(0, j, 1530, j, fill="#0D1A2E", width=1)

        # Accent bars
        hdr.create_rectangle(0, 0, 5, 110, fill=ACCENT_CYAN, outline="")
        hdr.create_rectangle(1525, 0, 1530, 110, fill=ACCENT_TEAL, outline="")
        hdr.create_rectangle(0, 107, 1530, 110, fill=ACCENT_CYAN, outline="")

        # Decorative corner brackets
        for x0, x1 in [(8, 30), (1500, 1522)]:
            hdr.create_line(x0, 10, x0, 30, fill=ACCENT_TEAL, width=2)
            hdr.create_line(x0, 10, x0+22, 10, fill=ACCENT_TEAL, width=2)
            hdr.create_line(x1, 10, x1, 30, fill=ACCENT_TEAL, width=2)
            hdr.create_line(x1-22, 10, x1, 10, fill=ACCENT_TEAL, width=2)
            hdr.create_line(x0, 100, x0, 80, fill=ACCENT_TEAL, width=2)
            hdr.create_line(x0, 100, x0+22, 100, fill=ACCENT_TEAL, width=2)
            hdr.create_line(x1, 100, x1, 80, fill=ACCENT_TEAL, width=2)
            hdr.create_line(x1-22, 100, x1, 100, fill=ACCENT_TEAL, width=2)

        hdr.create_text(765, 40, text="◈  FACE RECOGNITION ATTENDANCE SYSTEM  ◈",
                        font=("Courier New", 22, "bold"), fill=ACCENT_CYAN, anchor="center")
        hdr.create_text(765, 68, text="[ AI-POWERED BIOMETRIC IDENTIFICATION MODULE ]",
                        font=("Courier New", 11), fill=TEXT_SECONDARY, anchor="center")
        hdr.create_text(765, 88, text="─" * 90,
                        font=("Courier New", 8), fill=TEXT_DIM, anchor="center")

        # Status bar
        status_bar = Frame(self.root, bg=BG_SURFACE, height=22)
        status_bar.place(x=0, y=798, width=1530, height=22)
        Label(status_bar, textvariable=self.status_var,
              font=("Consolas", 9), fg=ACCENT_TEAL, bg=BG_SURFACE,
              anchor="w", padx=12).pack(side=LEFT)
        # Clock
        self.clock_var = StringVar()
        Label(status_bar, textvariable=self.clock_var,
              font=("Consolas", 9), fg=TEXT_SECONDARY, bg=BG_SURFACE,
              anchor="e", padx=12).pack(side=RIGHT)
        self._tick_clock()

    def _tick_clock(self):
        self.clock_var.set(datetime.now().strftime("  %A, %d %b %Y   |   %H:%M:%S  "))
        self.root.after(1000, self._tick_clock)

    # ── MAIN LAYOUT ──────────────────────────────
    def _build_main(self):
        main = Frame(self.root, bg=BG_DARK)
        main.place(x=10, y=118, width=1510, height=672)

        # LEFT: Camera feed + controls
        left = LabelFrame(main, text="  ◈  LIVE RECOGNITION FEED  ",
                          font=FONT_SECTION, fg=ACCENT_CYAN,
                          bg=BG_SURFACE, bd=1, relief="solid", labelanchor="nw")
        left.place(x=0, y=0, width=760, height=665)
        self._build_camera_panel(left)

        # RIGHT: Stats + Attendance log
        right = LabelFrame(main, text="  ◈  ATTENDANCE LOG  ",
                           font=FONT_SECTION, fg=ACCENT_CYAN,
                           bg=BG_SURFACE, bd=1, relief="solid", labelanchor="nw")
        right.place(x=768, y=0, width=740, height=665)
        self._build_log_panel(right)

    # ── CAMERA PANEL ─────────────────────────────
    def _build_camera_panel(self, parent):
        # Live feed canvas
        self.cam_canvas = Canvas(parent, width=740, height=420,
                                 bg="#050810", highlightthickness=1,
                                 highlightbackground=BORDER_GLOW)
        self.cam_canvas.place(x=8, y=10)

        # Placeholder
        self.cam_canvas.create_text(370, 180,
            text="◈", font=("Courier New", 60), fill=TEXT_DIM, anchor="center")
        self.cam_canvas.create_text(370, 260,
            text="CAMERA FEED INACTIVE", font=("Courier New", 14, "bold"),
            fill=TEXT_DIM, anchor="center")
        self.cam_canvas.create_text(370, 290,
            text="Press  [ START RECOGNITION ]  to begin",
            font=("Courier New", 10), fill=TEXT_DIM, anchor="center")

        # Stats row
        stats = Frame(parent, bg=BG_CARD, bd=1, relief="solid")
        stats.place(x=8, y=440, width=740, height=70)

        stat_items = [
            ("RECOGNIZED", self.recog_count_var, ACCENT_CYAN),
            ("LAST DETECTED", self.last_name_var, ACCENT_TEAL),
            ("CONFIDENCE", self.confidence_var, ACCENT_PURPLE),
        ]
        for i, (label, var, color) in enumerate(stat_items):
            col = Frame(stats, bg=BG_CARD)
            col.place(x=i*247, y=0, width=246, height=70)
            if i > 0:
                Frame(col, bg=BORDER_GLOW, width=1).place(x=0, y=8, width=1, height=54)
            Label(col, text=label, font=("Consolas", 8, "bold"),
                  fg=TEXT_DIM, bg=BG_CARD).place(x=15, y=10)
            Label(col, textvariable=var, font=("Courier New", 18, "bold"),
                  fg=color, bg=BG_CARD).place(x=15, y=28)

        # Control buttons
        ctrl = Frame(parent, bg=BG_DARK)
        ctrl.place(x=8, y=520, width=740, height=50)

        self.start_btn = neon_button(ctrl, "▶  START RECOGNITION",
                                     self.start_recognition, color=BTN_GREEN, width=22)
        self.start_btn.pack(side=LEFT, padx=(0, 6), expand=True, fill=X)

        self.stop_btn = neon_button(ctrl, "■  STOP",
                                    self.stop_recognition, color=BTN_RED, width=12)
        self.stop_btn.pack(side=LEFT, padx=(0, 6), expand=True, fill=X)
        self.stop_btn.config(state=DISABLED, bg="#3A1A1F")

        clear_btn = neon_button(ctrl, "↺  CLEAR LOG",
                                self.clear_log, color=ACCENT_PURPLE, width=14)
        clear_btn.pack(side=LEFT, expand=True, fill=X)

        # Info box
        info = Frame(parent, bg=BG_CARD, bd=1, relief="solid")
        info.place(x=8, y=580, width=740, height=75)

        tips = [
            "▸  Confidence threshold: 77% — faces below this are marked Unknown",
            "▸  Press ENTER inside the camera window to stop recognition",
            "▸  Each student is recorded only ONCE per session (no duplicates)",
            "▸  Attendance auto-saved to  Yash.csv  with timestamp",
        ]
        for i, tip in enumerate(tips):
            Label(info, text=tip, font=("Consolas", 8), fg=TEXT_DIM,
                  bg=BG_CARD, anchor="w").place(x=10, y=5 + i*16)

    # ── LOG PANEL ────────────────────────────────
    def _build_log_panel(self, parent):
        # Today's summary cards
        summary = Frame(parent, bg=BG_SURFACE)
        summary.place(x=8, y=10, width=722, height=70)

        self.total_var   = StringVar(value="0")
        self.session_var = StringVar(value="0")
        self.time_var    = StringVar(value="—")

        cards = [
            ("TOTAL TODAY", self.total_var,   ACCENT_CYAN),
            ("THIS SESSION", self.session_var, ACCENT_TEAL),
            ("LAST MARKED",  self.time_var,    ACCENT_PURPLE),
        ]
        for i, (lbl, var, color) in enumerate(cards):
            c = Frame(summary, bg=INPUT_BG, bd=1, relief="solid")
            c.place(x=i*242, y=0, width=238, height=68)
            Label(c, text=lbl, font=("Consolas", 8, "bold"),
                  fg=TEXT_DIM, bg=INPUT_BG).place(x=10, y=8)
            Label(c, textvariable=var, font=("Courier New", 20, "bold"),
                  fg=color, bg=INPUT_BG).place(x=10, y=26)

        # Table
        tbl_frame = Frame(parent, bg=BG_CARD, bd=1, relief="solid")
        tbl_frame.place(x=8, y=90, width=722, height=480)

        scx = ttk.Scrollbar(tbl_frame, orient=HORIZONTAL)
        scy = ttk.Scrollbar(tbl_frame, orient=VERTICAL)

        self.log_table = ttk.Treeview(tbl_frame,
            columns=("sid", "roll", "name", "dep", "time", "date", "status"),
            show="headings",
            xscrollcommand=scx.set,
            yscrollcommand=scy.set,
            style="Tech.Treeview")

        scx.pack(side=BOTTOM, fill=X)
        scy.pack(side=RIGHT, fill=Y)
        scx.config(command=self.log_table.xview)
        scy.config(command=self.log_table.yview)
        self.log_table.pack(fill=BOTH, expand=1)

        cols = {
            "sid": ("STUDENT ID", 90),
            "roll": ("ROLL NO", 110),
            "name": ("NAME", 130),
            "dep": ("DEPARTMENT", 120),
            "time": ("TIME", 90),
            "date": ("DATE", 90),
            "status": ("STATUS", 80),
        }
        for col, (heading, width) in cols.items():
            self.log_table.heading(col, text=heading)
            self.log_table.column(col, width=width, minwidth=60)

        self.log_table.tag_configure("present", foreground=ACCENT_TEAL)
        self.log_table.tag_configure("odd", background="#0F1A2E")
        self.log_table.tag_configure("even", background=BG_CARD)

        # Export button
        exp_btn = neon_button(parent, "📤  EXPORT ATTENDANCE CSV",
                              self.export_csv, color=ACCENT_CYAN, width=30)
        exp_btn.place(x=8, y=580, width=722, height=40)

        # Load existing attendance
        self._load_existing_attendance()

    # ── ATTENDANCE FUNCTIONS ─────────────────────
    def mark_attendance(self, i, r, n, d):
        try:
            now = datetime.now()
            date_str = now.strftime("%d/%m/%Y")
            time_str = now.strftime("%H:%M:%S")

            # Write to CSV
            with open("Yash.csv", "a+", newline="\n") as f:
                f.seek(0)
                existing = f.read()
                # Only write if student not already present today
                if str(i) not in existing or date_str not in existing:
                    f.write(f"\n{i},{r},{n},{d},{time_str},{date_str},Present")

            # Update GUI log table
            row_count = len(self.log_table.get_children())
            tag = "odd" if row_count % 2 else "even"
            self.log_table.insert("", 0, values=(i, r, n, d, time_str, date_str, "✓ Present"),
                                  tags=(tag, "present"))

            # Update stats
            self.session_var.set(str(len(self.recognized_ids)))
            self.time_var.set(time_str)
            self.last_name_var.set(str(n)[:14])
            self._update_total_count()
            self._set_status(f"Attendance marked — {n}  [{time_str}]")

        except Exception as e:
            self._set_status(f"CSV write error: {e}")

    def _load_existing_attendance(self):
        """Load today's records from CSV into the table on startup."""
        try:
            if not os.path.exists("Yash.csv"):
                return
            today = datetime.now().strftime("%d/%m/%Y")
            with open("Yash.csv", "r") as f:
                lines = f.readlines()
            count = 0
            for i, line in enumerate(lines):
                parts = line.strip().split(",")
                if len(parts) >= 6 and parts[5] == today:
                    tag = "odd" if i % 2 else "even"
                    self.log_table.insert("", END, values=tuple(parts[:7]),
                                          tags=(tag, "present"))
                    count += 1
            self.total_var.set(str(count))
        except Exception:
            pass

    def _update_total_count(self):
        try:
            if not os.path.exists("Yash.csv"):
                return
            today = datetime.now().strftime("%d/%m/%Y")
            with open("Yash.csv", "r") as f:
                lines = f.readlines()
            count = sum(1 for l in lines if today in l)
            self.total_var.set(str(count))
        except Exception:
            pass

    def clear_log(self):
        self.log_table.delete(*self.log_table.get_children())
        self.recognized_ids.clear()
        self.recog_count_var.set("0")
        self.session_var.set("0")
        self.last_name_var.set("—")
        self.confidence_var.set("—")
        self._set_status("Session log cleared.")

    def export_csv(self):
        self._set_status("Attendance already auto-saved to Yash.csv")

    def _set_status(self, msg):
        self.status_var.set(f"◉  {msg}")

    # ── RECOGNITION ENGINE ───────────────────────
    def start_recognition(self):
        if self.is_recognizing:
            return
        # Validate files exist
        if not os.path.exists("Classifier.xml"):
            from tkinter import messagebox
            messagebox.showerror("Missing File",
                "Classifier.xml not found!\nPlease train the model first using train.py",
                parent=self.root)
            return
        if not os.path.exists("haarcascade_frontalface_default.xml"):
            from tkinter import messagebox
            messagebox.showerror("Missing File",
                "haarcascade_frontalface_default.xml not found!\nMake sure it's in your project folder.",
                parent=self.root)
            return

        self.is_recognizing = True
        self.recognized_ids.clear()
        self.start_btn.config(state=DISABLED, bg="#1A3A2A")
        self.stop_btn.config(state=NORMAL, bg=BTN_RED)
        self._set_status("Recognition started — camera active...")

        # Run in background thread so UI stays responsive
        self.camera_thread = threading.Thread(target=self._recognition_loop, daemon=True)
        self.camera_thread.start()

    def stop_recognition(self):
        self.is_recognizing = False
        self.start_btn.config(state=NORMAL, bg=BTN_GREEN)
        self.stop_btn.config(state=DISABLED, bg="#3A1A1F")
        self._set_status(f"Recognition stopped — {len(self.recognized_ids)} student(s) marked this session.")
        # Reset camera canvas
        self.cam_canvas.delete("all")
        self.cam_canvas.create_text(370, 180, text="◈",
            font=("Courier New", 60), fill=TEXT_DIM, anchor="center")
        self.cam_canvas.create_text(370, 260, text="CAMERA FEED INACTIVE",
            font=("Courier New", 14, "bold"), fill=TEXT_DIM, anchor="center")
        self.cam_canvas.create_text(370, 290, text="Press  [ START RECOGNITION ]  to begin",
            font=("Courier New", 10), fill=TEXT_DIM, anchor="center")

    def _get_student_info(self, student_id):
        """Single DB call to fetch all student fields at once — faster than 4 separate queries."""
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="mysql", database="face_recognizer")
            cur = conn.cursor()
            cur.execute(
                "SELECT Student_id, Roll, Name, Dep FROM student WHERE Student_id=%s",
                (student_id,))
            row = cur.fetchone()
            conn.close()
            if row:
                return str(row[0]), str(row[1]), str(row[2]), str(row[3])
        except Exception as e:
            print(f"DB error: {e}")
        return "Unknown", "Unknown", "Unknown", "Unknown"

    def _recognition_loop(self):
        """Runs in a separate thread. Processes camera frames and updates the GUI."""
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("Classifier.xml")

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 740)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 420)
        cap.set(cv2.CAP_PROP_FPS, 30)

        frame_skip = 0  # Process every other frame for speed

        while self.is_recognizing:
            ret, frame = cap.read()
            if not ret:
                break

            frame_skip += 1
            display = frame.copy()

            # Only run face detection every 2nd frame (doubles speed)
            if frame_skip % 2 == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=8,
                    minSize=(80, 80))  # minSize filters tiny false positives

                for (x, y, w, h) in faces:
                    face_roi = gray[y:y+h, x:x+w]
                    student_id, predict = clf.predict(face_roi)
                    confidence = int(100 * (1 - predict / 300))

                    if confidence > 77:
                        sid, roll, name, dep = self._get_student_info(student_id)

                        # Neon green box for recognised
                        cv2.rectangle(display, (x, y), (x+w, y+h), (0, 245, 196), 2)

                        # Semi-transparent label background
                        overlay = display.copy()
                        cv2.rectangle(overlay, (x, y-90), (x+w, y), (10, 14, 26), -1)
                        cv2.addWeighted(overlay, 0.7, display, 0.3, 0, display)

                        cv2.putText(display, f"ID: {sid}",
                            (x+6, y-70), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 212, 255), 1)
                        cv2.putText(display, f"Roll: {roll}",
                            (x+6, y-52), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 245, 196), 1)
                        cv2.putText(display, f"{name}",
                            (x+6, y-32), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
                        cv2.putText(display, f"Dept: {dep}  |  {confidence}%",
                            (x+6, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

                        # Update GUI stats (thread-safe via after)
                        self.root.after(0, lambda c=confidence, n=name: (
                            self.confidence_var.set(f"{c}%"),
                            self.last_name_var.set(n[:14])
                        ))

                        # Mark attendance only once per session
                        if student_id not in self.recognized_ids:
                            self.recognized_ids.add(student_id)
                            self.root.after(0, lambda c=confidence: 
                                self.recog_count_var.set(str(len(self.recognized_ids))))
                            # Schedule attendance marking on main thread
                            self.root.after(0, lambda s=sid, r=roll, n=name, d=dep:
                                self.mark_attendance(s, r, n, d))
                    else:
                        # Red box for unknown
                        cv2.rectangle(display, (x, y), (x+w, y+h), (255, 71, 87), 2)
                        overlay2 = display.copy()
                        cv2.rectangle(overlay2, (x, y-30), (x+w, y), (10, 14, 26), -1)
                        cv2.addWeighted(overlay2, 0.7, display, 0.3, 0, display)
                        cv2.putText(display, "UNKNOWN",
                            (x+6, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 71, 87), 2)

            # HUD overlay on frame
            h_frame, w_frame = display.shape[:2]
            cv2.rectangle(display, (0, 0), (w_frame, 28), (10, 14, 26), -1)
            cv2.putText(display, f"LIVE  |  Session: {len(self.recognized_ids)} marked  |  {datetime.now().strftime('%H:%M:%S')}",
                (10, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 212, 255), 1)

            # Convert to tkinter image and update canvas
            rgb = cv2.cvtColor(display, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(rgb)
            img_pil = img_pil.resize((740, 420), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img_pil)

            # Must update canvas on main thread
            self.root.after(0, lambda p=photo: self._update_canvas(p))

        cap.release()
        cv2.destroyAllWindows()
        if self.is_recognizing:
            self.root.after(0, self.stop_recognition)

    def _update_canvas(self, photo):
        """Update the canvas with the latest frame (called from main thread)."""
        try:
            self.cam_canvas.image = photo  # Prevent garbage collection
            self.cam_canvas.create_image(0, 0, image=photo, anchor=NW)
        except Exception:
            pass


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognitions(root)
    root.mainloop()