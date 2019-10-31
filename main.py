from static import *


# 设定输入为字符串，返回字符串长度，分成八位存在数组中,最后不足的用0填充
def expand_data(data, mode=1):
    length = len(data)
    res = []
    num = int(length / 8)
    mod = length % 8
    for i in range(num):
        res.append(data[i*8: i*8+8])
    # 扩充至8位
    if mod != 0:
        res.append(data[num*8:] + "0" * (8-mod))
    # 最后增加一行，第一个字节为mod值
    if mode==1:
        res.append(str(mod) + "0" * 7)
        print(res)
    return res, length


# 将字符转为字节存在list中
def to_list(c):
    res = [0]*8
    for i in range(8):
        res[7-i] = (ord(c) >> i) & 1
    return res


def to_char(data):
    return chr(data[0]*128+data[1]*64+data[2]*32+data[3]*16+data[4]*8+data[5]*4+data[6]*2+data[7])


def init_string(data):
    s = ""
    for i in range(8):
        s += to_char(data[i*8: i*8+8])
    return s


def xor(list1, list2):
    res = []
    for i in range(len(list1)):
        res.append(list1[i]^list2[i])
    return res


# 生成batch
def init_batch(k="iloveyou"):
    key = []
    for i in range(8):
        key += to_list(k[i])
    return key

# 置换,合并初始值换/子密钥的置换
def swap(data, table):
    # data为数组，内容为1/0
    length = len(table)
    res = [0]*length
    for i in range(length):
        res[i] = data[table[i]-1]
    return res, res[0:int(length/2)], res[int(length/2):]


# 左移
def shift_left(data, num):
    length = len(data)
    res = [0] * length
    for i in range(-num, length-num):
        res[i] = data[i+num]
    return res


# 生成子密钥，输入为密钥
def get_sub_key(key):
    # 变换为56位
    C_D, C, D = swap(key, PC_1)
    sub_key = []
    # 8 轮变换
    for i in range(0, 8):
        C = shift_left(C, shift_count[i])
        D = shift_left(D, shift_count[i])
        k, k_left, k_right = swap(C + D, PC_2)
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


# f函数，输入为rn,kn
def f_func(R, K):
    # 扩展置换
    r, r_l, r_r = swap(R, E)
    # 异或
    r = xor(r, K)
    ans = []
    # s盒置换
    for i in range(8):
        ans += calculate_s(r[i*6: i*6+6], i)
    # p盒置换
    res, res_l, res_r = swap(ans, P_box)
    return res


# data 为64, 默认加密
def encrypt_decrypt(key, data, mode = 1):
    # 初始置换
    res, L, R = swap(data, IP)
    sub_keys = get_sub_key(key)
    if mode == 0:
        sub_keys.reverse()
        for i in range(8):
            new_R = L
            # f函数
            new_L = xor(R, f_func(L, sub_keys[i]))
            L = new_L
            R = new_R
    else:
        for i in range(8):
            new_L = R
            # f函数
            new_R = xor(L, f_func(R, sub_keys[i]))
            L = new_L
            R = new_R
    # 逆置换
    res, l, r = swap(L+R, IP_1)
    return res


# mode 默认为1 即加密
def main_encrypt(file, key, mode=1):
    # 初始化向量为全0
    IV = [0] * 64
    ans = []
    write_data = ""
    with open(file, "r", encoding='utf-8') as f:
        data = f.read()
        # 得到分组64位字节
        group, length= expand_data(data, mode)
        for byte in group:
            text = init_batch(byte)
            if mode == 1:
                text = xor(text, IV)
                res = encrypt_decrypt(key, text,mode)
                IV = res
                print(init_string(IV))
            else:
                res = encrypt_decrypt(key, text, mode)
                print(init_string(IV))
                res = xor(res, IV)
                IV = text

            write_data += init_string(res)
            ans.append(init_string(res))

        print(ans)
        if mode == 0:
            mod = int(write_data[-8])
            if mod == 0:
                write_data = write_data[: -8]
            else:
                write_data = write_data[: -16+mod]
    with open("res1.txt", "w", encoding='utf-8') as f:
        f.write(write_data)






if __name__ == "__main__":
    key = init_batch("iloveyou")
    main_encrypt("res.txt", key, 0)