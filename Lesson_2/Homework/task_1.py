def calculate(num1, num2, op):
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/" and num2 != 0:
        return num1 / num2
    elif op == "/" and num2 == 0:
        return f"{None}, because division by zero!"
    elif op == "**":
        return num1 ** num2


def validate_number(num):
    try:
        return float(num)
    except Exception as error:
        print(error)
        print()
        return None


def validate_operation(op):
    operations = ("+", "-", "*", "/", "**")
    try:
        if op not in operations:
            raise ValueError("Invalid operation!")
    except Exception as error:
        print(error)
        print()
        return None
    return op


num1 = input("Enter the first number: ")
num1 = validate_number(num=num1)
while validate_number(num1) is None:
    num1 = input("Enter the first number: ")
    num1 = validate_number(num=num1)

num2 = input("Enter the second number: ")
num2 = validate_number(num=num2)
while validate_number(num2) is None:
    num2 = input("Enter the second number: ")
    num2 = validate_number(num=num2)

op = input("""Enter the operation: 
+, -, *, /, **: """)
while validate_operation(op) is None:
    op = input("""Enter the operation: 
+, -, *, /, **: """)
    op = validate_operation(op=op)

result = calculate(num1=num1, num2=num2, op=op)

if type(result) is float and result.is_integer():
    result = int(result)
print(f"Result is {result}")
