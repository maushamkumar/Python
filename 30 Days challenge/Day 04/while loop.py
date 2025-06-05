print("Welcome to Mausham's Calculator (While Loop Version)")

while True:
    num1 = float(input("\nEnter first number: "))
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

    # Ask user if they want to continue
    choice = input("Do you want to do another calculation? (yes/no): ").lower()
    if choice != "yes":
        print("Thanks for using Mausham's Calculator!")
        break
