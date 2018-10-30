# encoding=utf-8
import paramiko
import time
import multiprocessing
from tkinter import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
import os
import re
import pandas as pd
from datetime import datetime

iplist = ['10.222.27.36',
          '10.222.27.37',
          '10.222.11.77',
          '10.222.11.78',
          '10.222.18.93',
          '10.222.18.94',
          '10.222.25.21',
          '10.222.25.22',
          # '10.222.11.244',
          # '10.222.11.245'
          ]
dict1 = {'10.222.27.36': 'CE1-QZ',
         '10.222.27.37': 'CE2-QZ',
         '10.222.11.77': 'CE3-JQ',
         '10.222.11.78': 'CE4-JQ',
         '10.222.18.93': 'CE5-WR',
         '10.222.18.94': 'CE6-WR',
         '10.222.25.21': 'CE7-PD',
         '10.222.25.22': 'CE8-PD',
         # '10.222.11.244': 'CE9-CM',
         # '10.222.11.245': 'CE10-CM'
         }
CmdList = [
           # 'dis cu',
           'dis cpu-u',
           'dis mem',
           'dis int bri',
           'dis ala all'
           ]
waittime = 0.5
CommonRecv = b'>'


def sendcmd(com, rec, ssh_shell, outputfile):
    ssh_shell.sendall(com + '\r\n')
    time.sleep(waittime)
    while True:
        line = ssh_shell.recv(4096)
        if line and line.endswith(rec):
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


def NEcmd(ilist):
    global t
    cmd_back = Tk()
    cmd_back.title('自动备份程序回显')
    cmd_back.geometry('800x500')
    t = Text(cmd_back, height=40, bg='white')
    scroll = Scrollbar(cmd_back, orient=VERTICAL)
    scroll.config(command=t.yview)
    scroll.pack(fill=Y, expand=0, side=RIGHT, anchor=N)
    t.pack(fill=X)
    ip = ilist[0]
    CmdList = ilist[1]
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username='username', password='password', look_for_keys=False)
    ssh_shell = client.invoke_shell()
    while True:
        start = ssh_shell.recv(1024)
        if start and start.endswith(b'>'):
            break
    outputfile = open(sys.path[0] + '\\NE自动月报\\' + dict1[ip] + '.txt', 'w')
    for cmd in CmdList:
        sendcmd(cmd, CommonRecv, ssh_shell, outputfile)
    outputfile.close()
    cmd_back.destroy()
    cmd_back.mainloop()
    ssh_shell.close()
    client.close()


