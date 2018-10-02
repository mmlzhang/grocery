## 更改用户名



### POST 请求

```python

GET /user/profile/
```

##### params

```python

name str 新用户名
```

#### 成功响应

```python

{
    'code': 200, 
    'msg': '用户名更换成功'
}
```

#### 失败响应 1

```python

{
    'code': 1009, 
    'msg': '用户名已存在'
}
```

#### 失败响应 2

```python
{
    'code': 1008, 
    'msg': '数据库错误, 请稍后再试'
}
```











