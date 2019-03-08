'''
Chatroom
env: python3.5
exc: socket and fork
'''
from socket import *
import os, sys

# 用于存储用户{name:addr}
user = {}

#处理登入
def do_login(s, name, addr):
    if (name in user) or name == '管理员消息':
        s.sendto('该用户已存在'.encode(),addr)
        return
    s.sendto(b'OK',addr)

    #通知其他人
    msg = "欢迎 %s 进入聊天" %name
    for i in user:
        s.sendto(msg.encode(), user[i])
    
    #将用户加入user
    user[name] = addr

def do_chat(s,name,text):
    msg = "%s : %s"%(name, text)

    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])

def do_quit(s, name):
    msg = '%s退出了聊天室'%name
    print(msg)
    print(user)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])
        else:
            
            s.sendto(b'EXIT', user[i])
            print(i)

    # 将用户删除
    del user[name]


def do_requersts(s):
    while True:
        data,addr = s.recvfrom(1024)
        
        msgList = data.decode().split(' ')
        print(msgList)
        
        #区分请求类型        
        if msgList[0] == 'L':
            do_login(s,msgList[1],addr)

        elif msgList[0] == 'C':
            #重新组织消息内容
            text = ' '.join(msgList[2:])
            do_chat(s,msgList[1],text)

        elif msgList[0] == 'Q':
            print(msgList[1])
            do_quit(s, msgList[1])

#创建网络连接
def main():
    ADDR = ('0.0.0.0',6666)
    # 创建套接字
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)

    #创建单独进程用于发送管理员消息
    pid = os.fork()
    if pid < 0:
        print('Error')
        return 
    if pid == 0:
        while True:
            msg = input('管理员消息:')
            msg = 'C 管理员消息 '+msg
            s.sendto(msg.encode(), ADDR)  
    else:
        # 处理各种客户端请求
        do_requersts(s)


if __name__ == '__main__':
    main()