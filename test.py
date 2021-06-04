x = [1, 2, 1, 2, 1]
y = []
for i in x:
    if not i in y:
        y.append(i)
print(y)