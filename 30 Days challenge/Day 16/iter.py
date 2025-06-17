class CustomRange:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self  # returns the iterator object

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        val = self.current
        self.current += 1
        return val

def main():
    print("🔢 Custom Range Iterator")
    start = int(input("Enter start value: "))
    end = int(input("Enter end value: "))
    
    custom_range = CustomRange(start, end)
    
    for num in custom_range:
        print(num)

if __name__ == "__main__":
    main()
