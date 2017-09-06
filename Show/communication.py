import socket,json


# 一个通用的hello测试函数
def testHello(deviceip,port,key):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 5秒连接超时
    s.settimeout(5)

    try:
        s.connect((deviceip, int(port)))
        message = key+" "+"HELLO\n"
        s.send(message.encode())
        getrespond = s.recv(1024).decode()
        s.close()

        change = json.loads(getrespond)
        if(change.get("result",None)=="SUCCESS"):
            return "SUCCESS"
        else:
            print("鉴权码错误！！！")
            return "FAIL"
    # 如果连接超时
    except socket.timeout as e:
        print("连接超时！！！")
        return "FAIL"
    # 如果结果不符合JSON格式
    except json.JSONDecodeError as e2:
        print("编码错误！！！")
        return "FAIL"