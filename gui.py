from tkinter import *
from main import *
from tkinter import filedialog
from rsa import *

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


def handle(text,text_input, text_output, text_n, text_d,text_key, mode):
    text_output.delete('1.0', END)
    key = text.get()
    n = text_n.get()
    d = text_d.get()
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
        res_string = ""
        if mode == 0 :
            # 如果是解密需要rsa私钥
            if len(n) == 0 or len(d) == 0:
                text_output.insert("insert", "解密请输入私钥！")
                return
            new_data = ""
            data = data.split()
            for i in data:
                x = decrypt(int(i), (int(n), int(d)))
                new_data += chr(x)
            data = new_data
            res_string_1, res_bit= main_encrypt(data, key, mode)
            for i in res_string_1:
                res_string += i
                text_output.insert("insert", i)
        if mode == 1:
            res_string_1, res_bit = main_encrypt(data, key, mode)
            while 1:
                p = get_prime()
                q = get_prime()
                '''生成公钥私钥'''
                pubkey, selfkey = gen_key(p, q)
                if selfkey[1] > 0:
                    break
            text_key.delete('1.0', END)
            text_n.delete('0',END)
            text_d.delete('0',END)
            text_n.insert("insert", selfkey[0])
            text_d.insert('insert', selfkey[1])
            text_key.insert("insert", "公钥: n: " + str(pubkey[0]) + " e: " + str(pubkey[1]) + "\n" +
                                      "私钥: n: " + str(selfkey[0]) + " d: " + str(selfkey[1]) + "\n" )
            for i in res_string_1:
                c = encrypt(ord(i), pubkey)
                res_string += str(c)+"\n"
                text_output.insert("insert", str(c)+" ")

        # for i in res_bit:
        #     text_output.insert("insert", i)



def main():
    root = Tk()  # create a rootwindow
    root.title("8轮des算法 by fduxuan")
    root.geometry("600x400")
    L1 = Label(text="请输入8位字符作为des密钥:")
    L2 = Label(text="输入:")
    L3 = Label(text="输出:")
    L4 = Label(text="请输入rsa秘钥:")
    L5 = Label(text="n:")
    L6 = Label(text="d:")
    L7 = Label(text="rsa密钥请牢记:")

    text_input = Text(root, height=10, width=50,bd=5, bg="#E6EDFF")
    text_output = Text(root, height=10, width=50,bd=5, bg="#E6EDFF")
    text_key = Text(root, height=3, width=25, bg="#E6EDFF")
    text = Entry(root, fg = "black", show='*')
    text_n = Entry(root, fg = "black")
    text_d = Entry(root, fg = "black")

    button1 = Button(root, text="导入输入文件", fg="black", command=(lambda:open_file(text_input)))
    button2 = Button(root, text="保存输出文件", fg="black", command=(lambda:save_file(text_output)))
    button3 = Button(root, text="加密",  command=(lambda:handle(text, text_input, text_output,text_n, text_d,text_key,1)), bg="#ACB4E6")
    button4 = Button(root, text="解密",  command=(lambda:handle(text, text_input, text_output,text_n, text_d,text_key, 0)), bg="#EAD0FA")

    text_input.place(x=220, y=40)
    text_output.place(x=220, y=230)
    text_key.place(x=20,y=340)
    button1.place(x=20, y=20)
    text.place(x=20, y=120)
    text_n.place(x=20, y=170)
    text_d.place(x=20,y=200)
    L1.place(x=20, y=100)
    L2.place(x=220, y=20)
    L3.place(x=220, y=210)
    L4.place(x=20, y=150)
    L5.place(x=5, y=170)
    L6.place(x=5, y=200)
    L7.place(x=20, y=310)
    button2.place(x=20,y=50)
    button3.place(x=20, y=260)
    button4.place(x=100, y=260)
    root.mainloop()  # create an eventloop








if __name__ == "__main__":
    main()