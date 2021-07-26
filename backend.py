"""
    render_template 是渲染模板用的，这里我们用来返回 index.html
    flask_cors 用来解决跨域的问题
"""
import os
import traceback
import json
import numpy as np
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import csv

# 通过 static_folder 指定静态资源路径，以便 index.html 能正确访问 CSS 等静态资源
# template_folder 指定模板路径，以便 render_template 能正确渲染 index.html
app = Flask(__name__, static_folder='./templates/static', template_folder='./templates')

CORS(app, supports_credentials=True)
# data = None

# 尝试重写load_data函数
def load_data(path):
    with open(path, 'r+', encoding='utf-8') as f:
        data_mat = [i[:-1].split(',') for i in f.readlines()]
        data_mat = data_mat[1:]
        data_mat = np.transpose(data_mat)
        time = data_mat[0]
        data = data_mat[1:]
        return time,data


def transformMatrix(m):
    rt = [[] for i in m[0]]    # m[0] 有几个元素，说明原矩阵有多少列。此处创建转置矩阵的行
    for ele in m:
        for i in range(len(ele)):
            # rt[i] 代表新矩阵的第 i 行
            # ele[i] 代表原矩阵当前行的第 i 列
            rt[i].append(ele[i])
    return rt


def strip_first_col(fname, delimiter):
    with open(fname, 'r') as fin:
        for line in fin:
            try:
                yield line.split(delimiter, 1)[1]
            except IndexError:
                continue


@app.route("/")
def index():
    """
        当在浏览器访问网址时，通过 render_template 方法渲染 dist 文件夹中的 index.html。
        页面之间的跳转交给前端路由负责，后端不用再写大量的路由
    """
    return render_template('index.html')


# 上传文件
@app.route("/upload", methods=['POST'])
def upload():
    # noinspection PyBroadException
    try:
        file_name = request.data.decode("utf-8")
        path = "./data/" + file_name
        print(path)
        # 应该在前端留接口
        metric_num, input_size, day_num = 19, 288, 15
        # global data
        # data = loadData(path, metric_num, input_size, day_num)
        timestamp, data = load_data(path)
        if timestamp[0]=='1':
            daylength = np.ceil(len(timestamp)/288)
            gen_timestamp = ["D%d-%02d:%02d" %(d,h,m) for d in range(1,int(daylength+1)) for h in range(0,24) for m in range(0,60,5)]
            timestamp = gen_timestamp[0:len(timestamp)]
        min_gap = get_interval(timestamp)
        dict_data = {'datas': data.tolist(), 'timestamp': timestamp, 'mingap': min_gap}
        # dict_data = {'datas': data.tolist(), 'timestamp': timestamp.tolist()}

        # 将文件的数据以dict形式存储至json文件中
        with open('./' + file_name + '_data.json', 'w', encoding='utf-8') as fp:
            json.dump(dict_data, fp, ensure_ascii=True)
        # print('==========================================')
        # with open('./info.json','r',encoding='utf-8') as fp:
        #     t_dict = json.load(fp)
        #     print(t_dict)

        # return jsonify(message)
        # return jsonify(data.tolist())
        return 'success'
    except Exception as e:
        traceback.print_exc()
        return jsonify({'status': 'fail'})

def get_interval(time_list):
    return abs(int(time_list[1][-2:]) - int(time_list[0][-2:]))

@app.route('/get/<file_name>', methods=['GET'])
def get_data(file_name):
    global data
    # noinspection PyBroadException
    with open('./' + file_name + '_data.json', 'r', encoding='utf-8') as fp:
        t_dict = json.load(fp)
        data = t_dict

    # try:
    return jsonify(data)

    # except Exception as e:
    #     traceback.print_exc()

    #     return None

@app.route('/post/export', methods=['POST'])
def export_data():
    data = request.get_data()
    data = json.loads(data)
    print(data)
    d_data_list = []
    d_mark_list = []
    d_time_list = []
    for i in range(4):
        j = 0
        tdlist = []
        tmlist = []
        ttlist = []
        while j < len(data[str(i)+'_data']):
            tdlist.append(data[str(i)+'_data'][j:j+288])
            tmlist.append(data[str(i)+'_markdata'][j:j+288])
            ttlist.append(data['timestamp'][j:j+288])
            j+=288
        d_data_list.append(tdlist)
        d_mark_list.append(tmlist)
        d_time_list.append(ttlist)
        # print(d_mark_list)
    for i in range(4):
        data_list = []
        for j in range(len(d_mark_list[i])):
            if 1 in d_mark_list[i][j] or 2 in d_mark_list[i][j]:
                day = '_day_'+str(j+1)
                if 2 in d_mark_list[i][j]:
                    day+='_anomaly'
                else:
                    day+='_outlier'
                if data_list == []:
                    data_list.append(d_time_list[i][j])
                    data_list.append(d_data_list[i][j])
                    data_list.append(d_mark_list[i][j])
                else:
                    data_list[0].extend(d_time_list[i][j])
                    data_list[1].extend(d_data_list[i][j])
                    data_list[2].extend(d_mark_list[i][j])
                if d_mark_list[i][j][-1] != 1:
                    data_list = np.transpose(data_list)
                    with open("./marked/"+(data['filename']+'_kpi_'+str(i)+ day +".csv"),"w+",newline='') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerows(data_list)
                        csvfile.close()
                        data_list = []
    return 'exported'


@app.route('/del/<file_name>', methods=['POST'])
def del_data(file_name):
    print('remove:' + './' + file_name + '_data.json')
    os.remove('./' + file_name + '_data.json')
    return 'deleted'


if __name__ == '__main__':
    # 开启 debug模式，这样我们就不用每更改一次文件，就重新启动一次服务
    # 设置 host='0.0.0.0'，让操作系统监听所有公网 IP
    # 也就是把自己的电脑作为服务器，可以让别人访问
    # app.run(debug=True)
    app.run(debug=True)
