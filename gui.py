from tkinter import *
import tkinter
from main import *
from tkinter import filedialog

def pressOk():
    print("button is press")
    filename = filedialog.askopenfilename()
    main_encrypt(filename, init_batch("iloveyou"))

def main():
    root = Tk()  # create a rootwindow
    root.title("8轮des算法 by fduxuan")
    root.geometry("600x400")

    button1 = Button(root, text="打开", fg="black", command=pressOk)
    button1.pack()

    root.mainloop()  # create an eventloop








if __name__ == "__main__":
    main()