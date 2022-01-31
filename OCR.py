import cv2
import pytesseract
from tkinter import *
import tkinter
from tkinter import filedialog
from PIL import ImageTk, Image
import os
from datetime import datetime
from textblob import TextBlob

pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)//Tesseract-OCR//tesseract.exe'
curr_datetime = datetime.now().strftime('_%Y-%m-%d-%H-%M-%S')
temp_directory = "temp/"
file_name = "OCR'ed_"



def corrected_text(file):
    one = TextBlob(file)
    return str(one.correct())


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def fn(saved_at):
    file_name = os.path.basename(image_file)
    splitted_path = os.path.splitext(file_name)
    modified_picture_path = saved_at + splitted_path[0] + curr_datetime + splitted_path[1]
    final_temp_path = temp_directory + modified_picture_path
    return final_temp_path


ui = tkinter.Tk()
ui.title('TEXT RECOGNITION')
ui.geometry('720x640+0+0')
ui.configure(bg='#8D3DAF')

image_file = filedialog.askopenfilename(initialdir="/Images",
                                        title="select a file",
                                        filetypes=(("png files", "*.jpg"), ("all file", "*.*")))


og_image_label = Label(ui, text="Original Image", bg='black', fg='white',
                       font=("Courier New", 14)).place(x=50, y=125)
text_gen_label = Label(ui, text="Text Generated", bg='black', fg='white',
                       font=("Terminal", 16)).place(x=250, y=330)

img = cv2.imread(image_file)
gray = get_grayscale(img)
thresh = thresholding(gray)
ima = Image.open(image_file)
resized = ima.thumbnail((480, 360))
resized = ima.save(fn(file_name))
image = Image.open(fn(file_name))
photo = ImageTk.PhotoImage(image)
og_image = Label(ui, image=photo)
og_image.place(x=240, y=10)

file_rn = fn(file_name)
txt = pytesseract.image_to_string(file_rn)
text_rn = corrected_text(txt)
res = " ".join(text_rn.split())

text_gen_ = Label(ui, text=res, bg='#f1c40f', fg='#0D0D0D',
                  font=('MS Serif', 14), width=60, height=8).place(x=20, y=365)

txt_filename = fn(file_name)+'.txt'
fs = f"Text Generated File Saved at and as:\n {txt_filename}"
file_saved_label = Label(ui, text=fs, bg='#3498db', fg='white',
                         font=("Arial", 12)).place(x=125, y=580)

f = open(txt_filename, 'w+')
f.write(res)
f.write('\n')
f.close()

ui.mainloop()