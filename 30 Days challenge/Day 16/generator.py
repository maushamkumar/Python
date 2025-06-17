def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def main():
    print("📈 Fibonacci Number Generator")
    fib = fibonacci_generator()
    
    while True:
        user_input = input("Press Enter to get the next number (or type 'exit' to quit): ")
        if user_input.lower() == 'exit' or user_input.lower() == 'quit':
            print("Goodbye!")
            break
        print(next(fib))

if __name__ == "__main__":
    main()
