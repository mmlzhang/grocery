## 用户注册



### GET 请求

```python

GET /user/register/
```

##### params

```python

NULL
```

#### 成功响应

```python

返回页面   register.html
```

#### 失败响应

```python

404.html
```



### POST 请求

```python

POST /user/register/
```

#### params

```python

mobile str 用户手机号码
password str 用户密码
password2 str 用户确认的密码
```

#### 成功响应

```python

{ 
    'code': 200, 
    'msg': '注册成功!'
}
```



#### 失败响应1

```python

{
    'code': 1004, 
    'msg': '用户信息不完整'
}
```



#### 失败响应 2

```python

{
    'code': 1002, 
    'msg': '手机号码不正确'
}
```



#### 失败响应3

```python

{
    'code': 1003, 
    'msg': '密码不一致'
}
```



#### 失败响应 4

```python

{
    'code': 1004, 
    'msg': '该用户已注册,请直接登录'
}
```



















