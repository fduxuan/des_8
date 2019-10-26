from static import *


# 置换,合并初始值换/子密钥的置换
def swap(data, table):
    # data为数组，内容为1/0
    length = len(data)
    res = [0]*length
    for i in range(length):
        res[i] = data[table[i]-1]
    return res[0:int(length/2)], res[int(length/2):]


# 左移
def shift(data, num):
    length = len(data)
    res = [0] * length
    for i in range(-num, length-num):
        res[i] = data[i+num]
    return res


# 生成子密钥，输入为密钥
def get_sub_key(key):
    # 变换为56位
    C, D = swap(key, PC_1)
    sub_key = []
    # 8 轮变换
    for i in range(0, 8):
        C = shift(C, shift_count(i))
        D = shift(D, shift_count(i))
        k_left, k_right = swap(C + D)
        sub_key.append(k_left+k_right)
    return sub_key


# 计算S盒步骤，输入为data和第几个盒
def calculate_s(data, num):
    row = data[0]*2 + data[5]
    col = data[1]*8 + data[2]*4 + data[3]*2 + data[4]
    res = S_box[num][row][col]
    ans = [0, 0, 0, 0]
    # 得到二进制
    for i in range(4):
        ans[3-i] = (res >> i) & 1
    return ans


# f函数
def f_func():
    print("ttt")


if __name__ == "__main__":
      print(swap([1,2,3,4],[4,2,3,1]))