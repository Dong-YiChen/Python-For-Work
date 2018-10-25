# encoding=utf-8
import paramiko
import time
import multiprocessing
from tkinter import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
import os

login = {'NokiaBSC': ['ip', 22, 'username', 'password'],
         'getFB': ['ip', 22, 'username', 'password']
         }
CmdList = [
    # 'ZUSI:COMP;',
    'ZWQO:CR::;',
    'ZWQD:NAME=FB180930:MAFILE;',
    'Y',
    'N',
    'ZWKS:NAME=FB181024,DIRE=FB181024,MODE=FULL;',
    'ZWQO:CR::;',
    # 'ZAHO;'
]
CmdList_2 = ['./getFB.sh'
             ]
waittime = 0.5
BSCList = ['BSC59-0', 'BSC60-D', 'BSC60-E', 'BSC60-F', 'BSC69-C', 'BSC69-D', 'BSC69-E', 'BSC77-4',
           'BSC77-5', 'BSC82-C', 'BSC82-D', 'BSC82-E', 'BSC82-F', 'BSC83-0', 'BSC83-1', 'BSC83-2',
           'BSC83-3', 'BSC84-C', 'BSC84-D', 'BSC84-E', 'BSC84-F', 'BSC85-B', 'BSC85-C', 'BSC85-D',
           'BSC85-E', 'BSC85-F', 'BSC86-D', 'BSC86-E', 'BSC86-F', 'BSC86-C', 'BSC57-F', 'BSC63-E',
           'BSC63-F', 'BSC72-8', 'BSC72-9', 'BSC74-E', 'BSC74-F', 'BSC75-E', 'BSC75-F', 'BSC87-3',
           'BSC87-4', 'BSC88-E', 'BSC88-F', 'BSC89-D', 'BSC89-E', 'BSC89-F', 'BSC57-E']
BSCList_2 = ['BSC59-0', 'BSC60-D', 'BSC60-E', 'BSC60-F', 'BSC69-C', 'BSC69-D', 'BSC69-E', 'BSC77-4',
             'BSC77-5', 'BSC82-C', 'BSC82-D', 'BSC82-E', 'BSC82-F', 'BSC83-0', 'BSC83-1', 'BSC83-2',
             'BSC83-3', 'BSC84-C', 'BSC84-D', 'BSC84-E', 'BSC84-F', 'BSC85-B', 'BSC85-C', 'BSC85-D',
             'BSC85-E', 'BSC85-F', 'BSC86-D', 'BSC86-E', 'BSC86-F', 'BSC86-C', 'BSC57-F', 'BSC63-E',
             'BSC63-F', 'BSC72-8', 'BSC72-9', 'BSC74-E', 'BSC74-F', 'BSC75-E', 'BSC75-F', 'BSC87-3',
             'BSC87-4', 'BSC88-E', 'BSC88-F', 'BSC89-D', 'BSC89-E', 'BSC89-F', 'BSC57-E']

# BSCList = ['BSC77-4']
# BSCList_2 = ['BSC0', 'BSC1', 'BSC2', 'BSC3', 'BSC4', 'BSC5']

CommonRecv = b'< \x08 '
CommonRecv_Check = b'CONFIRM COMMAND EXECUTION: Y/N ? \x08 \n'
CommonRecv_2 = b'[wangyinh@shcs1 ~]$ '
alarm = ''


def sendcmd(com, rec, ssh_shell, outputfile):
    ssh_shell.sendall(com + '\r\n')
    time.sleep(waittime)
    while True:
        line = ssh_shell.recv(4096)
        if line and line.endswith(rec):
            break
        elif line and line.endswith(CommonRecv_Check):
            break
        else:
            t.insert('end', line.decode())
            t.see(END)
            t.update()
            print(line.decode(), end="", file=outputfile)
    t.insert('end', line.decode())
    t.see(END)
    t.update()
    print(line.decode(), file=outputfile)