def getcsv():
    cpu_usage_re = re.compile('^CPU Usage\s+:\s(\d+)%\s+Max:\s\d+%')
    memory_usage_re = re.compile('^ Memory Using Percentage Is:\s+(\d+)%')
    flow_re = re.compile('^\s*GigabitEthernet\d/\d/\d+\s+up\s+up\s+(\d+\.\d*)%\s+(\d+\.\d*)%')
    alarm_re = re.compile('^(\d)\s+([A-Z][a-z]+)\s+(\d{2}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(.+)')
    alarm_info_re = re.compile('^\s{32,}(.+)')
    filenames = os.listdir(sys.path[0] + '\\NE自动月报\\')
    ne_list = []
    cpu_list = []
    memory_list = []
    flow_in_ave_list = []
    flow_out_ave_list = []
    alarms_list = []
    for file in filenames:
        flow_in_list = []
        flow_out_list = []
        al_index = None
        al_info = ''
        if file.split('.')[-1] == 'txt':
            ne_list.append(file.split('.')[0])
            with open(sys.path[0] + '\\NE自动月报\\' + file) as f:
                datas = f.readlines()
            for l in datas:
                cpu_usage = cpu_usage_re.search(l)
                mem_usage = memory_usage_re.search(l)
                flow = flow_re.search(l)
                alarm = alarm_re.search(l)
                info = alarm_info_re.search(l)
                if cpu_usage:
                    cpu_list.append(cpu_usage.group(1))
                if mem_usage:
                    memory_list.append(mem_usage.group(1))
                if flow:
                    flow_in_list.append(float(flow.group(1)))
                    flow_out_list.append(float(flow.group(2)))
                if alarm:
                    if al_index is not None:
                        alarms_list.append([file.split('.')[0], al_index, al_level,
                                            datetime.strptime(al_date + ' ' + al_time,
                                                              '%y-%m-%d %H:%M:%S'),
                                            al_info])
                    al_index = alarm.group(1)
                    al_level = alarm.group(2)
                    al_date = alarm.group(3)
                    al_time = alarm.group(4)
                    al_info = alarm.group(5)
                if info:
                    al_info = al_info + info.group(1)
            if al_index is not None:
                alarms_list.append(
                    [file.split('.')[0], al_index, al_level,
                     datetime.strptime(al_date + ' ' + al_time, '%y-%m-%d %H:%M:%S'), al_info])
            if len(flow_in_list) != 0:
                in_ave = "%.2f" % float(sum(flow_in_list) / len(flow_in_list))
                flow_in_ave_list.append(in_ave)
            else:
                flow_in_ave_list.append('0')
            if len(flow_out_list) != 0:
                out_ave = "%.2f" % float(sum(flow_out_list) / len(flow_out_list))
                flow_out_ave_list.append(out_ave)
            else:
                flow_out_ave_list.append('0')
    df_all = pd.DataFrame([ne_list, cpu_list, memory_list, flow_in_ave_list, flow_out_ave_list])
    df = df_all.T
    df.columns = ['NE40名称', 'CPU占用率', '内存占用率', 'Abis接收带宽平均利用率', 'Abis发送带宽平均利用率']
    print(df)
    df_alarm = pd.DataFrame(alarms_list)
    df_alarm.columns = ['Ne40', 'Id', 'Level', 'Time', 'Info']
    print(df_alarm)
    with open(sys.path[0] + '\\NE自动月报\\' + 'NE40月报.csv', 'w') as f:
        df.to_csv(f, sep=',', index=False, header=1)
    with open(sys.path[0] + '\\NE自动月报\\' + 'NE40告警.csv', 'w') as f:
        df_alarm.to_csv(f, sep=',', index=False, header=1)


def cmd_start():
    if askyesno(title='Are You Sure?', message='确认开始获取NE数据吗？'):
        print('开始获取NE数据')
        isExists = os.path.exists(sys.path[0] + '\\NE自动月报')
        if not isExists:
            os.makedirs(sys.path[0] + '\\NE自动月报')
        ilist = [(i, CmdList) for i in iplist]
        p = multiprocessing.Pool(4)  # 1
        p.map(NEcmd, ilist)
        showinfo(title='Finish', message='获取NE数据完成')
        print('获取NE数据完成')


def get_start():
    if askyesno(title='Are You Sure?', message='确认开始生成NE月报吗？'):
        print('开始生成月报')
        isExists = os.path.exists(sys.path[0] + '\\NE自动月报')
        if not isExists:
            os.makedirs(sys.path[0] + '\\NE自动月报')
        getcsv()
        showinfo(title='Finish', message='NE月报完成')
        print('NE月报完成')


if __name__ == '__main__':
    root = Tk()
    root.title('NE40月报生成器')
    root.geometry('500x200')
    fm1 = Frame(root, bg='pink')
    fm2 = Frame(root, bg='pink')
    cv = Canvas(root, width=500, height=100, bg='pink', bd=0)
    cv.pack()
    fname = sys.path[0] + '\\Title.JPG'
    img = Image.open(fname)
    img = ImageTk.PhotoImage(img)
    cv.create_image(80, 25, anchor=NW, image=img)
    # t = Text(root, height=20, bg='white')
    # t.pack(fill=X)
    Button(fm1, text='获取NE数据', command=cmd_start, width=15, height=2).pack(pady=25)
    Button(fm2, text='生成月报', command=get_start, width=15, height=2).pack(pady=25)
    fm1.pack(side=LEFT, fill=X, expand=YES)
    fm2.pack(side=LEFT, fill=X, expand=YES)
    root.mainloop()
