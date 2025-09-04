import bcrypt


def hash(password:str)-> str:
    salt = bcrypt.gensalt()
    hashed=bcrypt.hashpw(password=password.encode(),salt=salt)
    return hashed.decode()


def check(password:str,hashed:str)-> str:
    return bcrypt.checkpw(password.encode(),hashed.encode())