def bsccmd(CmdList, BSCList):
    global t
    cmd = Tk()
    cmd.title('自动备份程序回显')
    cmd.geometry('800x500')
    t = Text(cmd, height=40, bg='white')
    scroll = Scrollbar(cmd, orient=VERTICAL)
    scroll.config(command=t.yview)
    scroll.pack(fill=Y, expand=0, side=RIGHT, anchor=N)
    t.pack(fill=X)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # connect to client
    client.connect(hostname=login.get('NokiaBSC')[0],
                   port=22,
                   username=login.get('NokiaBSC')[2],
                   password=login.get('NokiaBSC')[3]
                   )
    # get shell
    ssh_shell = client.invoke_shell()
    # ready when line endswith '>' or other character
    while True:
        start = ssh_shell.recv(1024)
        if start and start.endswith(b'>'):
            break
    for bsc in BSCList:
        outputfile = open(sys.path[0] + '\\BSC备份log\\' + bsc + '.txt', 'w')
        sendcmd(bsc, b'ENTER USERNAME < \x08 ', ssh_shell, outputfile)
        sendcmd('BSCusername', b'ENTER PASSWORD < \x08 ', ssh_shell, outputfile)
        sendcmd('BSCpassword', CommonRecv, ssh_shell, outputfile)
        for cmd in CmdList:
            sendcmd(cmd, CommonRecv, ssh_shell, outputfile)
        # sendcmd('ZWQO:CR::;', CommonRecv)
        # sendcmd('ZUSI:COMP;', CommonRecv)
        # if line.find('SP-EX'):
        #     alarm += bsc + '\n'
        # sendcmd('ZAHO;', CommonRecv)
        sendcmd('ZZZ;', b'>', ssh_shell, outputfile)
        outputfile.close()
    # print(alarm)
    showinfo(title='Finish', message='BSC备份完成')
    cmd.mainloop()
    ssh_shell.close()
    client.close()


def getfb(para):
    global t
    cmd_2 = Tk()
    cmd_2.title('自动备份程序回显')
    cmd_2.geometry('800x500')
    t = Text(cmd_2, height=40, bg='white')
    scroll = Scrollbar(cmd_2, orient=VERTICAL)
    scroll.config(command=t.yview)
    scroll.pack(fill=Y, expand=0, side=RIGHT, anchor=N)
    t.pack(fill=X)
    CmdList = para[1]
    bsc = para[0]
    outputfile = open(sys.path[0] + '\\备份包导出log\\' + bsc + '.txt', 'w')
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # connect to client
    client.connect(hostname=login.get('getFB')[0],
                   port=22,
                   username=login.get('getFB')[2],
                   password=login.get('getFB')[3]
                   )
    # get shell
    ssh_shell = client.invoke_shell()
    # ready when line endswith '>' or other character
    while True:
        start = ssh_shell.recv(1024)
        if start and start.endswith(CommonRecv_2):
            break
    for cmd in CmdList:
        sendcmd(cmd + ' ' + bsc, CommonRecv_2, ssh_shell, outputfile)
    # print(alarm)
    outputfile.close()
    cmd_2.destroy()
    cmd_2.mainloop()
    ssh_shell.close()
    client.close()


def bsccmd_start():
    if askyesno(title='Are You Sure?', message='确认开始执行BSC备份吗？'):
        print('开始BSC备份')
        isExists = os.path.exists(sys.path[0] + '\\BSC备份log')
        if not isExists:
            os.makedirs(sys.path[0] + '\\BSC备份log')
        bsccmd(CmdList, BSCList)
        print('BSC备份完成')


def getfb_start():
    if askyesno(title='Are You Sure?', message='确认开始执行备份包导出吗？'):
        print('开始备份包导出')
        isExists = os.path.exists(sys.path[0] + '\\备份包导出log')
        if not isExists:
            os.makedirs(sys.path[0] + '\\备份包导出log')
        the_list = [(bsc, CmdList_2) for bsc in BSCList_2]
        p = multiprocessing.Pool(6)
        p.map(getfb, the_list)
        print('备份包导出完成')
        showinfo(title='Finish', message='备份包导出完成')


if __name__ == '__main__':
    # global t
    root = Tk()
    root.title('诺基亚BSC自动备份程序')
    root.geometry('500x200')
    fm1 = Frame(root, bg='pink')
    fm2 = Frame(root, bg='pink')
    cv = Canvas(root, width=500, height=100, bg='pink', bd=0)
    cv.pack()
    fname = sys.path[0] + '\\Title.JPG'
    img = Image.open(fname)
    img = ImageTk.PhotoImage(img)
    cv.create_image(12, 25, anchor=NW, image=img)
    # t = Text(root, height=20, bg='white')
    # t.pack(fill=X)
    Button(fm1, text='执行BSC备份', command=bsccmd_start, width=15, height=2).pack(pady=25)
    Button(fm2, text='执行备份包导出', command=getfb_start, width=15, height=2).pack(pady=25)
    fm1.pack(side=LEFT, fill=X, expand=YES)
    fm2.pack(side=LEFT, fill=X, expand=YES)
    root.mainloop()
