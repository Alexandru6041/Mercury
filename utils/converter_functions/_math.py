def add_1(str:str):
    x = len(str) - 1
    t = 1

    while t and x >= 0:
        last = str[x]
        c = ord(last) + t

        if c <= ord('Z'):
            last = chr(c)
            t = 0
        
        else:
            last = 'A'
            t = 1
        
        str = str[:x] + last + str[x+1:]
        x -= 1
    
    if t:
        str = 'A' + str

    return str

if __name__ == '__main__':
    print(add_1('A'))
    print(add_1('Z'))
    print(add_1(add_1('Z')))
    print(add_1('AAZ'))