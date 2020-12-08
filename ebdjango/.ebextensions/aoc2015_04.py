import hashlib 

string = 'bgvyzdsv'
i = 0
while True:
    code = bytes(string + str(i),'utf-8')
    result = hashlib.md5(code) 
    if result.hexdigest()[:6] == '000000':
        print(i)
        print(result.hexdigest())
        print(string + str(i))
        break
    i += 1