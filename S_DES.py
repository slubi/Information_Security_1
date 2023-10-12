class My_S_DES():
    def __init__(self,key) -> None:
        #初始化算法中用到的常量
        self.p10_table=(3,5,2,7,4,10,1,9,8,6)
        self.p8_table=(6,3,7,4,8,5,10,9)
        self.p4_table=(2,4,3,1)
        self.ip_table=(2,6,3,1,4,8,5,7)
        self.ep_table=(4,1,2,3,2,3,4,1)
        self.ip_inv_table=(4,1,3,5,7,2,8,6)
        self.s_box_0=[
            [1,0,3,2],
            [3,2,1,0],
            [0,2,1,3],
            [3,1,0,2]
        ]

        self.s_box_1=[
            [0,1,2,3],
            [2,3,1,0],
            [3,0,1,2],
            [2,1,0,3]
        ]
        self.generate_key(key)
    def permute(self,input_str,table):#通用的置换函数
        output_str=""
        for bit_position in table:
            output_str+=input_str[bit_position-1]
        return output_str
    def ls(self,key,n):
        # 将密钥分成两段并循环左移 n 位
        left_half=key[:5]
        right_half=key[5:]
        shifted_left=left_half[n:] + left_half[:n]
        shifted_right=right_half[n:] + right_half[:n]
        return shifted_left + shifted_right
    def generate_key(self,k):
        # 执行 P10 置换
        p10_key=self.permute(k,self.p10_table)
        # 对结果进行左移操作和P8置换，得到 K1
        self.k1=self.permute(self.ls(p10_key,1),self.p8_table)
        # 再次对上一步结果进行左移操作h和P8置换，得到 K2
        self.k2=self.permute(self.ls(self.ls(p10_key,1),2),self.p8_table)
    def F(self,right_half,k):
        # 对右半部分进行 E/P 扩展置换
        expanded=self.permute(right_half,self.ep_table)
        # 对结果与 K1 进行异或操作
        xored='{0:08b}'.format(int(expanded,2) ^ int(k,2))
        # 将结果分为两组，并根据 S-box 进行替换
        s0_input=xored[:4]
        s1_input=xored[4:]
        # 根据S盒规则行列查找
        s0_row=int(s0_input[0] + s0_input[-1],2)
        s0_col=int(s0_input[1:-1],2)
        s1_row=int(s1_input[0] + s1_input[-1],2)
        s1_col=int(s1_input[1:-1],2)
        s0_output='{0:02b}'.format(self.s_box_0[s0_row][s0_col])
        s1_output='{0:02b}'.format(self.s_box_1[s1_row][s1_col])
        # 对两个输出串进行 P4 置换得到最终结果
        s_output=s0_output + s1_output
        return self.permute(s_output,self.p4_table)
    def encrypt(self,p:str):#加密函数
        # 执行初始置换
        p=self.permute(p,self.ip_table)
        # 进行两轮 Feistel 加密
        l0=p[:4]
        r0=p[4:]
        l1=r0
        # 第一轮的P4
        f_result=self.F(r0,self.k1)
        # p41和L0异或
        r1='{0:04b}'.format(int(l0,2) ^ int(f_result,2))
        # 第二轮的P4
        f_result=self.F(r1,self.k2)
        # p42和L1异或
        r2='{0:04b}'.format(int(l1,2) ^ int(f_result,2))
        # 逆置换并返回结果(左边R2右边R1)
        return self.permute(r2 + r1,self.ip_inv_table)
    def decrypt(self,c:str):#解密函数
        # 执行初始置换
        c=self.permute(c,self.ip_table)
        # 进行两轮 Feistel 解密（注意子密钥的使用顺序）
        r2=c[:4]
        l2=c[4:]
        # 第一轮的P4
        f_result=self.F(l2,self.k2)
        # p41和R2异或
        l1='{0:04b}'.format(int(r2,2) ^ int(f_result,2))
        # 第二轮的P4
        f_result=self.F(l1,self.k1)
        # p42和R1异或
        r1='{0:04b}'.format(int(l2,2) ^ int(f_result,2))
        # 逆置换并返回明文
        return self.permute(r1 + l1,self.ip_inv_table)
if __name__=="__main__":
    test=My_S_DES("1010000010")
    a=test.encrypt("11000101")
    print(a)
    print(test.decrypt(a))
