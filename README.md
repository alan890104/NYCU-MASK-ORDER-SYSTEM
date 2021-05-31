# 資料庫-口罩訂購系統

## 使用者
### 使用者登入(後端)
```python=
#route 140.113.67.121:5000/user/login method='POST'
login request
{
    "account": string
    "passwd":  string
}

Retrun(json)
{
    "info":"User Not Exist"/"Password Not Correct"/"Success"
    "status": 0(FAIL)/1(Success)
    "data":{
            (只有在Success時才會有值)
            "uid":     string
            "account": string
            "phone" :  string
            }
}
```

### 使用者註冊(後端)
```python=
#route 140.113.67.121:5000/user/register method='POST'
register request
{
    "account": string
    "passwd":  string
    "phone":   string
}

Retrun(json):
{
    info: "Success"/"Fail"(帳號已被註冊)
    status: 1/0
} 
```

## 商店
### 註冊商店(後端)
```python=
#route 140.113.67.121:5000/shop/register/<使用者uid> method='POST'
register_shop request
{
    "name": string
    "city":  string
    "price":  unsigned int 
    "amount": unsigned int
}

Retrun(json):
{
    info: "Success"/"Fail"(店家名稱已被註冊)
    status: 1/0
} 
```


### 列出全部商店資訊(後端)
```python=
#route 140.113.67.121:5000/shop/query method='POST'
access store request
{
    不用傳東西，我直接給你全部的商店列表讓你在前端好排序 :)
}

Retrun(json):
{
    info: "Success"
    status: 1
    data:
            [   
                這裡都是list喔~
                ["sid","name","city","price","amount","uid"],
                ["sid","name","city","price","amount","uid"],
                .
                .
                .
            ]

} 
```

### 用uid得到使用者註冊的商店資訊(後端)
```python=
#route 140.113.67.121:5000/shop/query/uid/<使用者uid> method='POST'
query specify shop request(by uid)
{
    不用任何咚咚 店家名字放在route裡面
}

Retrun(json):
{
    info: "Success"/"Fail"(商店不存在)
    status: 1/0
    data:{
            成功才會有值
            "sid":  string
            "name": string
            "city": string
            "price": unsigned int
            "amount": unsigned int
            "uid": string
         }
} 
```

### 用商店名稱得到指定店家資訊(後端)
```python=
#route 140.113.67.121:5000/shop/query/name/<name>  method='POST'
query specify shop request(by name)
{
    不用任何咚咚 店家名字放在route裡面
}

Retrun(json):
{
    info: "Success"/"Fail"(商店不存在)
    status: 1/0
    data:{
            成功才會有值
            "sid":  string
            "name": string
            "city": string
            "price": unsigned int
            "amount": unsigned int
            "uid": string
         }
} 
```



### 用sid得到指定店家資訊(後端)
```python=
#route 140.113.67.121:5000/shop/query/sid/<sid>  method='POST'
query specify shop request(by sid)
{
    不用任何咚咚 店家名字放在route裡面
}

Retrun(json):
{
    info: "Success"/"Fail"(商店不存在)
    status: 1/0
    data:{
            成功才會有值
            "sid":  string
            "name": string
            "city": string
            "price": unsigned int
            "amount": unsigned int
            "uid": string
         }
} 
```

### 商店以條件搜尋(後端)
```python=
#route 140.113.67.121:5000/shop/query/condition/<使用者uid>  method='POST'
query shop by condition request
{
    "shop": string(沒有輸入的話預設就是null)
    "city": string(沒有輸入的話預設就是null)
    "price_min": unsigned_int(沒有輸入的話預設0)
    "price_max": unsigned_int(沒有輸入的話預設就是null)
    "amount_type": int (0:0(售完), 1:1~5000(稀少), 2:5001以上(充足),未輸入的話填null)
    "only_show_work": int (1(True)/0(False))
}

Retrun(json):
{
    info: "Success"
    status: 1
    data:   
            [   
                這裡都是list喔~
                ["sid","name","city","price","amount","uid"],
                ["sid","name","city","price","amount","uid"],
                .
                .
                .
            ]
} 
```


### 修改口罩價格數量(後端)
```python=
#route 140.113.67.121:5000/mask/edit/<sid> method='POST'
edit mask request
{
    傳過來指定店家最新的口罩數量與價格，無論是哪一個被改了
    "amount": unsigned int
    "price":  unsigned int
}

Retrun(json):
{
    info: "Success"/"Fail"
    status: 1/0
} 
```

