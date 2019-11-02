from tkinter import *
from main import *
from tkinter import filedialog

res_string = ""
input = ""


def open_file(text_input):
    text_input.delete('1.0', END)
    print("button is press")
    filename = filedialog.askopenfilename()
    if filename:
        with open(filename, "r", encoding='utf-8') as f:
            global input
            data=f.read()
            input = data
            text_input.insert("insert", "已导入！")


def save_file(text_output):
    filename = filedialog.asksaveasfilename(filetypes=[("TXT", ".txt")])
    if filename:
        with open(filename, "w", encoding='utf-8') as f:
            f.write(res_string)


def handle(text,text_input, text_output, mode):
    text_output.delete('1.0', END)
    key = text.get()
    if len(key) != 8:
        text_output.insert("insert", "您必须输入八位密钥！")
    else:
        t = text_input.get('1.0', END)
        if t != "已导入！\n":
            data = t
        else:
            data = input
        print(data)
        while data[-1] == '\n':
            data = data[:-1]
        if len(data)==0:
            text_output.insert("insert", "输入为空！")
        global res_string
        res_string, res_bit= main_encrypt(data, key, mode)
        for i in res_bit:
            text_output.insert("insert", i)



def main():
    root = Tk()  # create a rootwindow
    root.title("8轮des算法 by fduxuan")
    root.geometry("600x400")
    L1 = Label(text="请输入8位字符作为密钥:")
    L2 = Label(text="输入:")
    L3 = Label(text="输出:")
    text_input = Text(root, height=10, width=50,bd=5, bg="#E6EDFF")
    text_output = Text(root, height=10, width=50,bd=5, bg="#E6EDFF")
    text = Entry(root, fg = "black", show='*')
    button1 = Button(root, text="导入输入文件", fg="black", command=(lambda:open_file(text_input)))
    button2 = Button(root, text="保存输出文件", fg="black", command=(lambda:save_file(text_output)))
    button3 = Button(root, text="加密",  command=(lambda:handle(text, text_input, text_output,1)), bg="#ACB4E6")
    button4 = Button(root, text="解密",  command=(lambda:handle(text, text_input, text_output,0)), bg="#EAD0FA")

    text_input.place(x=220, y=40)
    text_output.place(x=220, y=230)
    button1.place(x=20, y=20)
    text.place(x=20, y=120)
    L1.place(x=20, y=100)
    L2.place(x=220, y=20)
    L3.place(x=220, y=210)
    button2.place(x=20,y=50)
    button3.place(x=20, y=230)
    button4.place(x=100, y=230)
    root.mainloop()  # create an eventloop








if __name__ == "__main__":
    main()