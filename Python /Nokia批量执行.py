# encoding=utf-8
import paramiko
import time
import multiprocessing
from tkinter import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
import os

login = {'NokiaBSC': ['ip', 22, 'username', 'password']}
CmdList = []
waittime = 0.5
BSCList = ['BSC59-0', 'BSC60-D', 'BSC60-E', 'BSC60-F', 'BSC69-C', 'BSC69-D', 'BSC69-E', 'BSC77-4',
           'BSC77-5', 'BSC82-C', 'BSC82-D', 'BSC82-E', 'BSC82-F', 'BSC83-0', 'BSC83-1', 'BSC83-2',
           'BSC83-3', 'BSC84-C', 'BSC84-D', 'BSC84-E', 'BSC84-F', 'BSC85-B', 'BSC85-C', 'BSC85-D',
           'BSC85-E', 'BSC85-F', 'BSC86-D', 'BSC86-E', 'BSC86-F', 'BSC86-C', 'BSC57-F', 'BSC63-E',
           'BSC63-F', 'BSC72-8', 'BSC72-9', 'BSC74-E', 'BSC74-F', 'BSC75-E', 'BSC75-F', 'BSC87-3',
           'BSC87-4', 'BSC88-E', 'BSC88-F', 'BSC89-D', 'BSC89-E', 'BSC89-F', 'BSC57-E']

# BSCList = ['BSC59-0', 'BSC60-D']

CommonRecv = b'< \x08 '
CommonRecv_Check = b'CONFIRM COMMAND EXECUTION: Y/N ? \x08 \n'
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
        elif line and line.endswith(b'>'):
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
    for c in inp.get("0.0", "end").split('\n'):
        CmdList.append(c)
    # print(CmdList)
    if CmdList == ['', '']:
        showinfo(title='Error', message='没有输入BSC指令')
    else:
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
        client.connect(hostname=login.get('NokiaBSC')[0],
                       port=22,
                       username=login.get('NokiaBSC')[2],
                       password=login.get('NokiaBSC')[3]
                       )
        ssh_shell = client.invoke_shell()
        while True:
            start = ssh_shell.recv(1024)
            if start and start.endswith(b'>'):
                break
        for bsc in BSCList:
            outputfile = open(sys.path[0] + '\\BSC批量执行log\\' + bsc + '.txt', 'w')
            sendcmd(bsc, b'ENTER USERNAME < \x08 ', ssh_shell, outputfile)
            sendcmd('BSCusername', b'ENTER PASSWORD < \x08 ', ssh_shell, outputfile)
            sendcmd('BSCpassword', CommonRecv, ssh_shell, outputfile)
            for cmd in CmdList:
                sendcmd(cmd, CommonRecv, ssh_shell, outputfile)
            # sendcmd('ZUSI:COMP;', CommonRecv)
            # if line.find('SP-EX'):
            #     alarm += bsc + '\n'
            # sendcmd('ZAHO;', CommonRecv)
            sendcmd('ZZZ;', b'>', ssh_shell, outputfile)
            outputfile.close()
        # print(alarm)
        filedir = sys.path[0] + '\\BSC批量执行log'
        with open(sys.path[0] + '\\BSC批量执行log\\all_log.txt', 'w') as f:
            for filename in os.listdir(filedir):
                filepath = filedir + '/' + filename
                for line in open(filepath):
                    f.writelines(line)
        showinfo(title='Finish', message='BSC备份完成')
        print('BSC备份完成')
        cmd.mainloop()
        ssh_shell.close()
        client.close()


def bsccmd_start():
    if askyesno(title='Are You Sure?', message='确认开始执行BSC备份吗？'):
        print('开始BSC备份')
        isExists = os.path.exists(sys.path[0] + '\\BSC批量执行log')
        if not isExists:
            os.makedirs(sys.path[0] + '\\BSC批量执行log')
        bsccmd(CmdList, BSCList)


def gethelp():
    helptext = '1、在输入栏中输入指令\n' \
               '2、点击\'执行BSC指令\'批量执行\n' \
               '3、在文件夹\'BSC批量执行log\'中生成全部log和分BSC的log'
    print('打开帮助')
    global t
    cmd = Tk()
    cmd.title('自动备份程序回显')
    cmd.geometry('500x300')
    t = Text(cmd, height=40, bg='white')
    t.pack(fill=X)
    t.insert('end', helptext)


if __name__ == '__main__':
    # global t
    root = Tk()
    root.title('诺基亚BSC批量执行程序')
    root.geometry('500x400')
    fm1 = Frame(root, bg='pink')
    fm2 = Frame(root, bg='pink')
    cv = Canvas(root, width=500, height=100, bg='pink', bd=0)
    cv.pack()
    fname = sys.path[0] + '\\Title_2.JPG'
    img = Image.open(fname)
    img = ImageTk.PhotoImage(img)
    cv.create_image(12, 25, anchor=NW, image=img)
    inp = Text(root, height=15, bg='white')
    inp.pack(fill=X)
    Button(fm1, text='执行BSC指令', command=bsccmd_start, width=15, height=2).pack(pady=25)
    Button(fm2, text='帮助', command=gethelp, width=15, height=2).pack(pady=25)
    fm1.pack(side=LEFT, fill=X, expand=YES)
    fm2.pack(side=LEFT, fill=X, expand=YES)
    root.mainloop()
