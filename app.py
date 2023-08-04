import dbutil
import pymysql
import numpy as np
import pandas as pd
from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/city_tranavg")
def city_tranavg():
    xdata = []
    ydata = []
    con = dbutil.getCon()
    cursor = con.cursor()
    cursor.execute("select * from city_tranavg")
    rows = cursor.fetchall()
    for row in rows:
        xdata.append(row[0])
        ydata.append(row[1])
    return render_template("city_tranavg.html",xdata=xdata,ydata=ydata)

@app.route("/city_type_tranavg")
def city_type_tranavg():
    con = dbutil.getCon()
    cursor = con.cursor()
    cursor.execute("SELECT city, building_type, avg_price from city_type_tranavg")
    results = cursor.fetchall()
    # 将查询结果转换为列表
    city_list, building_type_list, price_list = [], [], []
    for result in results:
        city_list.append(result[0])
        building_type_list.append(result[1])
        price_list.append(result[2])

# 将城市去重，构建为 radar 组件的 indicator
    indicator = []
    for city in set(city_list):
        indicator.append({"name": city, "max": 30000})

# 构建雷达图的数据
    data = []
    for building_type in set(building_type_list):
        data_temp = []
        for city in set(city_list):
            price = 0
            for i, v in enumerate(city_list):
                if v == city and building_type_list[i] == building_type:
                    price = price_list[i]
                    break
            data_temp.append(price)
        data.append({'value': data_temp, 'name': building_type})
    return render_template("city_type_tranavg.html", indicator=indicator, data=data)

@app.route("/city_building_count")
def city_building_count():
    con = dbutil.getCon()
    cursor = con.cursor()
    cursor.execute("SELECT city, building_structure, count FROM city_structure_shuliang")
    rows = cursor.fetchall()

    # 构造树形结构数据
    tree_data = []
    for row in rows:
        city = row[0]
        structure = row[1]
        count = row[2]
        # 判断是否已经存在该城市的节点
        city_node = None
        for node in tree_data:
            if node["name"] == city:
                city_node = node
                break
        # 如果不存在，则添加一个新节点
        if not city_node:
            city_node = {"value": count, "name": city, "children": []}
            tree_data.append(city_node)
        else:
            city_node["value"] += count  # 更新城市节点的值
        # 添加该城市对应的建筑物结构节点
        city_node["children"].append({
            "value": count,
            "name": structure
        })

    # 构造treemap所需数据
    treemap_data = [{
        "name": "建筑结构数量",
        "children": tree_data,
    }]

    return render_template("city_building_count.html", treemap_data=treemap_data)

@app.route("/city_111")
def city_tranavg():
    db = pymysql.connect(
    host = "192.168.109.142",
    database = "hive",
    user = "root",
    password = "ljh2002610",
    port = 3306,
    charset = 'utf8'
)
    #sql语句
    sqlcmd = "select housing_orientation,price_structure from cdhouse_op"
    a=pd.read_sql(sqlcmd,db)
    #取前5行数据
    b=a.to_numpy()
    fangwei = b[:,0]
    list_fangwei=[]
    for i in list(set(fangwei)):
        n = 0
        for j in b:
            if i==j[0]:
                n+=1
        list_fangwei.append([i,n])
    list_fangwei=np.array(list_fangwei).transpose()

    x_data = list_fangwei[0]
    y_data = list_fangwei[1]

    c = [list(z) for z in zip(x_data, y_data)]
    n = [{'value': i[1], 'name': i[0]} for i in c]
    return render_template('pie-doughnut.html',data_all=n)



if __name__ == '__main__':
    app.run(debug=True)