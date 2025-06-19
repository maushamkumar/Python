import time

class LoggerMeta(type):
    def __new__(cls, name, bases, dct):
        for attr_name, attr_value in dct.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                # Wrap methods with time logger
                def wrapper(func):
                    def inner(self, *args, **kwargs):
                        print(f"[LOG] Calling method: {func.__name__}")
                        start = time.time()
                        time.sleep(2)  
                        result = func(self, *args, **kwargs)
                        end = time.time()
                        print(f"[LOG] Method {func.__name__} took {end - start:.5f} seconds")
                        return result
                    return inner
                dct[attr_name] = wrapper(attr_value)
        return super().__new__(cls, name, bases, dct)



class Calculator(metaclass=LoggerMeta):
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b


calc = Calculator()
print(calc.add(10, 5))        # Logs the method call
print(calc.multiply(3, 4))    # Logs again
