def calculate(num1, num2, op):
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        return num1 / num2
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


num_of_el = input("number of elements: ")
while validate_number(num_of_el) is None:
    num_of_el = input("number of elements: ")
    validate_number(num_of_el)

num1 = input("Enter the 1-st number: ")
num1 = validate_number(num=num1)
while validate_number(num1) is None:
    num1 = input("Enter the 1-st number: ")
    num1 = validate_number(num=num1)

for i in range(1, int(num_of_el)):
    op = input("""Enter the operation: 
+, -, *, /, **: """)
    while validate_operation(op) is None:
        op = input("""Enter the operation: 
+, -, *, /, **: """)
        op = validate_operation(op=op)
    if i == 1:
        num2 = input("Enter the 2-nd number: ")
        num2 = validate_number(num=num2)
        while validate_number(num2) is None:
            num2 = input("Enter the 2-nd number: ")
            num2 = validate_number(num=num2)
    elif i == 2:
        num2 = input("Enter the 3-rd number: ")
        num2 = validate_number(num=num2)
        while validate_number(num2) is None:
            num2 = input("Enter the 3-rd number: ")
            num2 = validate_number(num=num2)
    else:
        num2 = input(f"Enter the {i+1}-th number: ")
        num2 = validate_number(num=num2)
        while validate_number(num2) is None:
            num2 = input(f"Enter the {i+1}-th number: ")
            num2 = validate_number(num=num2)

    if op == "/" and num2 == 0:
        print("You try to division by zero, that returns Infinity! Therefore, further calculations will not be carry "
              "out.")
        break
    else:
        num1 = calculate(num1=num1, num2=num2, op=op)

else:
    if num1.is_integer():
        num1 = int(num1)
    print(f"Result is {num1}")
