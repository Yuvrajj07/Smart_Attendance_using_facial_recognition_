from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np


class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")



        title_lbl = Label(self.root, text="Train Data Set",
                          font=("times new roman", 35, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=0, width=1530, height=45)



        img_top = Image.open(r"college_images\facialrecognition.png")
        img_top = img_top.resize((1530, 325), Image.LANCZOS)  # Note: Image.Resampling.LANCZOS may change to Image.LANCZOS based on PIL version
        self.photoimg_top = ImageTk.PhotoImage(img_top)  # Use a different variable for the top image

        # Create the label for the top image and place it
        f_lbl_top = Label(self.root, image=self.photoimg_top)
        f_lbl_top.place(x=0, y=55, width=1530, height=325)

        b1_1 = Button(self.root, text="Train Data",command=self.train_classifier, cursor="hand2",
                      font=("times new roman", 30, "bold"), bg="darkblue", fg="white")
        b1_1.place(x=0, y=380, width=1530, height=60)

        # Load and resize the bottom image
        img_bottom = Image.open(r"college_images\Photos.jpg")
        img_bottom = img_bottom.resize((1530, 325), Image.LANCZOS)  # Ensure we resize img_bottom instead of img_top
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)  # Use a different variable for the bottom image

        # Create the label for the bottom image and place it
        f_lbl_bottom = Label(self.root, image=self.photoimg_bottom)
        f_lbl_bottom.place(x=0, y=440, width=1530, height=325)
    def train_classifier(self):
        data_dir=("data")
        path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)]

        faces=[]
        ids=[]

        for image in path:
            img=Image.open(image).convert('L')   #Gray Scale Image
            imageNp=np.array(img,'uint8')
            id=int(os.path.split(image)[1].split('.')[1]) 

            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training",imageNp)
            cv2.waitKey(1)==13
        ids=np.array(ids)



        # ======================Train The Classifier===============

        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)
        clf.write("Classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result","Training data set completed!!!!")




                         


        










if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()