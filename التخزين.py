from ABH import *
def save_data(data):
    return r.sadd("save_users", data)
def load_data():
    return r.smembers("save_users")
