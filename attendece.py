from tkinter import *
from tkinter import ttk
from time import strftime
from datetime import datetime
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os
import csv
from tkinter import filedialog
from tkinter import messagebox


mydata=[]

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendnce")

        

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
        left_inside_frame.place(x=0,y=135,width=720,height=370)


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

        #Button Frame
        btn_frame=Frame(left_inside_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=300,width=715,height=35)

        #Save Button
        save_btn=Button(btn_frame,text="Import CSV",command=self.importCsv,width=19,font=("Times New Roman",12,"bold"),bg="Blue",fg="White")
        save_btn.grid(row=0,column=0)

        #Update button
        update_btn=Button(btn_frame,text="Export CSV",command=self.exportCsv,width=19,font=("Times New Roman",12,"bold"),bg="Blue",fg="White")
        update_btn.grid(row=0,column=1) 
        
        #Delete button
        delete_btn=Button(btn_frame,text="Update",width=19,font=("Times New Roman",12,"bold"),bg="Blue",fg="White")
        delete_btn.grid(row=0,column=2)

        #Reset Button
        reset_btn=Button(btn_frame,text="Reset",command=self.reset_data,width=19,font=("Times New Roman",12,"bold"),bg="Blue",fg="White")
        reset_btn.grid(row=0,column=3)

    #  ==================Right Frame =====================
        RIGHT_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Attendance Details ", font=("Times New Roman", 12, "bold"))
        RIGHT_frame.place(x=750, y=10, width=720, height=580)

        table_frame=Frame(RIGHT_frame,bd=2,relief=RIDGE,bg="white")
        table_frame.place(x=5,y=5,width=700,height=455)


    # =======Scrole Bar & Table==================
     
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.AttendanceReportTable = ttk.Treeview(
        table_frame,
        columns=("id", "roll", "name", "department", "time", "date", "attendance"),
        xscrollcommand=scroll_x.set,
        yscrollcommand=scroll_y.set
    )


        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        self.AttendanceReportTable.heading("id",text="Attendance ID")
        self.AttendanceReportTable.heading("roll",text="Roll")
        self.AttendanceReportTable.heading("name",text="Name")
        self.AttendanceReportTable.heading("department",text="Department")
        self.AttendanceReportTable.heading("time",text="Time")
        self.AttendanceReportTable.heading("date",text="Date")
        self.AttendanceReportTable.heading("attendance",text="Attendance")

        self.AttendanceReportTable["show"]="headings"
        self.AttendanceReportTable.column("id",width=100)
        self.AttendanceReportTable.column("roll",width=100)
        self.AttendanceReportTable.column("name",width=100)
        self.AttendanceReportTable.column("department",width=100)
        self.AttendanceReportTable.column("time",width=100)
        self.AttendanceReportTable.column("date",width=100)
        self.AttendanceReportTable.column("attendance",width=100)

        self.AttendanceReportTable.pack(fill=BOTH,expand=1)

        self.AttendanceReportTable.bind("<ButtonRelease-1>", self.get_cursor)


    def fetchData(self,rows):
            self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
            for i in rows:
                self.AttendanceReportTable.insert("",END,values=i)


#=====================IMPORT CSV================
    def importCsv(self):
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Open CSV",
            filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")),
            parent=self.root
        )
        
        with open(fln) as myfile:
            csvread = csv.reader(myfile, delimiter=",")
            for i in csvread:
                mydata.append(i)
        
        self.fetchData(mydata)
#=====================EXPORT CSV============
    def exportCsv(self):
        try:
            # Check if mydata is empty
            if not mydata:
                messagebox.showerror("No Data", "No data found to export", parent=self.root)
                return False

            # Open file dialog to specify the save location
            fln = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Save CSV",
                defaultextension=".csv",
                filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")),
                parent=self.root
            )
            
            if fln:  # Check if a filename was provided
                with open(fln, mode="w", newline="") as myfile:
                    exp_write = csv.writer(myfile, delimiter=",")
                    for row in mydata:
                        exp_write.writerow(row)
                
                messagebox.showinfo("Data Export", "Your data was exported to " + os.path.basename(fln) + " successfully")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}", parent=self.root)

    def get_cursor(self,event="" ):
        cursor_row = self.AttendanceReportTable.focus()
        content = self.AttendanceReportTable.item(cursor_row)
        rows = content['values']
        self.var_atten_id.set(rows[0])
        self.var_atten_roll.set(rows[1])
        self.var_atten_name.set(rows[2])
        self.var_atten_dep.set(rows[3])
        self.var_atten_time.set(rows[4])
        self.var_atten_date.set(rows[5])
        self.var_atten_attendance.set(rows[6])


    def reset_data(self):
            self.var_atten_id.set("")
            self.var_atten_roll.set("")
            self.var_atten_name.set("")
            self.var_atten_dep.set("")
            self.var_atten_time.set("")
            self.var_atten_date.set("")
            self.var_atten_attendance.set("")
       




if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()


















