from ABH import *
def save_data(data):
    r.rpush("users", data)
    return r.lrange('users', 0, -1)
def load_data():
    return r.lrange('users', 0, -1)
