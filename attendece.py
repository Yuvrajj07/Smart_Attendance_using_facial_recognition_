from tkinter import *
from tkinter import ttk
from time import strftime
from datetime import datetime
from PIL import Image, ImageTk
import mysql.connector
import cv2


class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendnce")


        # img = Image.open(r"college_images\facial-recognition_0.jpg")
        # img = img.resize((800, 200), Image.Resampling.LANCZOS)
        # self.photoimg = ImageTk.PhotoImage(img)

        # f_lbl = Label(self.root, image=self.photoimg)
        # f_lbl.place(x=0, y=0, width=800, height=200)

        # # Second Image
        # img1 = Image.open(r"college_images\smart-attendance.jpg")
        # img1 = img1.resize((800, 200), Image.Resampling.LANCZOS)
        # self.photoimg1 = ImageTk.PhotoImage(img1)

        # f_lbl1 = Label(self.root, image=self.photoimg1)
        # f_lbl1.place(x=800, y=0, width=800, height=200)


        # img3 = Image.open(r"C:wp2551980.jpg")
        # img3 = img3.resize((1530, 710), Image.Resampling.LANCZOS)
        # self.photoimg3 = ImageTk.PhotoImage(img3)

        # bg_img = Label(self.root, image=self.photoimg3)
        # bg_img.place(x=0, y=200, width=1530, height=710)

        # title_lbl = Label(bg_img, text="Attendance Management System",
        #                   font=("times new roman", 35, "bold"), bg="white", fg="dark green")
        # title_lbl.place(x=0, y=200, width=1530, height=45)


        # First Image
        img = Image.open(r"college_images/facial-recognition_0.jpg")
        img = img.resize((800, 200), Image.LANCZOS)  # Use Image.LANCZOS
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=800, height=200)

        # Second Image
        img1 = Image.open(r"college_images/smart-attendance.jpg")
        img1 = img1.resize((800, 200), Image.LANCZOS)  # Use Image.LANCZOS
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl1 = Label(self.root, image=self.photoimg1)
        f_lbl1.place(x=800, y=0, width=800, height=200)

        # Background Image
        img3 = Image.open(r"college_images/wp2551980.jpg")
        img3 = img3.resize((1530, 710), Image.LANCZOS)  # Use Image.LANCZOS
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=200, width=1530, height=710)

        # Title Label
        title_lbl = Label(bg_img, text="Attendance Management System",
                          font=("times new roman", 35, "bold"), bg="white", fg="dark green")
        title_lbl.place(x=0, y=0, width=1530, height=45)  # Adjusted the position

        main_frame=Frame(bg_img,bd=2,bg="white")
        main_frame.place(x=20,y=55,width=1480,height=600)
    #   =============Left Frame================
        Left_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Attendence  Details",font=("Times New Roman",12,"bold"))
        Left_frame.place(x=10,y=10,width=730,height=580)

        img_left = Image.open(r"college_images\AdobeStock.jpeg")
        img_left = img_left.resize((720, 130), Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)

        f_lbl2 = Label(Left_frame, image=self.photoimg_left)
        f_lbl2.place(x=5, y=0, width=720, height=130)

        left_inside_frame=Frame(Left_frame,bd=2,relief=RIDGE,bg="white")
        left_inside_frame.place(x=0,y=135,width=720,height=300)


        # LabeleND Entry

        attendanceId_label = Label(left_inside_frame, text="Attendance ID:", font=("Times New Roman", 12, "bold"), bg="white")
        attendanceId_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        attendanceId_entry = ttk.Entry(left_inside_frame, font=("Times New Roman", 12, "bold"), width=28)
        attendanceId_entry.grid(row=0, column=1, padx=2, pady=5, sticky=W)

        # ===Roll no=============
        Roll_label = Label(left_inside_frame, text="Roll:", font=("Times New Roman", 12, "bold"), bg="white")
        Roll_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        Roll_entry = ttk.Entry(left_inside_frame, font=("Times New Roman", 12, "bold"), width=28)
        Roll_entry.grid(row=0, column=3, padx=2, pady=5, sticky=W)

        # =======Name 
        name_label = Label(left_inside_frame, text="Name:", font=("Times New Roman", 12, "bold"), bg="white")
        name_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        name_entry = ttk.Entry(left_inside_frame, font=("Times New Roman", 12, "bold"), width=28)
        name_entry.grid(row=1, column=1, padx=2, pady=5, sticky=W)

        # =============Department========

        dep_label = Label(left_inside_frame, text="Department:", font=("Times New Roman", 12, "bold"), bg="white")
        dep_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)

        dep_entry = ttk.Entry(left_inside_frame, font=("Times New Roman", 12, "bold"), width=28)
        dep_entry.grid(row=1, column=3, padx=2, pady=5, sticky=W)
        
        # ========Time===========
        time_label = Label(left_inside_frame, text="Time:", font=("Times New Roman", 12, "bold"), bg="white")
        time_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        time_entry = ttk.Entry(left_inside_frame, font=("Times New Roman", 12, "bold"), width=28)
        time_entry.grid(row=2, column=1, padx=2, pady=5, sticky=W)

        # ===============date 
        date_label = Label(left_inside_frame, text="Date:", font=("Times New Roman", 12, "bold"), bg="white")
        date_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)

        date_entry = ttk.Entry(left_inside_frame, font=("Times New Roman", 12, "bold"), width=28)
        date_entry.grid(row=2, column=3, padx=2, pady=5, sticky=W)

        # ==================Attendance Statu===========================
        AttendanceStatus_label=Label(left_inside_frame,text="Attendance Status:",font=("Times New Roman",12,"bold"),bg="white")
        AttendanceStatus_label.grid(row=3,column=0)

        AttendanceStatus_combo=ttk.Combobox(left_inside_frame,font=("Times New Roman",12,"bold"),state="read only",width=28)
        AttendanceStatus_combo["values"]=("Status","Present","Absent")
        AttendanceStatus_combo.current(0)
        AttendanceStatus_combo.grid(row=3,column=1,pady=8)




















    #  ==================Right Frame =====================
        RIGHT_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Attendance Details ", font=("Times New Roman", 12, "bold"))
        RIGHT_frame.place(x=750, y=10, width=720, height=580)
   


if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()