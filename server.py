from flask import Flask,jsonify,request,redirect
from flask_cors import CORS
import sqlite3
import hashlib
from database import *
import datetime
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
    print(jsonify({"info":info,"status":status}))
    return jsonify({"info":info,"status":status})
    
@app.route('/shop/query' , methods=['POST'])
def query_shop():
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    data =  list_shop(con,cur)
    print(data)
    cur.close()
    con.close()
    return jsonify({"info":"Success",'status':1,"data":data})

@app.route('/shop/query/uid/<uid>' , methods=['POST'])
def query_specify_shop_by_uid(uid):
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT * FROM shop WHERE uid = ?",[uid,])
    data = cur.fetchone()
    print(data)
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
    condition['name'] = '%' if request.form['shop']=='' else '%'+request.form['shop']+'%'
    condition['city'] = '%' if request.form['city']=='All' else '%'+request.form['city']+'%'
    condition['price_min'] = request.form['price_min']
    
    if isinstance(request.form['price_max'], str):
        if request.form['price_max']!='-1':
            condition['price_max'] = " AND price<={}".format(request.form['price_max'])
        else:
            condition['price_max'] = ''
    else:
        condition['price_max'] = ''

    if request.form['amount_type']=='0':
        condition['amount_type'] = 'AND amount=0'
    elif request.form['amount_type']=='1':
        condition['amount_type'] = 'AND amount BETWEEN 1 AND 5000'
    elif request.form['amount_type']=='2':
        condition['amount_type'] = 'AND amount>5000'
    else:
        condition['amount_type'] = ''

    if request.form['only_show_work']=='1': # 只顯示自己工作的店家
        cur.execute("SELECT DISTINCT shop.name,shop.city,shop.price,shop.amount FROM shop left join work on shop.sid=work.sid\
                     where (work.uid=? or shop.uid=?) AND price>=? AND name LIKE ? AND city LIKE ? \
                    {} {}".format(condition['price_max'],condition['amount_type']) , [uid,uid,condition['price_min'],condition['name'],condition['city']])
    else:
        cur.execute("SELECT shop.name,shop.city,shop.price,shop.amount FROM shop WHERE price>=? AND name LIKE ? AND city LIKE ? \
                    {} {}".format(condition['price_max'],condition['amount_type']) , [condition['price_min'],condition['name'],condition['city']])
    
    data = cur.fetchall()
    print(data)
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
    print("#######ADD EMPLYEE FROM SHOP#########")
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    sid = request.form['sid']
    account = request.form['account']
    info,status,phone = add_employee(con,cur,sid, account)
    cur.close()
    con.close()
    return jsonify({"info":info,"status":status,"data":phone})

@app.route('/employee/del' , methods=['POST'])
def del_employee_from_shop():
    print("#######DELETE EMPLYEE FROM SHOP#########")
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
    cur.execute("SELECT DISTINCT shop.name FROM shop left join work on shop.sid=work.sid where (work.uid=? or shop.uid=?)",(uid,uid,))
    data = cur.fetchall()
    print(data)
    cur.close()
    con.close()
    return jsonify({"info":"Success","status":1,"data":data})

@app.route('/order/create/<uid>' , methods=['POST'])
def create_order(uid):
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    print(request.form)
    name = request.form['name']
    amount = request.form['amount']
    price = request.form['price']
    # orders shema = oid,status,start,finish,creator,completer,sid,amount,price
    cur.execute("SELECT sid FROM shop WHERE name = ?",[name])
    sid = cur.fetchone()[0]
    status = '0'
    start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    finish = None
    creator = uid
    completer = None
    input_list = [status,start,creator,sid,amount,price]
    print("Insert: ",input_list)
    # create a new order
    cur.execute("INSERT INTO orders values (NULL, ?, ?, NULL, ?, NULL, ?, ?, ?)", input_list)
    con.commit()
    # update value in shop table
    cur.execute("UPDATE shop set amount=amount-? WHERE sid=?",[amount,sid])
    con.commit()
    cur.close()
    con.close()
    return jsonify({"info":"Success","status":1})

@app.route('/order/list/user/<uid>' , methods=['POST'])
def list_my_order(uid):
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    status = request.form['status']
    if status=="All": # show all orders by uid
        input_list = [uid]
        cur.execute("SELECT a.oid,a.status,a.start,a.finish,b.account,c.account,d.name,a.amount,a.price \
                    FROM orders as a \
                    left join user as b on a.creator=b.uid\
                    left join user as c on a.completer=c.uid\
                    left join shop as d on a.sid=d.sid \
                    WHERE a.creator=?", input_list)
    else:
        input_list = [status,uid]
        cur.execute("SELECT a.oid,a.status,a.start,a.finish,b.account,c.account,d.name,a.amount,a.price \
                    FROM orders as a \
                    left join user as b on a.creator=b.uid\
                    left join user as c on a.completer=c.uid\
                    left join shop as d on a.sid=d.sid \
                    WHERE a.status=? AND a.creator=?", input_list)
    data = [list(x) for x in cur.fetchall()]
    print(data)
    cur.close()
    con.close()
    return jsonify({"info":"Success","status":1,"data":data})

