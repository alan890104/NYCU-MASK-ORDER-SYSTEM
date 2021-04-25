import requests
import json

print("############## REGISTER ############## ")
r = requests.post("http://140.113.67.121:5000/user/register", data={'account': 'alan890104', 'passwd': '123456789','phone':'0913548678'})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/user/register", data={'account': 'fgjyh', 'passwd': '0000','phone':'0913548678'})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/user/register", data={'account': 'david', 'passwd': 'sdfqw','phone':'0911937178'})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/user/register", data={'account': 'yoyo', 'passwd': 'grtr','phone':'0917948678'})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/user/register", data={'account': 'BTC', 'passwd': 'sf','phone':'0917948665'})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/user/register", data={'account': 'dodo', 'passwd': 'gretr','phone':'0910949738'})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/user/register", data={'account': 'ETH', 'passwd': 'wreqjh','phone':'0914941948'})
print(json.loads(r.text))

print("############## LOGIN ############## ")
r = requests.post("http://140.113.67.121:5000/user/login", data={'account': 'alan890104', 'passwd': '123456789'})
print(json.loads(r.text))
uid = json.loads(r.text)['data']['uid']

r = requests.post("http://140.113.67.121:5000/user/login", data={'account': 'yoyo', 'passwd': 'grtr'})
print(json.loads(r.text))
uid_yoyo = json.loads(r.text)['data']['uid']

r = requests.post("http://140.113.67.121:5000/user/login", data={'account': 'dodo', 'passwd': 'gretr'})
print(json.loads(r.text))
uid_dodo = json.loads(r.text)['data']['uid']

r = requests.post("http://140.113.67.121:5000/user/login", data={'account': 'fgjyh', 'passwd': '0000'})
print(json.loads(r.text))
uid_fgjyh = json.loads(r.text)['data']['uid']

print("############## register_shop ############## ")
r = requests.post("http://140.113.67.121:5000/shop/register/{}".format(uid), data={'name': 'Alan\'s shop', 'city': 'Taoyuan','price':12,'amount':50000})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/shop/register/{}".format(uid_yoyo), data={'name': 'Yoyo\'s shop', 'city': 'Taipei','price':5,'amount':0})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/shop/register/{}".format(uid_dodo), data={'name': 'Dodo\'s shop', 'city': 'Hsinchu','price':7,'amount':1496})
print(json.loads(r.text))

print("############## query_shop ############## ")
r = requests.post("http://140.113.67.121:5000/shop/query")
print(json.loads(r.text))

r = requests.post("http://140.113.67.121:5000/shop/query/Alan's shop")
print(json.loads(r.text))

print("############## EDIT MASK ############## ")
r = requests.post("http://140.113.67.121:5000/mask/edit/Alan's shop",data={"price":49999,"amount":50000})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/shop/query/Alan's shop")
print(json.loads(r.text))
sid = json.loads(r.text)['data']['sid']
r = requests.post("http://140.113.67.121:5000/shop/query/Yoyo's shop")
print(json.loads(r.text))
yoyo_sid = json.loads(r.text)['data']['sid']
r = requests.post("http://140.113.67.121:5000/shop/query/Dodo's shop")
print(json.loads(r.text))
dodo_sid = json.loads(r.text)['data']['sid']

print("############## ADD EMPLOYEE ############## ")
r = requests.post("http://140.113.67.121:5000/employee/add",data={"sid":sid,"account":'yoyo'})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/employee/add",data={"sid":sid,"account":'david'})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/employee/add",data={"sid":yoyo_sid,"account":'fgjyh'})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/employee/add",data={"sid":dodo_sid,"account":'fgjyh'})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/employee/add",data={"sid":yoyo_sid,"account":'ETH'})
print(json.loads(r.text))
r = requests.post("http://140.113.67.121:5000/employee/add",data={"sid":dodo_sid,"account":'BTC'})
print(json.loads(r.text))


print("############## SHOW SHOP'S EMPLOYEE ############## ")
r = requests.post("http://140.113.67.121:5000/employee/query/sid/{}".format(sid),data={})
print(json.loads(r.text))

print("############## SHOW WORK PLACE ############## ")
r = requests.post("http://140.113.67.121:5000/employee/query/uid/{}".format(uid_yoyo),data={})
print(json.loads(r.text))


print("############## SEARCH BY CONDITION ############## ")
r = requests.post("http://140.113.67.121:5000/shop/query/condition/{}".format(uid_fgjyh),data={"shop":'yo',"city":'t','price_min':0,"price_max":10000,'amount_type':3,'only_show_work':1})
print(json.loads(r.text))

# r = requests.post("http://140.113.67.121:5000/shop/query/condition/{}".format(uid_fgjyh),data={"shop":'o',"city":None,'price_min':0,"price_max":None,'amount_type':None,'only_show_work':0})
# print(json.loads(r.text))

# r = requests.post("http://140.113.67.121:5000/shop/query/condition/{}".format(uid_fgjyh),data={"shop":None,"city":'a','price_min':0,"price_max":None,'amount_type':None,'only_show_work':0})
# print(json.loads(r.text))

# r = requests.post("http://140.113.67.121:5000/shop/query/condition/{}".format(uid_fgjyh),data={"shop":None,"city":None,'price_min':10,"price_max":None,'amount_type':None,'only_show_work':0})
# print(json.loads(r.text))

# r = requests.post("http://140.113.67.121:5000/shop/query/condition/{}".format(uid_fgjyh),data={"shop":None,"city":None,'price_min':0,"price_max":10000,'amount_type':None,'only_show_work':0})
# print(json.loads(r.text))

# r = requests.post("http://140.113.67.121:5000/shop/query/condition/{}".format(uid_fgjyh),data={"shop":None,"city":None,'price_min':0,"price_max":None,'amount_type':0,'only_show_work':0})
# print(json.loads(r.text))

# r = requests.post("http://140.113.67.121:5000/shop/query/condition/{}".format(uid_fgjyh),data={"shop":None,"city":None,'price_min':0,"price_max":None,'amount_type':None,'only_show_work':1})
# print(json.loads(r.text))