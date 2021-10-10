import time

import jieba
import pymysql
import pprint

def get_time():
    time_str=time.strftime("%Y-%m-%d %X")
    return time_str

def get_c1_data():
    conn=pymysql.connect(host="####",user="####",password="###",db="###")
    cursor=conn.cursor()
    sql="select confirm,suspect,heal,dead from history"
    cursor.execute(sql)
    conn.commit()
    d=cursor.fetchall()[-1]
    conn.close()
    cursor.close()
    return d

def get_c2_data():

    conn=pymysql.connect(host="####",user="####",password="###",db="###")
    cursor=conn.cursor()
    sql="select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    cursor.execute(sql)
    conn.commit()
    d=cursor.fetchall()
    conn.close()
    cursor.close()
    return d

def get_l1_data():

    conn=pymysql.connect(host="####",user="####",password="###",db="###")
    cursor=conn.cursor()
    sql = "select ds,confirm,suspect,heal,dead from history "
    cursor.execute(sql)
    conn.commit()
    d=cursor.fetchall()
    conn.close()
    cursor.close()
    return d

def get_l2_data():

    conn=pymysql.connect(host="####",user="####",password="###",db="###")
    cursor=conn.cursor()
    sql = "select ds,confirm_add,suspect_add,heal_add,dead_add from history "
    cursor.execute(sql)
    conn.commit()
    d=cursor.fetchall()
    conn.close()
    cursor.close()
    insert_h2(d)
    return d

def insert_h2():
    conn=pymysql.connect(host="####",user="####",password="###",db="###")
    cursor = conn.cursor()
    sql_insert="insert into history_2(province,confirm) values(%s,%s)"
    cursor.execute(sql_insert,d)
    conn.commit()
    conn.close()
    cursor.close()

def get_r1_data():
    conn=pymysql.connect(host="####",user="####",password="###",db="###")
    cursor=conn.cursor()
    sql = 'select city,confirm from ' \
          '(select city,confirm from details ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province not in ("湖北","北京","上海","天津","重庆","地区待确认","境外输入") ' \
          'union all ' \
          'select province as city,sum(confirm) as confirm from details ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province in ("北京","上海","天津","重庆") group by province) as a ' \
          'order by confirm desc limit 15'
    cursor.execute(sql)
    conn.commit()
    d=cursor.fetchall()
    conn.close()
    cursor.close()
    l=[]
    for data in d:
        if data[0] not in ["地区待确认","境外输入"]:
            l.append(data)
    return l[:5]

def get_r2_data():
    conn=pymysql.connect(host="####",user="####",password="###",db="###")
    cursor = conn.cursor()
    sql = "select content from hotsearch order by id desc limit 40"
    cursor.execute(sql)
    conn.commit()
    d = cursor.fetchall()
    conn.close()
    cursor.close()
    return d

if __name__=="__main__":
    # print(get_c1_data())
    # print(get_c2_data())
    # pprint.pprint(get_l1_data()[0][0])
    # pprint.pprint(get_l2_data())
    pprint.pprint(get_r1_data())
    data=get_r2_data()
    s=""
    for d in data:
        s+=d[0]
    l=[]
    s=s.replace("：","").replace("“","")
    ls=jieba.lcut(s)
    dic={}
    for d in ls:
        dic[d]=dic.get(d,0)+1
    for d in dic:
        l.append({"name":d,"value":dic[d]})
    # pprint.pprint(l)
    pprint.pprint(get_c2_data())