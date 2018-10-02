## 获取用户个人信息



### GET 请求

```python

GET /user/user_info/
```

#####  params

```python

NULL
```

#### 成功响应

```python

{
    'code': 200, 
    'data': {
        'name': '小明',
        'phone': '13500000000',
        'avatar': '/static/upload/avatar.jpg',
    }
}
```

#### 失败响应 1

```python

{
    'code': 1011, 
    'msg': '用户未登录'
}
```

