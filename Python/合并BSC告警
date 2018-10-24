# coding: utf-8
import re
import pandas as pd

BSCList = ['BSC59-0', 'BSC60-D', 'BSC60-E', 'BSC60-F', 'BSC69-C', 'BSC69-D', 'BSC69-E', 'BSC77-4',
           'BSC77-5', 'BSC82-C', 'BSC82-D', 'BSC82-E', 'BSC82-F', 'BSC83-0', 'BSC83-1', 'BSC83-2',
           'BSC83-3', 'BSC84-C', 'BSC84-D', 'BSC84-E', 'BSC84-F', 'BSC85-B', 'BSC85-C', 'BSC85-D',
           'BSC85-E', 'BSC85-F', 'BSC86-D', 'BSC86-E', 'BSC86-F', 'BSC86-C', 'BSC57-F', 'BSC63-E',
           'BSC63-F', 'BSC72-8', 'BSC72-9', 'BSC74-E', 'BSC74-F', 'BSC75-E', 'BSC75-F', 'BSC87-3',
           'BSC87-4', 'BSC88-E', 'BSC88-F', 'BSC89-D', 'BSC89-E', 'BSC89-F', 'BSC57-E'
           ]

alarm_1 = re.compile('^\s{10,}(BSC\d{2}-.{1})\s+(.+)\s+(.+)\s+(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})')
alarm_2 = re.compile('^\*+\s+ALARM\s+(.+)\s+(.+-\d{2})\s+(.+)')
alarm_3 = re.compile('^\s{4,}(\(\d{4}\))\s+(\d{4})\s+(.+)')
alarm_4 = re.compile('^\s{4,}([A-Za-z0-9]+)\s+([A-Za-z0-9]+)\s+(.+)')

fi_bsc_list = []
se_unit_list = []
fi_datetime_list = []
fi_date_list = []
fi_time_list = []
th_NR_list = []
th_NAME_list = []

for bsc in BSCList:
    with open(bsc + '.txt') as f:
        alarms = f.readlines()
    fi_bsc = None
    for l in alarms:
        first = alarm_1.search(l)
        second = alarm_2.search(l)
        third = alarm_3.search(l)
        forth = alarm_4.search(l)
        if first:
            if fi_bsc is not None:
                # print(fi_bsc, se_unit, fi_date, fi_time, th_NR, th_NAME)
                fi_bsc_list.append(fi_bsc)
                se_unit_list.append(se_unit.strip())
                fi_datetime_list.append(fi_date + ' ' + fi_time)
                fi_date_list.append(fi_date)
                fi_time_list.append(fi_time)
                th_NR_list.append(th_NR)
                th_NAME_list.append(th_NAME.strip())
                # 上一条告警入库
            fi_bsc = first.group(1)
            fi_unit = first.group(2)
            fi_date = first.group(4)
            fi_time = first.group(5)

        if second:
            se_unit = second.group(1)
            se_locate = second.group(2)
            se_thing = second.group(3)

        if third:
            th_index = third.group(1)
            th_NR = third.group(2)
            th_NAME = third.group(3)

    # print(fi_bsc, se_unit, fi_date, fi_time, th_NR, th_NAME)
    fi_bsc_list.append(fi_bsc)
    se_unit_list.append(se_unit.strip())
    fi_datetime_list.append(fi_date + ' ' + fi_time)
    fi_date_list.append(fi_date)
    fi_time_list.append(fi_time)
    th_NR_list.append(th_NR)
    th_NAME_list.append(th_NAME.strip())
    # 入库最后一条告警
df_all = pd.DataFrame([fi_bsc_list, se_unit_list, fi_datetime_list, th_NR_list, th_NAME_list])
df = df_all.T
with open('all_alarm.csv', 'w') as f:
    df.to_csv(f, sep=',', index=False, header=None)
