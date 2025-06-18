from contextlib import contextmanager

@contextmanager
def open_file(file, mode):
    f = open(file, mode)
    try:
        yield f
    finally:
        f.close()

with open_file('sample.txt', 'w') as f:
    f.write("Today is the first I heard about context manager\n\n")
    f.write("Aur do theen line likh deta hu dena matlab \n\n")
    f.write("Arey yaar abhi toh do hi line hua h \n\n")
    f.write("Ab think h 4 line ho gaya \n\n")

print(f.closed) 
