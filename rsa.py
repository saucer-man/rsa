# coding:utf-8
#
import random
import time 
import math


def pow_mod(p, q, n):
    '''
    幂模运算，快速计算(p^q) mod (n)
    这里采用了蒙哥马利算法
    '''
    res = 1
    while q :
        if q & 1:
            res = (res * p) % n
        q >>= 1
        p = (p * p) % n
    return res

def gcd(a,b):
    '''
    欧几里得算法求最大公约数
    '''
    while a!=0:
        a, b =b%a , a
    return b

def mod_1(x, n):
    '''
    扩展欧几里得算法求模逆
    取模负1的算法:计算x2= x^-1 (mod n)的值
    '''
    x0 = x
    y0 = n
    x1 = 0
    y1 = 1
    x2 = 1
    y2 = 0
    while n != 0:
            q = x // n
            (x, n) = (n, x % n)
            (x1, x2) = ((x2 - (q * x1)), x1)
            (y1, y2) = ((y2 - (q * y1)), y1)
    if x2 < 0:
            x2 += y0
    if y2 < 0:
            y2 += x0
    return x2

def probin(w):
    '''
    随机产生一个伪素数，产生 w表示希望产生位数
    '''
    list = []
    list.append('1')  #最高位定为1
    for i in range(w - 2):
        c = random.choice(['0', '1'])
        list.append(c)
    list.append('1') # 最低位定为1
    # print(list)
    res = int(''.join(list),2)
    return res


def prime_miller_rabin(a, n): # 检测n是否为素数
    '''
    第一步，模100以内的素数，初步排除很显然的合数
    '''
    Sushubiao=(2,3,5,7,11,13,17,19,23,29,31,37,41
                ,43,47,53,59,61,67,71,73,79,83,89,97)# 100以内的素数，初步排除很显然的合数
    for y in Sushubiao:
        if n%y==0:
            #print("第一步就排除了%d                 %d"%(n,y))
            return False
    #print('成功通过100以内的素数')

    '''
    第二步 用miller_rabin算法对n进行检测
    '''
    if pow_mod(a, n-1, n) == 1: # 如果a^(n-1)!= 1 mod n, 说明为合数
        d = n-1 # d=2^q*m, 求q和m
        q = 0
        while not(d & 1): # 末尾是0
            q = q+1
            d >>= 1
        m = d

        # if pow_mod(a, m, n) == 1:
        #     # 满足条件
        #     return True
        
    #     for i in range(q+1): # 0~q 
    #         u = m * (2**i)  # u = 2^i*m
    #         if pow_mod(a, u, n) == n-1:
    #             # 满足条件 这里为什么 2^q * m == n-1也满足条件？？？？？
    #             return True
    #     return False  
    # else:
    #     return False
        for i in range(q): # 0~q-1, 我们先找到的最小的a^u，再逐步扩大到a^((n-1)/2)
            u = m * (2**i)  # u = 2^i * m
            tmp = pow_mod(a, u, n)
            if tmp == 1 or tmp == n-1:
                # 满足条件 
                return True
        return False
    else:
        return False


def prime_test(n, k):
    while k > 0:
        a = random.randint(2, n-1)
        if not prime_miller_rabin(a, n):
            return False
        k = k - 1
    return True

# 产生一个大素数(bit位)
def get_prime(bit):
    while True:
        prime_number = probin(512)
        # prime_number = 12053183412038934244199647849825520631926841159909870489683772445800307815934262271616287581789478437690748874723873375535588732777117648057138401098671371
        # print('生成的数字是%d\n'%prime_number)
        for i in range(50):  # 伪素数附近50个奇数都没有真素数的话，重新再产生一个伪素数
            u = prime_test(prime_number, 5)
            if u:
                break
            else:
                prime_number = prime_number + 2*(i)
        if u:
            return prime_number
        else:
            continue

if __name__=='__main__':
    p = get_prime(500) # 密钥p
    q = get_prime(550) # 密钥q
    n = p * q   # 公开n
    OrLa = (p-1)*(q-1)  # 欧拉函数
    
    while True: # 取一个合适的e，这里的e要和OrLa互素才行
        e = 65537
        if gcd(e, OrLa) == 1:
            break
        else:
            e = e-1

    d = mod_1(e, OrLa)

    print('私钥p,q,d分别为:\n')
    print('p: %d\n' % p)
    print('q: %d\n' % q)
    print('d: %d\n\n' % d)

    print('公钥n,e分别为:\n')
    print('n: %d\n' % n)
    print('e: %d\n\n' % e)


    M = int(input("请输入待加密的明文："))

    C = pow_mod(M, e, n) # 加密
    print('\n加密完成，得到的密文：\n%d\n'%C)

    M = pow_mod(C, d, n) # 解密
    print('解密完成，得到的明文为：\n%d\n'%M)






