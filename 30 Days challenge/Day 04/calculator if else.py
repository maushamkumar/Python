# Taking user input
num1 = float(input("Enter first number: "))
op = input("Enter operator (+, -, *, /, %): ")
num2 = float(input("Enter second number: "))

# Conditional logic
if op == '+':
    print("Result:", num1 + num2)
elif op == '-':
    print("Result:", num1 - num2)
elif op == '*':
    print("Result:", num1 * num2)
elif op == '/':
    if num2 != 0:
        print("Result:", num1 / num2)
    else:
        print("Error: Division by zero is not allowed")
elif op == '%':
    print("Result:", num1 % num2)
else:
    print("Invalid operator")