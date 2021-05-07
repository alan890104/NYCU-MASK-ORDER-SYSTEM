from flask import Flask,jsonify,request,redirect
from flask_cors import CORS
import sqlite3
import hashlib
from database import *

app = Flask(__name__)



@app.route('/user/login' , methods=['POST'])
def login():
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT uid,account,passwd,phone FROM user WHERE account=?;",(request.form['account'],))
    data = cur.fetchone()
    return_obj = {'info':'','status':0,'data':{}}
    if not data:
        return_obj['info'] = 'User Not Exist'
    else:
        if encrypt(request.form['passwd'].strip()) != data[2].strip():
            return_obj['info'] = 'Password Not Correct'
        else:
            return_obj['info'] = 'Success'
            return_obj['status'] = 1
            return_obj['data'] = {'uid':data[0],'account':data[1],'phone':data[3]}
    cur.close()
    con.close()
    return jsonify(return_obj)

@app.route('/user/register' , methods=['POST'])
def register():
    print(request.form)
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    account = request.form['account']
    encrpt_passwd = encrypt(request.form['passwd'])
    phone = request.form['phone']
    info,status =  add_user(con, cur, account, encrpt_passwd, phone)

    cur.close()
    con.close()
    return jsonify({"info":info,"status":status})
    
@app.route('/shop/register/<uid>' , methods=['POST'])
def register_shop(uid):
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    name = request.form['name']
    city = request.form['city']
    price = request.form['price']
    amount = request.form['amount']
    info,status =  add_shop(con, cur, name, city, price, amount,uid)
    cur.close()
    con.close()
    return jsonify({"info":info,"status":status})
    
@app.route('/shop/query' , methods=['POST'])
def query_shop():
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    data =  list_shop(con,cur)
    cur.close()
    con.close()
    return jsonify({"info":"Success",'status':1,"data":data})

@app.route('/shop/query/uid/<uid>' , methods=['POST'])
def query_specify_shop_by_uid(uid):
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT * FROM shop WHERE uid = ?",[uid])
    data = cur.fetchone()
    return_obj = {"info":'Success',"status":0}
    if not data:
        return_obj["info"] = "Fail"
    else:
        return_obj["status"] = 1
        return_obj["data"] = {"sid":data[0],"name":data[1],"city":data[2],"price":data[3],"amount":data[4],"uid":data[5]}
    cur.close()
    con.close()
    return jsonify(return_obj)

@app.route('/shop/query/name/<name>' , methods=['POST'])
def query_specify_shop_by_name(name):
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT * FROM shop WHERE name = ?",[name])
    data = cur.fetchone()
    return_obj = {"info":'Success',"status":0,"data":{}}
    if not data:
        return_obj["info"] = "Fail"
    else:
        return_obj["status"] = 1
        return_obj["data"] = {"sid":data[0],"name":data[1],"city":data[2],"price":data[3],"amount":data[4],"uid":data[5]}
    cur.close()
    con.close()
    return jsonify(return_obj)

@app.route('/shop/query/sid/<sid>' , methods=['POST'])
def query_specify_shop_by_sid(sid):
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT * FROM shop WHERE sid = ?",[sid])
    data = cur.fetchone()
    return_obj = {"info":'Success',"status":0,"data":{}}
    if not data:
        return_obj["info"] = "Fail"
    else:
        return_obj["status"] = 1
        return_obj["data"] = {"sid":data[0],"name":data[1],"city":data[2],"price":data[3],"amount":data[4],"uid":data[5]}
    cur.close()
    con.close()
    return jsonify(return_obj)

@app.route('/shop/query/condition/<uid>' , methods=['POST'])
def query_shop_by_conditioin(uid):
    print("WTF",request.form)
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    condition = {}
    condition['name'] = '%' if request.form['shop']==None else '%'+request.form['shop']+'%'
    condition['city'] = '%' if request.form['city']==None else '%'+request.form['city']+'%'
    condition['price_min'] = request.form['price_min']
    
    if isinstance(request.form['price_max'], int):
        condition['price_max'] = "AND price<{}".format(request.form['price_max'])
    else:
        condition['price_max'] = ''

    if request.form['amount_type']==0:
        condition['amount_type'] = 'AND amount=0'
    elif request.form['amount_type']==1:
        condition['amount_type'] = 'AND amount BETWEEN 1 AND 5000'
    elif request.form['amount_type']==2:
        condition['amount_type'] = 'AND amount>5000'
    else:
        condition['amount_type'] = ''

    if request.form['only_show_work']==1: # 只顯示自己工作的店家
        cur.execute("SELECT shop.name FROM shop inner join work on shop.sid=work.sid\
                     where work.uid=? or shop.uid=? AND price>? AND name LIKE ? AND city LIKE ? \
                    {} {}".format(condition['price_max'],condition['amount_type']) , [uid,uid,condition['price_min'],condition['name'],condition['city']])
    else:
        cur.execute("SELECT shop.name FROM shop WHERE price>? AND name LIKE ? AND city LIKE ? \
                    {} {}".format(condition['price_max'],condition['amount_type']) , [condition['price_min'],condition['name'],condition['city']])
    
    data = cur.fetchall()
    cur.close()
    con.close()
    return jsonify({"info":"Success","status":1,"data":data})

@app.route('/mask/edit/<sid>' , methods=['POST'])
def edit_mask(sid):
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    price = request.form['price']
    amount = request.form['amount']
    info,status = update_mask_price_amount(con, cur, sid, price, amount)
    cur.close()
    con.close()
    return jsonify({"info":info,"status":status})

@app.route('/employee/add' , methods=['POST'])
def add_employee_to_shop():
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    sid = request.form['sid']
    account = request.form['account']
    info,status = add_employee(con,cur,sid, account)
    cur.close()
    con.close()
    return jsonify({"info":info,"status":status})

@app.route('/employee/del' , methods=['POST'])
def del_employee_from_shop():
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    sid = request.form['sid']
    account = request.form['account']
    info,status = del_employee(con,cur,sid, account)
    cur.close()
    con.close()
    return jsonify({"info":info,"status":status})
    

@app.route('/employee/query/sid/<sid>' , methods=['POST'])
def show_shop_employees(sid):
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT account,phone FROM user NATURAL JOIN work WHERE sid=?",(sid,))
    data = cur.fetchall()
    cur.close()
    con.close()
    return jsonify({"info":"Success","status":1,"data":data})

@app.route('/employee/query/uid/<uid>' , methods=['POST'])
def show_work_places(uid):
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT name FROM shop inner join work on shop.sid=work.sid where work.uid=?",(uid,))
    data = cur.fetchall()
    cur.close()
    con.close()
    return jsonify({"info":"Success","status":1,"data":data})

if __name__=='__main__':
    app.debug=True
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.run(host="0.0.0.0",port=5000)