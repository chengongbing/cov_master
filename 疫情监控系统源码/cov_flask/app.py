from flask import Flask,render_template,request,jsonify
import utils
import time
import jieba
app = Flask(__name__)


@app.route('/cov')
def hello_world():  # put application's code here
    return render_template("index.html")

@app.route('/c1')
def get_cl_data():
    data=utils.get_c1_data()
    # data=(124447, 4, 116062, 5690)
    # return jsonify({"confir":1,"suspect":2,"heal":3,"dead":4})
    return jsonify({"confir":data[0],"suspect":data[1],"heal":data[2],"dead":data[3]})

@app.route('/c2')
def get_c2_data():
    res=[]
    # res=[{'name': '上海', 'value': 318}, {'name': '云南', 'value': 162}]
    for tup in utils.get_c2_data():
        # print(tup)
        res.append({"name":tup[0],"value":int(tup[1])})
    print(res)
    return jsonify({"data":res})

@app.route('/l1')
def get_l1_data():
    data=utils.get_l1_data()
    day,confirm,suspect,heal,dead=[],[],[],[],[]
    for a,b,c,d,e in data:
        # print(type(a))
        day.append(str(a)[5:10])
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day": day, "confirm": confirm, "suspect": suspect,
                    "heal": heal, "dead": dead})
    # return jsonify({"day":[100,200,300],"confirm":[1000,1100,1200],"suspect":[2000,2100,2200],"heal":[3000,3100,3200],"dead":[4000,4100,4200]})


@app.route('/l2')
def get_l2_data():
    data=utils.get_l2_data()
    day,confirm_add,suspect_add,heal_add,dead_add=[],[],[],[],[]
    for a,b,c,d,e in data:
        # print(type(a))
        day.append(str(a)[5:10])
        confirm_add.append(b)
        suspect_add.append(c)
        heal_add.append(d)
        dead_add.append(e)
    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add,
                    "heal_add": heal_add, "dead_add": dead_add})

@app.route('/r1')
def get_r1_data():
    data=utils.get_r1_data()
    city=[]
    confirm=[]
    for d in data:
        city.append(d[0])
        confirm.append(int(d[1]))
    return jsonify({"city":city,"confirm":confirm})

@app.route('/r2')
def get_r2_data():
    data=utils.get_r2_data()
    s=""

    for d in data:
        s+=d[0]
    s = s.replace("：", "").replace("“", "")
    l=[]
    ls=jieba.lcut(s)
    dic={}
    for d in ls:
        dic[d]=dic.get(d,0)+1
    for d in dic:
        l.append({"name":d,"value":dic[d]})
    print(l)
    return jsonify({"kws":l})

@app.route('/time')
def get_time():

    return utils.get_time()

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
