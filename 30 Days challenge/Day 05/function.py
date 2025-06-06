def bring_water():
    print("Bringing water for papa... 🧊💧")

# Calling the function
bring_water()


def bring_items(item):
    print(f"Bringing {item} for papa... ☕")

# Calling the function
bring_items("chai")
bring_items("water")


def bring_items_return(item):
    return f"{item.capitalize()} delivered to papa! ✅"

# Calling the function
msg = bring_items_return("chai")
print(msg)


def calculator(a, b, operation):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b if b != 0 else "Can't divide by zero"
    else:
        return "Invalid operation"

# Calling calculator function
print(calculator(10, 5, "add"))        # 15
print(calculator(10, 5, "subtract"))   # 5
