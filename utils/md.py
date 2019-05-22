import time, hashlib
def md5(user_name):
    ctime = str(time.time())
    m = hashlib.md5(bytes(user_name, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()

def password_md5(password):
    p_str_1='taojiji'
    p_str_2='shandian@taojiji'
    m=hashlib.md5(bytes(password+p_str_1, encoding='utf-8'))
    m.update(bytes(p_str_2, encoding='utf-8'))
    return m.hexdigest()