print("Welcome to Mausham's Calculator (For Loop Version)")

times = int(input("How many times do you want to run the calculator? "))

for i in range(times):
    print(f"\nCalculation {i+1}")
    num1 = float(input("Enter first number: "))
    op = input("Enter operator (+, -, *, /, %): ")
    num2 = float(input("Enter second number: "))

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
