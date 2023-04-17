file = open("codes.txt","r")
result = []

# while True:
data = file.readlines()
data = map(lambda s: s.strip(), data)
print(data)
# for line in data:
#     result.append(int(line.strip().split('-')[-1]))

# print(result)
# data = file.readlines()
file.close()
