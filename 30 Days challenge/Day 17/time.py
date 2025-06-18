import time
from contextlib import contextmanager

@contextmanager
def timer(name="Block"):
    start = time.time()
    print(f"[{name}] Started...")
    yield
    end = time.time()
    print(f"[{name}] Finished in {end - start:.2f} seconds.")

# Usage
with timer("Sleeping"):
    time.sleep(2)
