a = [(1, 2), 3]
while a:
    try:
        d = a.pop()
        b, c = d
    except TypeError:
        b = d
        c = "0"
    print(b, c)