s = {}
s[0] = [1]
for key, value in s.items():
    if 1 in value:
        value.append(2)

print(s)