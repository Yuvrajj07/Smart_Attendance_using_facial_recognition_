from tkinter import *
from tkinter import ttk
from time import strftime
from datetime import datetime
from PIL import Image, ImageTk
import mysql.connector
import cv2


class Face_Recognitions:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="Face Recognition",
                          font=("times new roman", 35, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # 1st Image
        img_top = Image.open(r"college_images\face_detector1.jpg")
        img_top = img_top.resize((650, 700), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl_top = Label(self.root, image=self.photoimg_top)
        f_lbl_top.place(x=0, y=55, width=650, height=700)

        # 2nd Image
        img_bottom = Image.open(r"college_images\facial_recognition_system_identification_digital_id_security_scanning_thinkstock_858236252_3x3-100740902-large.jpg")
        img_bottom = img_bottom.resize((950, 700), Image.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        f_lbl_bottom = Label(self.root, image=self.photoimg_bottom)
        f_lbl_bottom.place(x=650, y=55, width=950, height=700)

        b1_1 = Button(f_lbl_bottom, text="Face Recognition", cursor="hand2",
                      font=("times new roman", 18, "bold"), bg="darkblue", fg="white", command=self.face_recog)
        b1_1.place(x=365, y=620, width=200, height=40)

    # ======================Attendence====================
    def mark_attendance(self,i,r,n,d):
        with open("Yash.csv","r+",newline="\n") as f:
            myDataList=f.readlines()
            name_list=[]
            for line in myDataList:
                entry=line.split((",")) 
                name_list.append(entry[0])
            if((i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list)):
                now=datetime.now()
                d1=now.strftime("%d/%m/%Y")
                dtString=now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{dtString},{d1},Present")





    # ===============Face Recognition==============
    def face_recog(self):
        recognized_ids = set()  # Set to track recognized IDs

        def draw_boundry(img, classifier, scaleFactor, minNeighbours, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbours)

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                try:
                    conn = mysql.connector.connect(host="localhost", username="root", password="mysql", database="face_recognizer")
                    my_cursor = conn.cursor()

                    # Fetching the Name
                    my_cursor.execute("SELECT Name FROM student WHERE Student_id=%s", (id,))
                    n = my_cursor.fetchone()
                    n = "+".join(n) if n is not None else "Unknown"

                    # Fetching the Roll
                    my_cursor.execute("SELECT Roll FROM student WHERE Student_id=%s", (id,))
                    r = my_cursor.fetchone()
                    r = "+".join(r) if r is not None else "Unknown"

                    # Fetching the Department
                    my_cursor.execute("SELECT Dep FROM student WHERE Student_id=%s", (id,))
                    d = my_cursor.fetchone()
                    d = "+".join(d) if d is not None else "Unknown"

                    # =====Student Id===========
                    my_cursor.execute("SELECT Student_id FROM student WHERE Student_id=%s", (id,))
                    i = my_cursor.fetchone()
                    i = "+".join(i) if i is not None else "Unknown"

                except mysql.connector.Error as e:
                    print(f"Error: {e}")

                if confidence > 77:
                    if id not in recognized_ids:  # Check if ID is already recognized
                        recognized_ids.add(id)  # Add ID to the set
                        self.mark_attendance(i, r, n, d)  # Mark attendance

                    cv2.putText(img, f"ID: {i}", (x, y - 80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Dep: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

        def recognize(img, clf, faceCascade):
            coord = draw_boundry(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        # Check if face recognizer is available
        try:
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("Classifier.xml")
        except Exception as e:
            print(f"Error loading face recognizer: {e}")
            return

        video_cap = cv2.VideoCapture(0)

        while True:
            ret, img = video_cap.read()
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Welcome to face recognition", img)

            if cv2.waitKey(1) == 13:  # Press Enter to exit
                break

        video_cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()



if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognitions(root)
    root.mainloop()

