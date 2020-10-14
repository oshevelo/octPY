import math

ex = input("Enter the expression: ")

operations = ("+", "-", "*", "/", "**")
for _ in ex:
    if ex.find("pi") != -1:
        ex = ex.replace("pi", str(math.pi))
    elif ex.find("e") != -1:
        ex = ex.replace("e", str(math.e))

for i in range(1, len(ex)):
    if ex[i] != "." and ex[i] != " " and ex[i] in operations:
        if ex[i-1] != " ":
            ex = f"{ex[:i]} {ex[i:]}"
    elif ex[i].isdigit() and ex[i-1] in operations:
        ex = f"{ex[:i]} {ex[i:]}"

print(ex, len(ex))