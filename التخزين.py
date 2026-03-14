from ABH import *
def save_data(data):
    r.rpush("USERS", data)
    return r.sadd("USERS", data)
def load_data():
    return r.smembers("USERS")
