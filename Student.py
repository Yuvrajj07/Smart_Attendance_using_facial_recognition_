from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")


        #=====Veriables=====
        self.var_dep=StringVar()
        self.var_course=StringVar()
        self.var_year=StringVar()
        self.var_semester=StringVar()
        self.var_std_id=StringVar()
        self.var_std_name=StringVar()
        self.var_div=StringVar()
        self.var_roll=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_phone=StringVar()
        self.var_address=StringVar()
        self.var_teacher=StringVar()



        img = Image.open(r"C:\Face Recognition Attendence System\college_images\face-recognition.png")
        img = img.resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=500, height=130)

        # Second Image
        img1 = Image.open(r"C:\Face Recognition Attendence System\college_images\smart-attendance.jpg")
        img1 = img1.resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl1 = Label(self.root, image=self.photoimg1)
        f_lbl1.place(x=500, y=0, width=500, height=130)

        # Third Image
        img2 = Image.open(r"C:\Face Recognition Attendence System\college_images\Sudent.jpg")
        img2 = img2.resize((530, 130), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl2 = Label(self.root, image=self.photoimg2)
        f_lbl2.place(x=1000, y=0, width=530, height=130)


        # Background Image
        img3 = Image.open(r"C:\Face Recognition Attendence System\college_images\wp2551980.jpg")
        img3 = img3.resize((1530, 710), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=130, width=1530, height=710)

        title_lbl = Label(bg_img, text="Student Management System",
                          font=("times new roman", 35, "bold"), bg="white", fg="dark green")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        main_frame=Frame(bg_img,bd=2,bg="white")
        main_frame.place(x=20,y=55,width=1480,height=600)

         #left lable frame
        Left_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Details",font=("Times New Roman",12,"bold"))
        Left_frame.place(x=10,y=10,width=730,height=580)

        img_left = Image.open(r"C:\Face Recognition Attendence System\college_images\AdobeStock.jpeg")
        img_left = img_left.resize((720, 130), Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)

        f_lbl2 = Label(Left_frame, image=self.photoimg_left)
        f_lbl2.place(x=5, y=0, width=720, height=130)


        # current course  Information
        current_course_frame=LabelFrame(Left_frame,bd=2,bg="white",relief=RIDGE,text="Current Course Information",font=("Times New Roman",12,"bold"))
        current_course_frame.place(x=5,y=135,width=720,height=125)

        #Department
        dep_label=Label(current_course_frame,text="Department",font=("Times New Roman",12,"bold"),bg="white")
        dep_label.grid(row=0,column=0,padx=10,sticky=W)

        dep_combo=ttk.Combobox(current_course_frame,font=("Times New Roman",12,"bold"),state="read only",width=17)
        dep_combo["values"]=("Select Department","Computer","IT","Civil","Mechnical")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)

        #Course
        course_label=Label(current_course_frame,text="Course",font=("Times New Roman",12,"bold"),bg="white")
        course_label.grid(row=0,column=2,padx=10,sticky=W)

        course_combo=ttk.Combobox(current_course_frame,font=("Times New Roman",12,"bold"),state="read only",width=20)
        course_combo["values"]=("Select Course","FE","SE","TE","BE")
        course_combo.current(0)
        course_combo.grid(row=0,column=3,padx=2,pady=10,sticky=W)

        #Year 
        year_label=Label(current_course_frame,text="Course",font=("Times New Roman",12,"bold"),bg="white")
        year_label.grid(row=1,column=0,padx=10,sticky=W)

        year_combo=ttk.Combobox(current_course_frame,font=("Times New Roman",12,"bold"),state="read only",width=17)
        year_combo["values"]=("Select Year","2020-21","2021-22","2022-23","2023-24")
        year_combo.current(0)
        year_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)

        #Semester
        semester_label=Label(current_course_frame,text="Semester",font=("Times New Roman",12,"bold"),bg="white")
        semester_label.grid(row=1,column=2,padx=10,sticky=W)

        semester_combo=ttk.Combobox(current_course_frame,font=("Times New Roman",12,"bold"),state="read only",width=20)
        semester_combo["values"]=("Select Semester","Semester-1","Semester-2")
        semester_combo.current(0)
        semester_combo.grid(row=1,column=3,padx=2,pady=10,sticky=W)

        # Class Student Information
        class_Student_frame=LabelFrame(Left_frame,bd=2,bg="white",relief=RIDGE,text="Current Course Information",font=("Times New Roman",12,"bold"))
        class_Student_frame.place(x=5,y=250,width=720,height=300)

        studentId_label = Label(class_Student_frame, text="Student ID:", font=("Times New Roman", 12, "bold"), bg="white")
        studentId_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        studentId_entry = ttk.Entry(class_Student_frame, textvariable=self.var_std_id, font=("Times New Roman", 12, "bold"), width=20)
        studentId_entry.grid(row=2, column=1, padx=2, pady=5, sticky=W)

        # Student Name
        studentName_label = Label(class_Student_frame, text="Student Name:", font=("Times New Roman", 12, "bold"), bg="white")
        studentName_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)

        studentName_entry = ttk.Entry(class_Student_frame, textvariable=self.var_std_name, font=("Times New Roman", 12, "bold"), width=20)
        studentName_entry.grid(row=2, column=3, padx=2, pady=5, sticky=W)

        # Class Divison
        class_div_label = Label(class_Student_frame, text="Class Division:", font=("Times New Roman", 12, "bold"), bg="white")
        class_div_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)

        class_div_entry = ttk.Entry(class_Student_frame, textvariable=self.var_div, font=("Times New Roman", 12, "bold"), width=20)
        class_div_entry.grid(row=3, column=1, padx=2, pady=5, sticky=W)

        # Roll No
        roll_no_label = Label(class_Student_frame, text="Roll No:", font=("Times New Roman", 12, "bold"), bg="white")
        roll_no_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)

        roll_no_entry = ttk.Entry(class_Student_frame, textvariable=self.var_roll, font=("Times New Roman", 12, "bold"), width=20)
        roll_no_entry.grid(row=3, column=3, padx=2, pady=5, sticky=W)

        # Gender
        gender_label = Label(class_Student_frame, text="Gender:", font=("Times New Roman", 12, "bold"), bg="white")
        gender_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)

        gender_entry = ttk.Entry(class_Student_frame, textvariable=self.var_gender, font=("Times New Roman", 12, "bold"), width=20)
        gender_entry.grid(row=4, column=1, padx=2, pady=5, sticky=W)

        # Date of Birth
        dob_label = Label(class_Student_frame, text="Date of Birth:", font=("Times New Roman", 12, "bold"), bg="white")
        dob_label.grid(row=4, column=2, padx=10, pady=5, sticky=W)

        dob_entry = ttk.Entry(class_Student_frame, textvariable=self.var_dob, font=("Times New Roman", 12, "bold"), width=20)
        dob_entry.grid(row=4, column=3, padx=2, pady=5, sticky=W)

        # Email
        email_label = Label(class_Student_frame, text="Email:", font=("Times New Roman", 12, "bold"), bg="white")
        email_label.grid(row=5, column=0, padx=10, pady=5, sticky=W)

        email_entry = ttk.Entry(class_Student_frame, textvariable=self.var_email, font=("Times New Roman", 12, "bold"), width=20)
        email_entry.grid(row=5, column=1, padx=2, pady=5, sticky=W)

        # Phone No
        phone_label = Label(class_Student_frame, text="Phone:", font=("Times New Roman", 12, "bold"), bg="white")
        phone_label.grid(row=5, column=2, padx=10, pady=5, sticky=W)

        phone_entry = ttk.Entry(class_Student_frame, textvariable=self.var_phone, font=("Times New Roman", 12, "bold"), width=20)
        phone_entry.grid(row=5, column=3, padx=2, pady=5, sticky=W)

        # Address
        address_label = Label(class_Student_frame, text="Address:", font=("Times New Roman", 12, "bold"), bg="white")
        address_label.grid(row=6, column=0, padx=10, pady=5, sticky=W)

        address_entry = ttk.Entry(class_Student_frame, textvariable=self.var_address, font=("Times New Roman", 12, "bold"), width=20)
        address_entry.grid(row=6, column=1, padx=2, pady=5, sticky=W)

        # Teacher Name
        teacher_label = Label(class_Student_frame, text="Teacher:", font=("Times New Roman", 12, "bold"), bg="white")
        teacher_label.grid(row=6, column=2, padx=10, pady=5, sticky=W)

        teacher_entry = ttk.Entry(class_Student_frame, textvariable=self.var_teacher, font=("Times New Roman", 12, "bold"), width=20)
        teacher_entry.grid(row=6, column=3, padx=2, pady=5, sticky=W)
        #Radio Button
        self.var_radio1=StringVar()
        radiobtn1=ttk.Radiobutton(current_course_frame,text="Take photo sample",value="Yes")
        radiobtn1.grid(row=6,column=0)

        self.var_radio2=StringVar()
        radiobtn2=ttk.Radiobutton(current_course_frame,text="No photo sample",value="Yes")
        radiobtn2.grid(row=6,column=1)

        #Button Frame
        btn_frame=Frame(current_course_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=200,width=715,height=35)

        #Save Button
        save_btn=Button(btn_frame,text="Save",width=19,font=("Times New Roman",12,"bold"),bg="Blue",fg="White")
        save_btn.grid(row=0,column=0)

        #Update button
        update_btn=Button(btn_frame,text="Update",width=19,font=("Times New Roman",12,"bold"),bg="Blue",fg="White")
        update_btn.grid(row=0,column=1)
        
        #Delete button
        delete_btn=Button(btn_frame,text="Delete",width=19,font=("Times New Roman",12,"bold"),bg="Blue",fg="White")
        delete_btn.grid(row=0,column=2)

        #Reset Button
        reset_btn=Button(btn_frame,text="Reset",width=19,font=("Times New Roman",12,"bold"),bg="Blue",fg="White")
        reset_btn.grid(row=0,column=3)

        #Button Frame
        btn1_frame=Frame(current_course_frame,bd=2,relief=RIDGE,bg="white")
        btn1_frame.place(x=0,y=235,width=715,height=35)
        
        #Take Phot Sample 
        take_photo_btn=Button(btn1_frame,text="Take Photo",width=38,font=("Times New Roman",12,"bold"),bg="Blue",fg="White")
        take_photo_btn.grid(row=0,column=0)

        #Update Photo Sample 
        update_photo_btn=Button(btn1_frame,text="Update Photo",width=39,font=("Times New Roman",12,"bold"),bg="Blue",fg="White")
        update_photo_btn.grid(row=0,column=1)



         # Right label frame
        RIGHT_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Current Course Information", font=("Times New Roman", 12, "bold"))
        RIGHT_frame.place(x=750, y=10, width=720, height=580)

        # Loading the image
        img_right = Image.open(r"C:\Face Recognition Attendence System\college_images\gettyimage.jpg")
        img_right = img_right.resize((720, 130), Image.Resampling.LANCZOS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)  # Use self.photoimg_right here

        # Display the image in the label
        f_lbl2 = Label(RIGHT_frame, image=self.photoimg_right)
        f_lbl2.place(x=5, y=0, width=720, height=130)

        # =======Search System==========
        Search_frame = LabelFrame(RIGHT_frame, bd=2, bg="white", relief=RIDGE, text="Current Course Information", font=("Times New Roman", 12, "bold"))
        Search_frame.place(x=5, y=135, width=710, height=70)

        search_label=Label(Search_frame,text="Search By:",font=("Times New Roman", 15, "bold"),bg="white",fg="black")
        search_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)

        search_combo=ttk.Combobox(Search_frame,font=("Times New Roman", 13, "bold"),state="readonly",width="15")
        search_combo["values"]=("Select","Roll_No","Phone_No")
        search_combo.current(0)
        search_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)

        search_entry=ttk.Entry(Search_frame,width=15,font=("Times New Roman",13,"bold"))
        search_entry.grid(row=0,column=2,padx=10,pady=5,sticky=W)

        search_btn=Button(Search_frame,text="Search",width=10,font=("Times New Roman", 12, "bold"),bg="blue",fg="white")
        search_btn.grid(row=0,column=3,padx=4)

        showAll_btn=Button(Search_frame,text="Show All",width=10,font=("Times New Roman", 12, "bold"),bg="blue",fg="white")
        showAll_btn.grid(row=0,column=4,padx=4)

          #========Table Frame ===========
        # Create the table frame
        table_frame = Frame(RIGHT_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=210, width=710, height=250)

        # Create horizontal and vertical scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        # Create the Treeview
        self.student_table = ttk.Treeview(table_frame, 
                                        column=("dep", "course", "year", "sem", "id", "name", "dic", "roll", 
                                                "gender", "dob", "email", "phone", "address", "teacher", "photo"), 
                                        xscrollcommand=scroll_x.set, 
                                        yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        # Configure the scrollbars to work with the Treeview
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # Pack or grid the Treeview inside the frame
        self.student_table.pack(fill=BOTH, expand=1)

        # Set the headings (optional)
        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("id", text="Student ID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("dic", text="Date of Issue")
        self.student_table.heading("roll", text="Roll No")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="Date of Birth")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone No")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("teacher", text="Teacher")
        self.student_table.heading("photo", text="Photo Status")

        # Configure the column widths (optional)
        self.student_table.column("dep", width=100)
        self.student_table.column("course", width=100)
        self.student_table.column("year", width=100)
        self.student_table.column("sem", width=100)
        self.student_table.column("id", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("dic", width=100)
        self.student_table.column("roll", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("dob", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=100)
        self.student_table.column("teacher", width=100)
        self.student_table.column("photo", width=100)

        # Set the table to display columns and data
        self.student_table["show"] = "headings  "


    #======function declartion===============
#     def add_data(self):

        




































if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
      