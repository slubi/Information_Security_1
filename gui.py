import tkinter as tk
import s_des
import binascii
from tkinter import *
from tkinter import messagebox
import time

# 暴力破解函数
def password(password_length=10):
    start = time.time()
    p = entry1.get()
    c = entry3.get()
    for i in range(1024):
        binary_i = bin(i)[2:]
        if len(binary_i)<10:
            binary_i=binary_i.zfill(10)
        key = binary_i
        k1, k2 = s_des.generate_key(key, s_des.p10_table, s_des.p8_table)
        ciphertext = s_des.encrypt(p, k1, k2)
        if ciphertext == c:
            print(key)
            break
    entry2.delete(0, END)
    entry2.icursor(0)
    entry2.insert(0, str(key))
    end = time.time()
    messagebox.askyesno('成功破解', '密钥为： ' + str(key)+' 耗时为' + str(end - start)+'s')

# 加密函数
def button_callback(e):
    p = entry1.get()
    key = entry2.get()
    # 生成子密钥 K1 和 K2
    k1, k2 = s_des.generate_key(key, s_des.p10_table, s_des.p8_table)
    # 对明文进行加密
    ciphertext = s_des.encrypt(p, k1, k2)
    # 对密文进行解密
    plaintext = s_des.decrypt(ciphertext, k1, k2)
    entry3.delete(0, END)
    entry3.icursor(0)
    entry3.insert(0, str(ciphertext))
    messagebox.askyesno('成功加密', '密文为： ' + str(ciphertext))

# 解密函数
def button_back(e):
    p = entry3.get()
    key = entry2.get()
    # 生成子密钥 K1 和 K2
    k1, k2 = s_des.generate_key(key, s_des.p10_table, s_des.p8_table)
    # 对明文进行加密
    # 对密文进行解密
    plaintext = s_des.decrypt(p, k1, k2)
    entry1.delete(0, END)
    entry1.icursor(0)
    entry1.insert(0, str(plaintext))
    messagebox.askyesno('成功解密', '解密明文为： ' + str(plaintext))

# 字符模式函数
def button_ascll(e):
    p = entry1.get()
    key = entry2.get()
    # 生成子密钥 K1 和 K2
    k1, k2 = s_des.generate_key(key, s_des.p10_table, s_des.p8_table)

    text = p
    b_text = text.encode('utf-8')
    list_b_text = list(b_text)
    re = []
    for num in list_b_text:
        re.append(bin(num)[2:].zfill(8))
    ciphertext = ""
    for i in range(len(re)):
        temp = re[i]
        var2 = s_des.encrypt(temp, k1, k2)
        var2 = int(var2, 2)
        char = chr(var2)
        ciphertext += char
    entry3.delete(0, END)
    entry3.icursor(0)
    entry3.insert(0, ciphertext)
    messagebox.askyesno('成功加密', '密文为： ' + str(ciphertext))

def button_ascllb(e):
    p = entry3.get()
    key = entry2.get()
    # 生成子密钥 K1 和 K2
    k1, k2 = s_des.generate_key(key, s_des.p10_table, s_des.p8_table)

    text = p
    b_text = text.encode()
    list_b_text = list(b_text)
    re = []
    for num in list_b_text:
        re.append(bin(num)[2:].zfill(8))
    result = ""
    for i in range(len(re)):
        temp = re[i]
        var2 = s_des.decrypt(temp, k1, k2)
        var2 = int(var2, 2)
        char = chr(var2)
        result += char
    entry1.delete(0, END)
    entry1.icursor(0)
    entry1.insert(0, result)
    messagebox.askyesno('成功解密', '明文为： ' + str(result))

# 创建主窗口
root = tk.Tk()
root.title('S-DES')
root.geometry("450x300+600+280")  # (宽度x高度)+(x轴+y轴)
# 标签
label1 = tk.Label(root, text='明文:', width=10, height=2, font=25)# 明文
label2 = tk.Label(root, text='密钥:', width=10, height=2, font=25)# 密钥
label3 = tk.Label(root, text='密文:', width=10, height=2, font=25)# 密文
label1.place(x=90, y=40)
label2.place(x=90, y=80)
label3.place(x=90, y=120)

# 文本框
entry1 = tk.Entry(root)# 明文框
entry2 = tk.Entry(root)# 密钥框
entry1.place(x=190, y=53)
entry2.place(x=190, y=93)

entry3 = tk.Entry(root)# 密文框
entry3.place(x=190, y=133)

# 按钮
# 加密按钮
btn1 = tk.Button(root,width=5, height=1, bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn1["text"] = "计算"
btn1.place(x=100, y=168)  # 按钮在窗口里面的定位
btn1.bind("<Button-1>", button_callback)
# 解密按钮
btn2 = tk.Button(root,width=5, height=1,  bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn2["text"] = "解密"
btn2.place(x=150, y=168)  # 按钮在窗口里面的定位
btn2.bind("<Button-1>", button_back)
# Ascll按钮
btn3 = tk.Button(root,width=7, height=1,  bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn3["text"] = "Ascll字符"
btn3.place(x=200, y=168)  # 按钮在窗口里面的定位
btn3.bind("<Button-1>", button_ascll)
# Ascll解密按钮
btn5 = tk.Button(root,width=7, height=1,  bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn5["text"] = "A-解密"
btn5.place(x=265, y=168)  # 按钮在窗口里面的定位
btn5.bind("<Button-1>", button_ascllb)
# 破解按钮
btn4 = tk.Button(root,width=5, height=1,  bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn4["text"] = "破解"
btn4.place(x=330, y=168)  # 按钮在窗口里面的定位
btn4.bind("<Button-1>", password)

root.mainloop()