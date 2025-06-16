def my_decorator(func):
    def wrapper():
        print("Kon Call kiya mujhe")
        func()
        print("Ab call kar hi diya toh answer upper h")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