### 增加店家員工(後端)
```python=
#route 140.113.67.121:5000/employee/add method='POST'
add employee request
{
    "sid": 店家sid
    "account": 要被添加的員工的帳號
}

Retrun(json):
{
    info: "Success"/"Fail"
    status: 1/0
} 
```

### 刪除店家員工(後端)
```python=
#route 140.113.67.121:5000/employee/del method='POST'
delete employee request
{
    "sid": 店家sid
    "account": 要被刪除的員工的帳號
}

Retrun(json):
{
    info: "Success"/"Fail"
    status: 1/0
} 
```

### 列出店家員工的資訊(後端)
```python=
#route 140.113.67.121:5000/employee/query/sid/<店家sid> method='POST'
add employee request
{
    不用~
}

Retrun(json):
{
    "info": "Success"
    status: 1
    "data":
            [
                [account,phone],
                [account,phone],
                .
                .
                .
            ]
} 
```

### 列出一個人在哪些店家工作(後端)
```python=
#route 140.113.67.121:5000/employee/query/uid/<使用者uid> method='POST'
add employee request
{
    不用~
}

Retrun(json):
{
    "info": "Success"
    status: 1
    "data":
            [
                [name],
                [name],
                .
                .
                .
            ]
} 
```

## 訂單
* 在此先定義 已取消="-1", 未完成=:"0", 已完成="1", 全部="All"
* 訂單日期格式為 YYYY-MM-DD HH:MM:SS


### 建立訂單
```python=
#route 140.113.67.121:5000/order/create/<uid> method='POST'
create order request
{
    name: 店家名稱
    amount: 訂購數量
    price: 訂購時的價格
}

Reply:
{
    info: "Success"
    status: 1
} 
```

### 列出自己所有的訂單
* 前端只有"未完成"的訂單可以進行選取並執行取消等動作
```python=
#route 140.113.67.121:5000/order/list/user/<uid> method='POST'
list order request
{
    status:訂單狀態('-1','0','1','All')
}

Reply:
{
    info: "Success"
    status: 1
    data:
        [
            [   
                OID, 
                status, 訂單狀態('-1','0','1')
                start, 是datetime格式
                finish, 是datetime格式(可為null)
                creator, 自己的帳號(資料庫是存UID)
                completer,回傳帳號名稱(資料庫存UID)(可為null)
                shop name,回傳店家名稱(資料庫是存SID)
                amount,
                price,
            ],
            .
            .
            .
            .
        ]
} 
```

### (批量)取消訂單
```python=
#route 140.113.67.121:5000/order/cancel/<uid> method='POST'
cancel order request
{
    data:[OID_1,OID_2,...]把要取消的OID存成list回傳
}

Reply:
{
    info: "Success"
    status: 1
} 
```

### (批量)完成訂單
:::danger
當員工在批量完成訂單的時候，先判斷前端在每個店家批量選擇的數量是否有超過該店家的實際數量!!! 
:::
```python=
#route 140.113.67.121:5000/order/complete/<uid> method='POST'
complete order request
{
    data:[OID_1,OID_2,...]把要完成的OID存成list回傳
}

Reply:
{
    info: "Success"
    status: 1
} 
```

### 回傳全部店家的名稱+口罩數量
方便前端核對批量完成的數量是否相符
```python=
#route 140.113.67.121:5000/shop/amount method='POST'
 request
{
    不用
}

Reply:
{
    info: "Success"
    status: 1
    data:{
            "店家名稱": 口罩數量
            .
            .
            .
        }
} 
```



### 列出工作店家所有的訂單
* 前端只有"未完成"的訂單可以進行選取並執行取消等動作
```python=
#route 140.113.67.121:5000/order/list/shop/<uid> method='POST'
list order request
{
    work: 工作店家(是一個string)('All','店家1的店名','店家2的店名'...)
    
    status:訂單狀態('-1','0','1','All')
}

Reply:
{
    info: "Success"
    status: 1
    data:
        [
            [   
                OID, 
                status, 訂單狀態('-1','0','1')
                start, 是datetime格式
                finish, 是datetime格式(可為null)
                creator, 自己的帳號(資料庫是存UID)
                completer,回傳帳號名稱(資料庫存UID)(可為null)
                shop name,回傳店家名稱(資料庫是存SID)
                amount,
                price,
            ],
            .
            .
            .
            .
        ]
} 
```