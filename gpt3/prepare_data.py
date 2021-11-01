import os
import subprocess

out = subprocess.check_output(["ls"])
l = [i for i in out.decode("utf-8").splitlines() if os.path.isdir(i)]
print(l)
subprocess.call(["ls", l[0]])
os.system(f"ls {l[0]}")

import threading
import time

def some_function(a):
    if a < 5:
        print("sleeping 5 seconds")
    time.sleep(5)
    print(a)

threads = []
for i in range(10):
    t = threading.Thread(target=some_function, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

