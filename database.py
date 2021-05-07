import sqlite3
import hashlib
import os

def create_table(cur):
    # 使用者列表
    cur.execute("create table   user (uid  PRIMARY KEY, \
                                     account TEXT NOT NULL UNIQUE,\
                                     passwd  TEXT NOT NULL,\
                                     phone   TEXT NOT NULL )")

    # 商店列表
    cur.execute("create table   shop (sid  PRIMARY KEY, \
                                     name TEXT NOT NULL UNIQUE,\
                                     city TEXT NOT NULL,\
                                     price  UNSIGNED INT NOT NULL,\
                                     amount UNSIGNED INT NOT NULL,\
                                     uid NOT NULL UNIQUE,\
                                     FOREIGN KEY(uid) REFERENCES user(uid))")

    # 店員在店家工作                                 
    cur.execute("create  table  work (sid  NOT NULL ,\
                                      uid  NOT NULL ,\
                                      PRIMARY KEY(sid,uid)\
                                      FOREIGN KEY(uid) REFERENCES user(uid),\
                                      FOREIGN KEY(sid) REFERENCES shop(sid))")
def create_trigger(cur):
    cur.execute("CREATE TRIGGER uid_generate\
                AFTER INSERT ON user\
                FOR EACH ROW\
                WHEN (NEW.uid IS NULL)\
                BEGIN\
                    UPDATE user SET uid = (select hex( randomblob(8)) ) WHERE rowid = NEW.rowid;\
                END;")   
    cur.execute("CREATE TRIGGER sid_generate\
                AFTER INSERT ON shop\
                FOR EACH ROW\
                WHEN (NEW.sid IS NULL)\
                BEGIN\
                    UPDATE shop SET sid = (select hex( randomblob(8))) WHERE rowid = NEW.rowid;\
                END;")

def encrypt(data):
    obj = hashlib.sha256(b'nycu')
    obj.update(data.encode())
    return obj.hexdigest()

def add_user(con,cur,account,encrpt_passwd,phone):
    try:
        input_list = [account,encrpt_passwd,phone]
        cur.execute("insert into user values (NULL, ?, ?, ?)", input_list)
        con.commit()
        return 'Success',1
    except Exception as e:
        print(e)
        return 'Fail',0

def add_shop(con,cur,name,city,price,amount,uid):
    try:
        input_list = [name,city,price,amount,uid]
        cur.execute("insert into shop values (NULL, ?, ?, ?, ?,?)", input_list)
        con.commit()
        return 'Success',1
    except Exception as e:
        print(e)
        return 'Fail',0

def update_mask_price_amount(con,cur,sid,price,amount):
    try:
        cur.execute("UPDATE shop SET price=?,amount=? WHERE sid = ?",(price,amount,sid,))
        con.commit()
        return 'Success',1
    except Exception as e:
        print(e)
        return 'Fail',0

def add_employee(con,cur,sid,account):
    try:
        cur.execute("SELECT uid FROM user where account=?",(account,))
        uid = cur.fetchone()[0]
        cur.execute("Insert into work values (?,?)",(sid,uid,))
        con.commit()
        return 'Success',1
    except Exception as e:
        print(e)
        return 'Fail',0

def del_employee(con,cur,sid,account):
    try:
        cur.execute("SELECT uid FROM user where account=?",(account,))
        uid = cur.fetchone()[0]
        cur.execute("DELETE FROM work where sid=? and uid=?)",(sid,uid,))
        con.commit()
        return 'Success',1
    except Exception as e:
        print(e)
        return 'Fail',0

def list_shop(con,cur):
    cur.execute("SELECT * FROM shop")
    return cur.fetchall()


def drop_trigger(con,cur):
    cur.execute("DROP TRIGGER IF EXISTS uid_generate")
    cur.execute("DROP TRIGGER IF EXISTS sid_generate")
    con.commit()

    
if __name__=='__main__':
    try:
        os.remove('DB.sqlite3')
    except:
        pass
    con = sqlite3.connect("DB.sqlite3")
    cur = con.cursor()
    create_table(cur)
    create_trigger(cur)
     
    # obj = hashlib.sha256(b"nycu")
    # uid = '9487'
    # account = 'alan890104'
    # passwd = encrypt(obj, '123456789')
    # phone = '0908119998'
    # add_user(con,cur,account,passwd,phone)

    # cur.execute("SELECT * FROM user")
    # ans = cur.fetchall()
    # print(ans)

    cur.close()
    con.close()
