## 更新用户的头像文件



### GET 请求

```python

GET /user/profile/
```

##### params

```python

NULL
```

#### 成功响应

```python

返回页面 profile.html
```

#### 失败响应 1

```python

404.html
```



### POST 请求

```python

GET /user/profile/
```

##### params

```python

avatar str 用户头像
```

#### 成功响应

```python

{
    'code': 200,
    'img_url': /static/upload/user.png,
}
```

#### 失败响应 1

```python

{
    'code': 1007, 
    'msg': '文件格式不正确'
}
```

#### 失败响应 2

```python

{
    'code': 1008, 
    'msg': '数据库错误, 请稍后再试'
}
```











