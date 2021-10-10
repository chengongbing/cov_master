import requests
import json
import pymysql
import time
import traceback
connect=pymysql.connect(host="####",user="####",password="###",db="###")

cur=connect.cursor()

def history():
    data_history=[]
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
    res = requests.get(url)
    # print(type(res.text))
    html = json.loads(res.text)
    html = html["data"]
    data_dict = json.loads(html)
    dh = []
    for i in range(len(data_dict["chinaDayList"])):
        # print(data_dict["chinaDayList"][i])
        # print("-"*100)
        t = "2021." + data_dict["chinaDayList"][i]["date"]
        tup=time.strptime(t,"%Y.%m.%d")
        ds=time.strftime("%Y-%m-%d",tup)
        ljqz = data_dict["chinaDayList"][i]["confirm"]  # 累计确诊
        ljqz_yes = data_dict["chinaDayAddList"][i]["confirm"]  # 累计确诊较昨日

        ljsw = data_dict["chinaDayList"][i]["dead"]  # 累计死亡
        ljsw_yes = data_dict["chinaDayAddList"][i]["dead"]  # 累计死亡较昨日

        ljzy = data_dict["chinaDayList"][i]["heal"]  # 累计治愈
        ljzy_yes = data_dict["chinaDayAddList"][i]["heal"]  # 累计治愈较昨日

        xyys = data_dict["chinaDayList"][i]["suspect"]  # 现有疑似
        xyys_yes = data_dict["chinaDayAddList"][i]["suspect"]  # 现有疑似较昨日
        data_history.append([ds,ljqz,ljqz_yes,xyys,xyys_yes,ljzy,ljzy_yes,ljsw,ljsw_yes])
    return data_history
def insert_history():
    print(f"{time.asctime()}history开始插入数据")
    for data in history():
        insert_history="insert into history (ds,confirm,confirm_add,suspect,suspect_add,heal,heal_add,dead,dead_add) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"     #插入history
        cur.execute(insert_history,data)
        connect.commit()
    print(f"{time.asctime()}history开始插入数据")

def update_history():
    try:
        data=history()
        for dt in data:
            select_details = "select confirm from history where ds=%s"
            if not cur.execute(select_details, dt[0]):
                print(f"{time.asctime()}开始更新history数据")
                insert_history = "insert into history(ds,confirm,confirm_add,suspect,suspect_add,heal,heal_add,dead,dead_add) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # 插入history
                cur.execute(insert_history, dt)#
                connect.commit()
        else:
            print("history表已是最新数据")
    except:
        traceback.print_exc()
# insert_history()
# insert_details()
# update_details()
update_history()
cur.close()
connect.close()