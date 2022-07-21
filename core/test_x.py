import time
import marshal
import base64
path = r"C:\Users\pc\Pictures\Pictures.zip"
def wrapper(func):
    beginx = time.time()
    func()
    endix = time.time()
    print("%s: %s" % (func.__name__,beginx-endix))
@wrapper
def b16():
    global path
    base64.b16encode(open(path,"rb").read())
@wrapper
def b85():
    global path
    base64.b85encode(open(path,"rb").read())
@wrapper
def marshal_dump():
    global path
    marshal.dumps(open(path,"rb").read())