@app.route('/order/cancel/<uid>' , methods=['POST'])
def cancel_order(uid):
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    oid_list = request.form['data'].split()
    print('cancel receive oid: ',oid_list)
    finish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    input_list = [tuple(['-1',finish_time,uid,oid]) for oid in oid_list]
    # update orders status and cancel information 
    cur.executemany("UPDATE orders SET status=?,finish=?,completer=? WHERE oid=?",input_list)
    con.commit()
    # add the amount back
    # sum all of the amount group by sid
    cur.execute("SELECT SUM(amount),sid FROM orders WHERE oid IN ({}) GROUP BY sid".format(",".join("?"*len(oid_list))),oid_list)
    sum_of_order = cur.fetchall()
    print("sum of orders",sum_of_order) # [(amount,SID),(),()...]
    # update the amount in shop
    cur.executemany("UPDATE shop SET amount=amount+? WHERE sid=?",sum_of_order)
    con.commit()
    cur.close()
    con.close()
    return jsonify({"info":"Success","status":1})

@app.route('/order/complete/<uid>' , methods=['POST'])
def complete_order(uid):
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    oid_list = request.form['data'].split()
    print('cancel receive oid: ',oid_list)
    finish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    input_list = [tuple(['1',finish_time,uid,oid]) for oid in oid_list]
    # update the order list
    cur.executemany("UPDATE orders SET status=?,finish=?,completer=? WHERE oid=?",input_list)
    con.commit()
    cur.close()
    con.close()
    return jsonify({"info":"Success","status":1})

@app.route('/order/list/shop/<uid>' , methods=['POST']) # 列出工作店家的訂單
def list_shop_order(uid):
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    print('order list shop: ',request.form)
    status = request.form['status']
    work = request.form['work']
    if status=="All": # show all orders
        if work=="All":
            cur.execute("SELECT DISTINCT shop.name FROM shop left join work on shop.sid=work.sid where (work.uid=? or shop.uid=?)",(uid,uid,))
            db_return = cur.fetchall()
            input_list = [place[0] for place in db_return] #找到他在哪工作
            print('INPUT LIST: ',input_list)
            cur.execute("SELECT a.oid,a.status,a.start,a.finish,b.account,c.account,d.name,a.amount,a.price \
                        FROM orders as a \
                        left join user as b on a.creator=b.uid\
                        left join user as c on a.completer=c.uid\
                        left join shop as d on a.sid=d.sid \
                        WHERE d.name in ({})".format(",".join("?"*len(input_list))), input_list)
        else:
            input_list = [work]
            cur.execute("SELECT a.oid,a.status,a.start,a.finish,b.account,c.account,d.name,a.amount,a.price \
                        FROM orders as a \
                        left join user as b on a.creator=b.uid\
                        left join user as c on a.completer=c.uid\
                        left join shop as d on a.sid=d.sid \
                        WHERE d.name=? ", input_list)
    else:
        if work=="All":
            cur.execute("SELECT DISTINCT shop.name FROM shop left join work on shop.sid=work.sid where (work.uid=? or shop.uid=?)",(uid,uid,))
            workplace = [place[0] for place in cur.fetchall()]
            input_list = [status]
            input_list.extend(workplace)
            cur.execute("SELECT a.oid,a.status,a.start,a.finish,b.account,c.account,d.name,a.amount,a.price \
                        FROM orders as a \
                        left join user as b on a.creator=b.uid\
                        left join user as c on a.completer=c.uid\
                        left join shop as d on a.sid=d.sid \
                        WHERE a.status=? AND d.name=({})".format(",".join("?"*len(workplace))), input_list)
        else:
            input_list = [status,work]
            cur.execute("SELECT a.oid,a.status,a.start,a.finish,b.account,c.account,d.name,a.amount,a.price \
                        FROM orders as a \
                        left join user as b on a.creator=b.uid\
                        left join user as c on a.completer=c.uid\
                        left join shop as d on a.sid=d.sid \
                        WHERE a.status=? AND d.name=?", input_list)
                        
    data = cur.fetchall()
    print('return data is : ',data)
    cur.close()
    con.close()
    return jsonify({"info":"Success","status":1,"data":data})

@app.route('/shop/amount' , methods=['POST'])
def shop_amount():
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT name,amount FROM shop")
    data = cur.fetchall()
    print(data)
    cur.close()
    con.close()
    return_dict = {x[0]:x[1] for x in data}
    return jsonify({"info":"Success","status":1,"data":return_dict})


if __name__=='__main__':
    app.debug=True
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.run(host="0.0.0.0",port=5000)