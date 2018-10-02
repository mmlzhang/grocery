## 用户登录



### GET 请求

```python

GET /user/login/
```

##### params

```python

NULL
```

#### 成功响应

```python

返回页面   login.html
```

#### 失败响应

```python

404.html
```



### POST 请求

```python

POST /user/login/
```

#### params

```python

mobile str 用户手机号码
password str 用户密码
```

#### 成功响应

```python

{
    'code': 200, 
    'msg': '登录成功!'
}
```



#### 失败响应 1 

```python

{
    'code': 1002, 
    'msg': '手机号码不正确'
}
```



#### 失败响应 2

```python

{
    'code': 1004, 
    'msg': '用户信息不完整'
}
```



#### 失败响应 3 

```python

{
    'code': 1005, 
    'msg': '该用户不存在, 请先注册'
}
```



#### 失败响应 4

```python

{
    'code': 1006, 
    'msg': '密码输入错误'
}
```



















