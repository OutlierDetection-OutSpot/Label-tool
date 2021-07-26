"""
    render_template 是渲染模板用的，这里我们用来返回 index.html
    flask_cors 用来解决跨域的问题
"""
import os
import numpy as np

np.set_printoptions(suppress=True)
data_dir = "../data/"
length_per_day = 288
day_num = 15
has_timestamp = False
'''
If "choose_machine == True", plz rewrite the machine_list
Else give the range of machine numbers. (the files' name is successive)
'''
choose_machine = True
machine_list = [0, 100, 200, 300]
machine_start = 0
machine_end = 2


def convert_format(length_per_day, day_num, kpi_id):
    global choose_machine
    if choose_machine:
        global machine_list
        file_list = machine_list
    else:
        global machine_start, machine_end
        file_list = [i for i in range(machine_start, machine_end + 1)]

    machine_num = len(file_list)
    data = np.zeros(shape=(length_per_day * day_num, machine_num + 1))
    np.set_printoptions(suppress=True)
    header = ['machine_%d' % num for num in file_list]

    path = data_dir + str(file_list[0]) + ".txt"
    temp_data = np.loadtxt(path, delimiter=',', skiprows=1)
    global has_timestamp
    if has_timestamp:
        time = temp_data[:, 0]
    else:
        time = [int(i) for i in range(1, temp_data.shape[0] + 1)]
    data[:, 0] = time

    for i, file_name in enumerate(file_list):
        path = data_dir + str(file_name) + ".txt"
        temp_data = np.loadtxt(path, delimiter=',', skiprows=1)
        data[:, i + 1] = temp_data[:, kpi_id-1]

    name = data_dir + 'kpi_' + str(kpi_id) + '.txt'
    # delimiter=',',
    np.savetxt(name, data, header="time," + ",".join(header),
               fmt=','.join(['%d'] + ['%.2f'] * machine_num), comments='')


if __name__ == '__main__':
    # kpi_id start from one!!
    kpi_num = 19
    for id in range(1, kpi_num + 1):
        convert_format(length_per_day, day_num, id)
