import random


# 生成随机 ticket

def create_ticket():
    s = 'wer45ertewrwqtr'
    ticket = ''
    for i in range(10):
        ticket +=random.choice(s)
    return ('TK' + ticket)


def get_random_order_id():
    s = 'wer45ertewrwqtr'
    order_id = ''
    for i in range(10):
        order_id +=random.choice(s)
    return ('Dd' + order_id)